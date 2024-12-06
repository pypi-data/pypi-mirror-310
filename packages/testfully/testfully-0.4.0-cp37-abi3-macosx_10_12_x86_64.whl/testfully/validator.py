import importlib
import importlib.util
import os
import sys
import time
import traceback

from typing import Any, Callable, Dict, Set


mono_ref = time.monotonic_ns()


def print_with_timestamp(*args, **kwargs):
    wall_elapsed_ms = (time.monotonic_ns() - mono_ref) // 1_000_000
    (
        kwargs['file'] if 'file' in kwargs else sys.stdout
    ).write("[+{: 8}ms] ".format(wall_elapsed_ms))
    print(*args, **kwargs)


def import_file(name: str, filepath: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def is_test_file(name: str) -> bool:
    # https://docs.pytest.org/en/latest/explanation/goodpractices.html#test-discovery
    return (name.startswith("test_") and name.endswith('.py')) or name.endswith("_test.py")


def import_with_capture(fq, c_out, c_err):
    with io.StringIO() as f:
        with contextlib.redirect_stdout(f) if c_out else contextlib.nullcontext(), \
                contextlib.redirect_stderr(f) if c_err else contextlib.nullcontext():
            try:
                importlib.__import__(fq, fromlist=())
            except:
                if c_out or c_err:
                    print_with_timestamp(f'--- captured output for: {fq}')
                    sys.stderr.write(f.getvalue())
                raise


def recursive_import_tests(path: str, import_prefix: str, hook: Any,
                           errors: Dict[str, BaseException]) -> Set[str]:
    # catch stdout/stderr to prevent noise from packages being imported
    capture_out = getattr(hook, 'CAPTURE_STDOUT', True)
    capture_err = getattr(hook, 'CAPTURE_STDERR', True)

    imported = set()

    init_py = os.path.join(path, '__init__.py')
    if os.path.exists(init_py):
        try:
            import_with_capture(import_prefix, capture_out, capture_err)
        except BaseException as ex:
            # NB: this should not happen, report so it can be fixed and proceed
            errors[init_py] = ex

    with os.scandir(path) as it:
        for e in it:
            if e.is_dir():
                imported |= recursive_import_tests(e.path, import_prefix + '.' + e.name, hook, errors)
            elif e.is_file() and is_test_file(e.name):
                if hasattr(hook, 'before_file'):
                    hook.before_file(e, import_prefix)
                fq = import_prefix + "." + e.name[:-3]
                try:
                    import_with_capture(fq, capture_out, capture_err)
                    imported.add(fq)
                except BaseException as ex:
                    # NB: this should not happen, report so it can be fixed and proceed
                    errors[e.path] = ex
                if hasattr(hook, 'after_file'):
                    hook.after_file(e, import_prefix)

    return imported


def validate(py_tracked, rust_graph, filter_fn: Callable[[str], bool], package = None) -> int:
    diff_count = 0
    for module, pydeps in py_tracked.items():
        if not filter_fn(module):
            continue
        rdeps = rust_graph.module_depends_on(module, package) or frozenset()

        # NB: we only care about anything that the rust code might be missing
        # it's safe to consider extra dependencies, and in fact expected since
        # the rust parser goes deep and tracks import statements inside code
        # that might never get executed whereas by design the python validation
        # will only track anything that gets executed during the import phase
        rust_missing = pydeps - rdeps
        if rust_missing:
            diff_count += 1
            print(f'{module} rust {len(rdeps)} / py {len(pydeps)}: rust missing {len(rust_missing)} {rust_missing}')
    return diff_count


if __name__ == '__main__':
    """
    Usage: validator <path/to/hook.py> [<path/to/serialized/graph>]
    
    Purpose:
    
    This files is part of a multi-pronged system to validate the correctness of
    the rust-implemented ModuleGraph provided by this package.
    
    Specifically, it is concerned with validating that, the transitive closure
    of dependencies for a set of test files is computed properly, to give
    confidence in the computation of its transpose: the set of affected tests to
    run given a set of modified files.
       
    Python import tracking is a *very hard* problem, because arbitrary Python
    code can be executed at import time, and arbitrary imports can be loaded
    at run time! We do our best to deal with that as follows:
     - the rust parser goes deep, extracting import statements even in code that
       might never be executed (it does however ignore typechecking-only
       imports). These are not going to be reported by the Python validator
       and that's OK. Better to have false positives (detected imports that
       are not used) than false negatives (undetected imports).
     - the python validator actually runs arbitrary python code during import
       tracking, because that's how Python rolls, so it is able to find
       dynamically-loaded imports, provided they are resolved at import-time
       (i.e. triggered by a module-level statement). This is good as it shows
       blind spots in the rust parser and gives us an opportunity to make those
       dynamic dependencies explicit.
     - neither the rust parser nor the python validator can catch dependencies
       that are resolved dynamically at run-time. Those are generally not a
       good idea exactly because they escape static analysis and are a major
       source of bugs. These are addressed in a separate validation step that
       need to be incorporated in the actual test runner, to detect whether a
       given test had run-time dynamic imports not covered by the validator.
    
        
    """
    import io
    import contextlib

    hook = import_file("_validator_hook", sys.argv[1])

    from . import ModuleGraph, tracker

    t = tracker.Tracker()
    t.start_tracking(hook.GLOBAL_NAMESPACES | hook.LOCAL_NAMESPACES,
                     patches=getattr(hook, 'IMPORT_PATCHES', None),
                     record_dynamic=True,
                     dynamic_anchors=getattr(hook, 'DYNAMIC_AGGREGATE', None),
                     dynamic_ignores=getattr(hook, 'DYNAMIC_IGNORE', None),
                     log_file=getattr(hook, 'TRACKER_LOG', None),
                     )

    if hasattr(hook, 'setup'):
        hook.setup()

    # TODO: we could move most of this into a separate thread
    # load graph from file if provided, otherwise parse the repo
    if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
        print_with_timestamp("--- loading existing rust-based import graph")
        g = ModuleGraph.from_file(sys.argv[2])
    else:
        print_with_timestamp("--- building fresh import graph using rust extension")
        g = ModuleGraph(
            hook.package_map(),
            hook.GLOBAL_NAMESPACES,     # unified namespace
            hook.LOCAL_NAMESPACES,      # per-pkg namespace
            getattr(hook, 'EXTERNAL_IMPORTS', set()) | {'importlib', '__import__'},
            getattr(hook, 'dynamic_dependencies', dict)()
        )

        if hasattr(hook, 'dynamic_dependencies_at_edges'):
            print_with_timestamp("--- computing dynamic dependencies")
            unified, per_pkg = hook.dynamic_dependencies_at_edges()
            print_with_timestamp("--- incorporating dynamic dependencies")
            g.add_dynamic_dependencies_at_edges(unified, per_pkg)

        if len(sys.argv) > 2:
            print_with_timestamp("--- saving import graph")
            g.to_file(sys.argv[2])

    # keep track or errors and import differences
    files_with_missing_imports = 0
    error_count = 0

    # TODO: user-defined order (toposort of package dep graph...)
    print_with_timestamp(f"--- tracking python imports")
    for base, sub in sorted(hook.test_folders().items()):
        assert sub in hook.LOCAL_NAMESPACES, f"{sub} not in {hook.LOCAL_NAMESPACES}"

        # some packages do not have tests, simply skip them
        if not os.path.isdir(os.path.join(base, sub)):
            continue

        # print_with_timestamp(f"--- {base}")
        # put package path first in sys.path to ensure finding test files
        sys.path.insert(0, os.path.abspath(base))
        old_k = set(sys.modules.keys())

        if hasattr(hook, 'before_folder'):
            hook.before_folder(base, sub)

        errors = {}

        # we want to import every test file in that package, recursively,
        # while preserving the appropriate import name, to allow for:
        #  - resolution of __init__.py
        #  - resolution of test helpers, via absolute or relative import
        imported = recursive_import_tests(os.path.join(base, sub), sub, hook, errors)

        if errors:
            error_count += len(errors)
            print(f"{len(errors)} exceptions encountered!")

            for filepath, ex in errors.items():
                print_with_timestamp(f'--- {filepath}')
                print(f'{type(ex)} {ex}')
                tb = traceback.extract_tb(ex.__traceback__)
                traceback.print_list(
                    tb
                    if tb[-1].filename == tracker.__file__ else
                    tracker.omit_tracker_frames(tb)
                )

        # test_dyn = {m: v for m, v in t.dynamic_users.items() if m.partition('.')[0] == sub}
        # if test_dyn:
        #     print(test_dyn)
        # print(t.dynamic_imports)

        with_dynamic = {}
        for m in imported:
            dyn_raw = {
                i
                for u in t.dynamic_users.get(m, ())
                for i in t.dynamic_imports.get(u, ())
            }
            dyn_new = dyn_raw - t.tracked[m]
            # if dyn_new:
            #      print(f"{m}: +{len(dyn_new)}/{len(dyn_raw)} dynamic from {t.dynamic_users.get(m)}")
            with_dynamic[m] = t.tracked[m] | dyn_new

        # NB: do validation at the package level for the test namespace
        # this is necessary because it is not a unified namespace. There can be
        # conflicts between similarly named test modules across packages.
        #
        # NB: we only validate test files, not test helpers. This is because, for
        # performance reason, dynamic dependencies are only applied to nodes of the
        # import graphs that do not have any ancestors (i.e modules not imported by
        # any other module)
        # This is fine because the purpose of this validation is to ensure that we
        # can determine a set of affected *test files* from a given set of modified
        # files, so as long as we validate that tests have matching imports between
        # python and Rust, we're good to go.
        def is_local_test_module(module: str) -> bool:
            last = module.rpartition('.')[2]
            return module.startswith(sub) and (last.startswith('test_') or last.endswith('_test'))

        files_with_missing_imports += validate(
            with_dynamic,
            g,
            package=base,
            filter_fn=is_local_test_module
        )

        # cleanup to avoid contaminating subsequent iterations
        sys.path = sys.path[1:]
        new_k = sys.modules.keys() - old_k
        for m in new_k:
            if m.partition('.')[0] == sub:
                del t.tracked[m]
                if m in t.dynamic_users:
                    del t.dynamic_users[m]
                del sys.modules[m]

        if hasattr(hook, 'after_folder'):
            hook.after_folder(base, sub)


    t.disable_tracking()

    if t.dynamic and getattr(hook, 'RECORD_DYNAMIC', False):
        print_with_timestamp(f"--- locations of dynamic imports")
        # TODO: allow whitelisting of expected sites
        #  1. trim down the stack trace up to the relevant function
        #  2. maybe only count number of occurrences of these, or hide them
        dedup_stack = set()
        whitelisted = 0
        is_whitelisted_dynamic_import = getattr(hook, 'is_whitelisted_dynamic_import', None)
        for dyn_stack in t.dynamic:
            if is_whitelisted_dynamic_import and is_whitelisted_dynamic_import(dyn_stack):
                whitelisted += 1
                continue
            as_tuple = tuple((f.filename, f.lineno) for f in dyn_stack)
            if as_tuple in dedup_stack:
                continue
            dedup_stack.add(as_tuple)
            print("---")
            traceback.print_list(dyn_stack, file=sys.stdout)

    # validate global namespace once all packages have been processed
    print_with_timestamp(f"--- comparing code import graphs")
    files_with_missing_imports += validate(
        t.tracked,
        g,
        filter_fn=lambda module: module.partition('.')[0] in hook.GLOBAL_NAMESPACES
    )

    print_with_timestamp(f"--- validation result")
    if error_count + files_with_missing_imports == 0:
        print(f"The rust module graph can be trusted")
        sys.exit(0)
    else:
        if files_with_missing_imports:
            print(f"The rust module graph is missing some imports")
            print("You may need to make some dynamic imports explicit")
        if error_count:
            print(f"Errors prevented validation of the rust module graph")
            print("Fix them and try again...")
        sys.exit(1)

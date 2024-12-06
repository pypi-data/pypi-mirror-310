import threading
import time
from typing import TypeVar
import types
import enum
import omp4py.core as core
import omp4py.context as context
import omp4py.error as error

T = TypeVar("T")


def omp(arg: str | T) -> context.DummyCtx | T:
    """
    The omp function imitates the behavior of the #pragma omp directive in OpenMP.
    This directive is used to provide hints and directives to the OpenMP compiler for parallel
    execution of code blocks. It allows controlling various aspects of parallel execution,
    such as loop parallelization, thread synchronization, and data sharing among threads.

    :param arg: The OpenMP directive to be used, such as "parallel", "for", "barrier", "critical", "atomic", etc.
                Additional clauses can be added as needed.
    :return: The OpenMP code when it is used as decorator.

    Usage:
    #pragma omp directive [clause [, clause] ...] -> with omp("directive [clause [, clause] ...]"):

    Note:
    OpenMP calls must be placed inside a function or a class decorated with the omp decorator in order to have
    an effect.

    Example:
    @omp
    def f():
        with omp("parallel"):
            print(omp_get_thread_num())
    """
    try:
        if isinstance(arg, str):
            # If the decorator is not used, the omp function will be executed within the with block. To avoid errors,
            # it requires an object with __enter__ and __exit__ methods to create a dummy block.
            return context.DummyCtx()
        elif isinstance(arg, (type, types.FunctionType, types.MethodType)):  # Classes, functions, or object methods
            return core.omp_parse(arg)
        else:
            raise error.OmpError("expected directive string, class, function or object method")
    except error.OmpSyntaxError as ex:
        # Hide the internal ast stack
        raise ex.__class__(ex) from None


openmp = omp


def omp_debug(dump_source=None, dump_ast=None, dump_prefix=None, dump_dir=None):
    """
    Enable/disable omp source code or omp source tree dump.

    :param dump_source: If true omp source code is dumped in the dump_dir
    :param dump_ast: If true omp source tree is dumped in the dump_dir
    :param dump_prefix: Prefix used to create the name of the dump
    :param dump_dir: Change the target dump_dir
    """
    if dump_source is not None:
        core._dump_source = dump_source

    if dump_ast is not None:
        core._dump_ast = dump_ast

    if dump_prefix is not None:
        core._dump_prefix = dump_prefix

    if dump_dir is not None:
        core._dump_dir = dump_dir


# documentation: https://rookiehpc.org/openmp/docs/ and https://www.openmp.org/

def omp_set_num_threads(num_threads: int):
    """
    The function omp_set_num_threads is one of the three ways to specify the number of threads to use when creating
    parallel regions. The other two are the environment variable OMP_NUM_THREADS and the num_threads clause. The
    function omp_set_num_threads specifies, during execution, the number of threads to use from now when creating
    parallel regions. It overwrites, for upcoming parallel regions only, the value that the environment variables
    OMP_NUM_THREADS defined. It can be overwritten, for a specific parallel region only, by the num_threads clause.
    If none of the environment variable OMP_NUM_THREADS, the function omp_set_num_threads or the num_threads clause
    is used, the number of threads used when creating parallel regions is implementation defined. To see the number of
    threads used when creating a parallel region, one can call omp_get_num_threads inside the parallel region created.

    :param num_threads: The number of threads to use from now on when creating a parallel region.
    """
    core._omp_context.max_num_threads = num_threads


def omp_get_num_threads() -> int:
    """
    The function omp_get_num_threads returns the number of threads in the current OpenMP region. If this function is
    called outside a parallel region, only the master thread is present hence the value returned is 1. Although
    spellings are close, do not confuse this function with omp_get_thread_num.

    :return: The number of threads contained in the current region.
    """
    return core._omp_context.current_level().num_threads


def omp_get_max_threads() -> int:
    """
    The function omp_get_num_threads returns the number of threads in the current OpenMP region. If this function is
    called outside a parallel region, only the master thread is present hence the value returned is 1. Although
    spellings are close, do not confuse this function with omp_get_thread_num.

    :return: The number of threads contained in the current region.
    """
    return core._omp_context.max_num_threads


def omp_get_thread_num() -> int:
    """
    The function omp_get_thread_num returns the identifier of the calling thread. Although spellings are close, do not
    confuse this function with omp_get_num_threads.

    :return: The identifier of the calling thread.
    """
    return core._omp_context.current_level().thread_num


def omp_get_num_procs() -> int:
    """
    The function omp_get_num_procs returns the number of available processors in the system. This function provides
    information about the number of processors that are available for concurrent execution. It can be used to determine
    the system's capacity for parallel processing.

    :return: The number of available processors in the system.
    """
    return core._omp_context.num_procs()


def omp_in_parallel() -> bool:
    """
    The function omp_in_parallel determines whether the current thread is executing inside an OpenMP parallel region.
    This function returns a boolean value indicating whether the current thread is executing within a parallel region
    controlled by OpenMP. It is useful for determining if the current execution context is parallelized, allowing
    conditional execution of parallel-aware code.

    :return: True if the current thread is executing inside a parallel region, otherwise False.
    """
    return core._omp_context.current_level().active_level > 0


def omp_set_dynamic(dynamic_threads: bool):
    """
    The function omp_set_dynamic is one of the two ways to enable / disable dynamic adjustment. The other one is the
    environment variable OMP_DYNAMIC. Dynamic adjustment is the feature that allows the runtime system to provide fewer
    threads than requested for a parallel region. In codes with recursively nested parallel regions for instance, the
    total number of threads to spawn may generate a high oversubscription, dynamic adjustment allows the runtime
    system to handle that growth. One can check if dynamic adjustment is enabled or disabled using the function
    omp_get_dynamic.

    :param dynamic_threads: If it evaluates to true dynamic adjustment is allowed, not allowed where appropriate.
    """
    if dynamic_threads:
        raise error.OmpError("dynamic threads not supported by current implementation")


def omp_get_dynamic() -> bool:
    """
    The function omp_get_dynamic indicates whether dynamic adjustment is enabled. Dynamic adjustment is the feature
    that allows the runtime system to provide fewer threads than requested for a parallel region. In codes with
    recursively nested parallel regions for instance, the total number of threads to spawn may generate a high
    oversubscription, dynamic adjustment allows the runtime system to handle that growth. It can be enabled or
    disabled using the function omp_set_dynamic.

    :return: True if dynamic adjustment is enabled, otherwise False.
    """
    return False


def omp_set_nested(nested: bool):
    """
    The function omp_set_nested toggles the nested parallelism feature in OpenMP, allowing or disallowing the creation
    of parallel regions within other parallel regions. When nested parallelism is enabled, parallel regions within
    existing parallel regions can create additional parallel threads. If nested parallelism is disabled, parallel
    regions within other parallel regions are constrained to only utilize the existing parallel threads.

    :param nested: If True, enables nested parallelism. If False, disables nested parallelism.
    """
    core._omp_context.nested = nested
    if not nested:
        core._omp_context.max_active_levels = 1


def omp_get_nested() -> bool:
    """
    The omp_get_nested function returns a boolean value indicating whether nested parallelism is currently enabled or
    disabled in the OpenMP environment. Nested parallelism allows the creation of parallel regions within other
    parallel regions, potentially leading to increased concurrency.

    :return: True if nested parallelism is enabled, False otherwise.
    """
    return core._omp_context.nested


class omp_sched_t(enum.Enum):
    omp_sched_static = "static"
    omp_sched_dynamic = "dynamic"
    omp_sched_guided = "guided"
    omp_sched_auto = "auto"


omp_sched_static: omp_sched_t = omp_sched_t.omp_sched_static
omp_sched_dynamic: omp_sched_t = omp_sched_t.omp_sched_dynamic
omp_sched_guided: omp_sched_t = omp_sched_t.omp_sched_guided
omp_sched_auto: omp_sched_t = omp_sched_t.omp_sched_auto


def omp_set_schedule(kind: omp_sched_t, chunk_size: int = -1):
    """
    The function omp_set_schedule is one of the two ways to specify the schedule to apply when a runtime clause is
    encountered during execution. The other one is the environment variable OMP_SCHEDULE. The expected format for the
    schedule is: the kind of scheduling (static, dynamic, auto or guided). Optionally, the kind can also be succeeded
    by a comma and the chunk size. To summarise, it can be represented as follows: "kind[,chunksize]".
    Please note that if this format is not respected, the behaviour is implementation defined. It is also worth
    mentioning that implementation specific schedules can be used in the omp_set_schedule function, but they cannot be
    used in the environment variable OMP_SCHEDULE. If none of the environment variable OMP_SCHEDULE or the function
    omp_set_schedule is used, the schedule to apply when a runtime clause is encountered during execution is
    implementation defined. To see the schedule to apply when the runtime clause is encountered, one can call
    omp_get_schedule.

    :param kind: The OpenMP scheduling kind to use, possible values are omp_sched_static, omp_sched_dynamic,
                    omp_sched_guided and omp_sched_auto.
    :param chunk_size: The number of iterations that make a chunk. If this number is less than 1, the defaulted chunk
                    size is used. For the auto schedule, this argument has no meaning.
    """
    core._omp_context.schedule = kind.value
    core._omp_context.chunk_size = chunk_size


def omp_get_schedule() -> (omp_sched_t, int):
    """
    The function omp_get_schedule returns the kind of scheduling and the chunk size used when a runtime schedule is
    encountered. Conversely, the schedule to apply when a runtime schedule is encountered can be set with OMP_SCHEDULE
    and omp_set_schedule.

    :return: (kind, chunk_size)
        kind : The variable in which store the OpenMP scheduling kind to use when a runtime schedule is encountered.
        chunk_size : The variable in which store the number of iterations that make a chunk.
    """
    return (omp_sched_t[core._omp_context.schedule], core._omp_context.chunk_size)


def omp_get_thread_limit() -> int:
    """
    This function returns the maximum number of threads that can be used in a parallel region, representing the upper
    limit on thread creation within parallel constructs. The value is determined by the thread-limit-var internal
    control variable, which can be set with the OMP_THREAD_LIMIT environment variable.

    :return: The maximum number of OpenMP threads available to the program.
    """
    return core._omp_context.thread_limit


def omp_set_max_active_levels(max_levels: int):
    """
    The omp_set_max_active_levels function sets the maximum number of nested parallel regions that can be active at any
    time. This function allows controlling the level of nesting in OpenMP parallel regions. However, this function has
    no effect if nested parallelism is not enabled.

    :param max_levels: The maximum number of active nested parallel regions to set.
    """
    if omp_get_nested() and max_levels > 0:
        core._omp_context.max_active_levels = max_levels


def omp_get_max_active_levels() -> int:
    """
    The omp_get_max_active_levels function returns the maximum number of nested parallel regions that can be active at
    any time. This function provides information about the level of nesting allowed in OpenMP parallel regions.

    :return: The maximum number of active nested parallel regions.
    """
    return core._omp_context.max_active_levels


def omp_get_level() -> int:
    """
    The omp_get_level function returns the level of nested parallelism at the current execution point. This function
    indicates how deeply nested the program is within parallel regions, counting both active and inactive parallel
    regions.

    :return: The level of nested parallelism.
    """
    return core._omp_context.current_level().level


def omp_get_ancestor_thread_num(level: int):
    """
    The omp_get_ancestor_thread_num function returns the thread number of the calling thread's
    ancestor at the specified level of nested parallelism. Ancestor threads are threads that
    are higher in the nesting hierarchy than the current thread.

    :param level: The level of nested parallelism to query for ancestor thread number.
    :return: The thread number of the calling thread's ancestor at the specified level. If the specified level does not
                exist, -1 is returned.
    """
    if level < 0 or level > omp_get_level() - 1:
        return -1
    return core._omp_context.get_level(level + 1).thread_num


def omp_get_team_size(level: int):
    """
    The omp_get_team_size function returns the number of threads in the team associated with
    the specified level of nested parallelism. A team is a group of threads executing in a
    parallel region.

    :param level: The level of nested parallelism to query for team size.
    :return: The number of threads in the team associated with the specified level. If the specified level does not
                exist, -1 is returned.
    """
    if level < 0 or level > omp_get_level() - 1:
        return -1
    return core._omp_context.get_level(level + 1).num_threads


def omp_get_active_level():
    """
    The omp_get_active_level function returns the level of nested parallelism at the current
    execution point. This function indicates how deeply nested the program is within active
    parallel regions.

    :return: The level of active parallelism.
    """
    return core._omp_context.current_level().active_level


def omp_init_lock() -> threading.Lock:
    """
    The omp_init_lock function initializes a lock and associates it with the lock variable passed in as a parameter.
    After the call to omp_init_lock, the initial state of the lock variable is unlocked.

    :return: The lock
    """
    return threading.Lock()


def omp_init_nest_lock() -> threading.RLock:
    """
    The omp_init_nest_lock function allows you to initialize a nestable lock and associate it with the lock variable
    you specify. The initial state of the lock variable is unlocked.

    :return: The nestable lock
    """
    return threading.RLock()


def omp_destroy_lock(lock: threading.Lock):
    """
    The omp_destroy_lock function should disassociate a given lock variable from all locks but in python it is not
    necessary.

    :param lock: The lock
    """
    pass


def omp_destroy_nest_lock(lock: threading.RLock):
    """
    The omp_destroy_lock function should disassociate a given nestable lock variable from all locks but in python it is
    not necessary.

    :param lock: The nestable lock
    """
    pass


def omp_set_lock(lock: threading.Lock):
    """
    The omp_set_lock function forces the calling task region to wait until the specified lock is available before
    executing subsequent instructions. The calling task region is given ownership of the lock when it becomes available.

    In python is preferable and safer use:
         with lock:
            ....

    :param lock: the lock
    :return:
    """
    lock.acquire()


def omp_set_nest_lock(lock: threading.RLock):
    """
    The omp_set_nest_lock function allows you to set a nestable lock. The task region executing the function will
     wait until the lock becomes available and then set that lock, incrementing the nesting count. A nestable lock is
     available if it is owned by the task region executing the subroutine, or is unlocked.

    In python is preferable and safer use:
         with lock:
            ....

    :param lock: The nestable lock
    """
    lock.acquire()


def omp_unset_lock(lock: threading.Lock):
    """
    The omp_unset_lock function causes the executing task region to release ownership of the specified lock. The lock
    can then be set by another task region as required.

    :param lock: The lock
    """
    lock.release()


def omp_set_unnest_lock(lock: threading.RLock):
    """
    The omp_unset_nest_lock function allows you to release ownership of a nestable lock. The function decrements the
    nesting count and releases the associated task region from ownership of the nestable lock.

    :param lock: The nestable lock
    """
    lock.release()


def omp_test_lock(lock: threading.Lock) -> True:
    """
    The omp_test_lock function attempts to set the lock associated with the specified lock variable. It returns True if
    it was able to set the lock and False otherwise. In either case, the calling task region will continue to execute
    subsequent instructions in the program.

    :param lock: The lock
    :return: True if the function was able to set the lock. False otherwise.
    """
    return lock.acquire(blocking=False)


def omp_test_nest_lock(lock: threading.RLock) -> True:
    """
    The omp_test_nest_lock function allows you to attempt to set a lock using the same method as omp_set_nest_lock,
    but the executing task region does not wait for confirmation that the lock is available. If the lock is successfully
    set, the function will increment the nesting count and return the new nesting count. If the lock is unavailable the
    function returns False.

    :param lock:
    :return: True if the lock is successfully set; otherwise, it returns False.
    """
    return lock.acquire(blocking=False)


def omp_get_wtime() -> float:
    """
    The omp_get_wtime function returns a double precision value equal to the number of seconds since the initial value
    of the operating system real-time clock. The initial value is guaranteed not to change during execution of the
    program.

    The value returned by the omp_get_wtime function is not consistent across all threads in the team.

    :return: The number of seconds since the initial value of the operating system real-time clock.
    """
    return time.perf_counter()


def omp_get_wtick() -> float:
    """
    The omp_get_wtick function returns a double precision value equal to the number of seconds between consecutive clock
    ticks.

    :return: The number of seconds between consecutive ticks of the operating system real-time clock.
    """
    return time.get_clock_info('perf_counter').resolution

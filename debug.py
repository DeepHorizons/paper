
class ProfileContextManager(object):
    import cProfile

    def __enter__(self):
        self.profiler = ProfileContextManager.cProfile.Profile()
        self.profiler.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.profiler.disable()
        self.profiler.print_stats(1)
        self.profiler.clear()


class TimerContextManager(object):
    import time
    
    def __init__(self, lst=None):
        """lst is a list that it will append to"""
        self.timer = self.time.perf_counter
        self.lst = lst

    def __enter__(self):
        self.starttime = self.timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        stoptime = self.timer()
        runtime = stoptime - self.starttime
        print(runtime)
        self.lst.append(runtime) if self.lst is not None else None


def time_functions():
    """To get performance between data sets"""
    import timeit
    import statistics

    RUN_TIMES = 5

    class TestContextManager(list):
        def __init__(self):
            super().__init__()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.sort(key=lambda x: x[0])
            [print('{:<40} {:.2%}'.format(str(i), ((i[0]-self[0][0])/self[0][0]))) for i in self]

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100000
        ACCESS_NUMBER = 0
        print('list access vs dict access vs tuple; access best case; acess number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100000
        ACCESS_NUMBER = RANGE_NUMBER - 1
        print('list access vs dict access; access worst case; acess number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a.values()}', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a)', 'a = (i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple gen'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> list comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('[i for i in a.values()]', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> set comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i for i in a.values()}', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> dict comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a}', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a.values()}', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a}', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a}', 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> tuple comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a)', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a.values())', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a)', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a)', 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        print('list, dict, set, tuple -> combining; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a + b', 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a.update(b)', 'a = {{i: i for i in range({0})}}; b = {{i: i for i in range({0} + {0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a | b', 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('a + b', 'a = tuple(i for i in range({0})); b = tuple(i for i in range({0} + {0}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, set -> list combine to set; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('set(a + b)', 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a | b', 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = 0
        print('list, dict, set, tuple -> member in best case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))


    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = RANGE_NUMBER
        print('list, dict, set, tuple -> member in worst case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = RANGE_NUMBER
        print('list, dict, set, tuple -> member in worst case list converted to set; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in set(a)'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = 0
        print('list, dict, set, tuple -> combining and member in best case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in (a + b)'.format(ACCESS_NUMBER), 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a.update(b); {} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({0})}}; b = {{i: i for i in range({0} + {0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a.union(b)'.format(ACCESS_NUMBER), 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{} in (a + b)'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({0})); b = tuple(i for i in range({0} + {0}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = RANGE_NUMBER
        print('list, dict, set -> combining and member in worst case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in (a + b)'.format(ACCESS_NUMBER), 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a.update(b); {} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({0})}}; b = {{i: i for i in range({0} + {0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a.union(b)'.format(ACCESS_NUMBER), 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('{} in (a + b)'.format(ACCESS_NUMBER), 'a = tuple(i for i in range({0})); b = tuple(i for i in range({0} + {0}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        print('list, dict, set, tuple -> generator set; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        print('list, dict, set, tuple; creation -> generator set; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('a = tuple(i for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        ITTER_NUMBER = 100
        print('list, dict, set, tuple; single creation -> generator set; run times {}'.format(ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a = [0]', number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a = {0: 0}', number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a = {0}', number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('a = (0,)', number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        ITTER_NUMBER = 100
        CREATE_NUMBER = 100000
        print('list, dict, tuple; single creation and access -> generator set; create number {} run times {}'.format(CREATE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a = [{}]; a[0]'.format(CREATE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a = {{0: {}}}; a[0]'.format(CREATE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a = ({},); a[0]'.format(CREATE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> filter using type() is; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('[i for i in a if type(i) is int]', 'a = [i if (i%2) else str(i) for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a.values() if type(i) is int}', 'a = {{i: i if (i%2) else str(i) for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i for i in a if type(i) is int}', 'a = {{i if (i%2) else str(i) for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a if type(i) is int)', 'a = (i if (i%2) else str(i) for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple gen'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set, tuple -> filter using isinstance(); range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('[i for i in a if isinstance(i, int)]', 'a = [i if (i%2) else str(i) for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a.values() if isinstance(i, int)}', 'a = {{i: i if (i%2) else str(i) for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i for i in a if isinstance(i, int)}', 'a = {{i if (i%2) else str(i) for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))
        t.append((statistics.mean([timeit.timeit('tuple(i for i in a if isinstance(i, int))', 'a = (i if (i%2) else str(i) for i in range({}))'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'tuple gen'))

if __name__ == '__main__':
    time_functions()

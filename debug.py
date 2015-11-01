
class ProfileContextManager(object):
    import cProfile

    def __enter__(self):
        self.profiler = ProfileContextManager.cProfile.Profile()
        self.profiler.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.profiler.disable()
        self.profiler.print_stats()


class TimerContextManager(object):
    import time
    
    def __init__(self):
        self.timer = self.time.perf_counter

    def __enter__(self):
        self.starttime = self.timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        stoptime = self.timer() 
        print(stoptime - self.starttime)


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
        print('list access vs dict access; access best case; acess number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100000
        ACCESS_NUMBER = RANGE_NUMBER - 1
        print('list access vs dict access; access worst case; acess number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a[{}]'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set -> comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a.values()}', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set -> list comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('[i for i in a.values()]', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('[i for i in a]', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set -> set comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i for i in a.values()}', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i for i in a}', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set -> dict comprehension; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a}', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a.values()}', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{i: i for i in a}', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        print('list, dict, set -> combining; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('a + b', 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a.update(b)', 'a = {{i: i for i in range({0})}}; b = {{i: i for i in range({0} + {0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('a | b', 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 1000
        ITTER_NUMBER = 1000
        print('list, dict, set -> list combine to set; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('set(a + b)', 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a | b', 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = 0
        print('list, dict, set -> member in best case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = RANGE_NUMBER
        print('list, dict, set -> member in worst case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = RANGE_NUMBER
        print('list, dict, set -> member in worst case list converted to set; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in set(a)'.format(ACCESS_NUMBER), 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a'.format(ACCESS_NUMBER), 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = 0
        print('list, dict, set -> combining and member in best case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in (a + b)'.format(ACCESS_NUMBER), 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a.update(b); {} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({0})}}; b = {{i: i for i in range({0} + {0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a.union(b)'.format(ACCESS_NUMBER), 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        ACCESS_NUMBER = RANGE_NUMBER
        print('list, dict, set -> combining and member in worst case; access number {} range {} run times {}'.format(ACCESS_NUMBER, RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('{} in (a + b)'.format(ACCESS_NUMBER), 'a = [i for i in range({0})]; b = [i for i in range({0} + {0})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('a.update(b); {} in a'.format(ACCESS_NUMBER), 'a = {{i: i for i in range({0})}}; b = {{i: i for i in range({0} + {0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('{} in a.union(b)'.format(ACCESS_NUMBER), 'a = {{i for i in range({0})}}; b = {{i for i in range({0}+{0})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

    with TestContextManager() as t:
        RANGE_NUMBER = 10000
        ITTER_NUMBER = 100
        print('list, dict, set -> generator set; range {} run times {}'.format(RANGE_NUMBER, ITTER_NUMBER))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = [i for i in range({})]'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'list'))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = {{i: i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'dict'))
        t.append((statistics.mean([timeit.timeit('(i for i in a)', 'a = {{i for i in range({})}}'.format(RANGE_NUMBER), number=ITTER_NUMBER) for i in range(RUN_TIMES)]), 'set'))

if __name__ == '__main__':
    time_functions()

class Client:
    def __init__(self):
        self.scheduler_url = 'https://scheduler.bowenchiu.repl.co/api/map/'

    def map(self, f, lst, dic={}):
        for i in lst:
            print(f'f.__module__:{f.__module__}')
            print(f'f.__name__:{f.__name__}')
            print(f'scheduler_url:{self.scheduler_url},f:{f},i:{i},dic:{dic}')
            yield f(i, dic)

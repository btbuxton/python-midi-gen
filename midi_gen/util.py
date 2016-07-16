#Collection of Utils

class Loop(object):
    '''
    Given a consumer (func that returns True/False to continue and has a reset method) continually loop it
    '''
    def __init__(self, consumer):
        self._consumer = consumer
    
    def __call__(self, pulse):
        if not self._consumer(pulse):
            self._consumer.reset()
        return True
    
    def reset(self):
        pass
     
class Parallel(object):
    '''
    Parallelize the calls to several pulse consumers
    '''
    def __init__(self, *consumers):
        self._consumers = consumers
        self._to_reset = None
        
    def __call__(self, pulse):
        for each in self._consumers:
            if not each(pulse):
                self._to_reset = each
                return False
        return True
    
    def reset(self):
        if self._to_reset is None:
            return
        self._to_reset.reset()
        self._to_reset = None
    
class Chain(object):
    '''
    Chain several pulse consumer to run sequentially
    '''
    def __init__(self, *consumers):
        self._consumers = consumers
        self.reset()
        
    def __call__(self, pulse):
        if not self._current(pulse):
            try:
                self._current = next(self._iter)
            except StopIteration:
                return False
        return True
    
    def reset(self):
        for each in self._consumers:
            each.reset()
        self._iter = iter(self._consumers)
        self._current = next(self._iter)
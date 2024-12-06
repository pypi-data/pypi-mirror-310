
class LazyObject:
    def __init__(self):
        self._wrapped = None
        
    def _setup(self):
        raise NotImplementedError("Subclasses of LazyObject must implement _setup() method.")
    
    def __getattr__(self, name):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)

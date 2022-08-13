

import threading


class OffsetManager():
    #region Singleton Constructor
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
         
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(OffsetManager, cls).__new__(cls)
                    cls._instance.init()
        return cls._instance
    #endregion
    
    
    def init(self) -> None:
        self.list_of_offsets = []
    
    def get_all_offsets(self):
        return self.list_of_offsets    
    
    def create_offset(self, x, y, angle):
        self.list_of_offsets.append((x, y, angle))
        
    def delete_all_offsets(self):
        self.list_of_offsets = []
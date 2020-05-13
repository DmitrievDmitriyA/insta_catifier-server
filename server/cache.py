from cachetools import LFUCache
from threading import RLock
import server.dataBaseAdapter


# Simple thread-safe caching to speed things up a bit
# Possible issues:
# - Cache stores urls which could expire in 7 days (it means that it will be outdated after some time)
# but there is no logic that checks that
# At the moment it's not an issue because a relativly small cache size is used (It gets updated before 
# the issue could appear) 
# - If user updates account, but his account is stored in cache, the update will not be visible
# until cache is not cleared


lock = RLock()


class ExtendedLFUCache(LFUCache):

    def __getitem__(self, key):
        with lock:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        with lock:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        with lock:
            super().__delitem__(key)
            dataBaseAdapter.remove_results_from_bucket(key)

    def popitem(self):
        with lock:
            super().popitem()

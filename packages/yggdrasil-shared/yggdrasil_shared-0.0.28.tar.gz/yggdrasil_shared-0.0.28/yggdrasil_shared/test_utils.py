import threading


class StubRedisLock:
    """Stub implementation of walrus Lock class.

    Uses threading synchronization lock in order to imitate walrus lock implementation so it's not process safe.
    """
    def __init__(self, database, name, ttl, lock_id):
        self.name = name
        self.lock = threading.Lock()

    def acquire(self, block=True):
        return self.lock.acquire(blocking=block)

    def release(self):
        if not self.lock.locked():
            return False
        else:
            self.lock.release()
            return True

    def clear(self):
        try:
            return self.lock.release()
        except RuntimeError:
            return False

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.release():
            raise RuntimeError('Error releasing lock "%s".' % self.name)


class StubRedis:
    """Stub implementation of walrus redis client.

    The methods signatures are exactly the same as walrus.
    """
    def __init__(self):
        self.data = {}
        self.hashes = {}
        self.locks = {}

    def set(
            self, name, value,
            ex=None, px=None, nx=False, xx=False, keepttl=False
    ):
        self.data[name] = value

    def get(self, name):
        result = self.data.get(name)
        if isinstance(result, str):
            return result.encode()
        else:
            return result

    def Hash(self, key):
        if key not in self.hashes:
            self.hashes[key] = {}

        return self.hashes[key]

    def delete(self, *names):
        for name in names:
            if name in self.data:
                del self.data[name]
            if name in self.hashes:
                del self.hashes[name]

    def lock(self, name, ttl=None, lock_id=None):
        if name not in self.locks:
            self.locks[name] = StubRedisLock(None, name, ttl, lock_id)

        return self.locks[name]

    def __getitem__(self, name):
        result = self.get(name)
        if result is None:
            raise KeyError
        else:
            return result

    def __setitem__(self, name, value):
        self.set(name, value)

    def __delitem__(self, name):
        self.delete(name)

    def __contains__(self, *names):
        """

        The behaviour is redis compatible.
        """
        existence_count = 0
        for name in names:
            if name in self.data:
                existence_count += 1
        return existence_count

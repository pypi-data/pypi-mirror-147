import walrus
from nameko.extensions import DependencyProvider


class MemoryStore(DependencyProvider):
    """Dependency provider for redis."""

    def __init__(self):
        self.client = None

    def setup(self):
        self.config = self.container.config['REDIS']

    def start(self):
        self.client = walrus.Database(**self.config)

    def stop(self):
        self.client = None

    def kill(self):
        self.client = None

    def get_dependency(self, worker_ctx):
        return self.client

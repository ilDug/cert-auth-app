from core.config import Settings
from core.paths import PkiPaths


class Architect:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths

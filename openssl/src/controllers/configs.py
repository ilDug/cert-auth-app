from core.paths import PkiPaths
from core.config import Settings


class ConfigController:
    def __init__(self, cnf: Settings, paths: PkiPaths):
        self.cnf = cnf
        self.paths = paths


    def compile_root_config(self):
        # Implement the logic to compile the root configuration starting from a template
        template_path = self.paths.CONFIG_ROOT
        config_path = self.paths.ROOT_CONF
        
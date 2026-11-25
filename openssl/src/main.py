from core.config import get_settings
from core.paths import get_settings as get_paths
from controllers.installer import Installer
from controllers.ca import RootCAController
from controllers.configs import ConfigController

def main():
    settings = get_settings()
    paths = get_paths()
    installer = Installer(settings, paths)
    installer.cleanup()
    installer.scaffolding()
    installer.db_files()
    print("Hello from openssl!")

    config = ConfigController(settings, paths)
    config.compile_root_config(
        country="IT",
        state="Lombardy",
        locality="Milan",
        organization="DagTech",
        organizational_unit="IT",
        common_name="DagCA",
    )

if __name__ == "__main__":
    main()

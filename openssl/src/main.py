from core.config import get_settings
from core.paths import get_settings as get_paths
from controllers.installer import Installer

def main():
    settings = get_settings()
    paths = get_paths()
    installer = Installer(settings, paths)
    installer.cleanup()
    installer.scaffolding()
    installer.db_files()
    print("Hello from openssl!")


if __name__ == "__main__":
    main()

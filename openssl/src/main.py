from core.config import get_settings
from core.paths import get_settings as get_paths
from controllers.installer import Installer
from controllers.builder import RootCABuilder
from controllers.cnf import ConfigController
from models.config_model import RootCertificateConfigModel

def main():
    settings = get_settings()
    paths = get_paths()
    # installer = Installer(settings, paths)
    # installer.cleanup()
    # installer.scaffolding()
    # installer.db_files()
    # print("Hello from openssl!")

    # config = ConfigController(settings, paths)
    # config.compile_root_config(RootCertificateConfigModel(
    #     root_ca_dir=str(paths.ROOT_CA),
    #     country="IT",
    #     state="Lombardy",
    #     locality="Milan",
    #     organization="DagTech",
    #     organizational_unit="IT",
    #     common_name="DagCA",
    # ))

    root_ca = RootCABuilder(settings, paths)
    # root_ca.create_passphrase()
    # root_ca.initialize_private_key()
    # root_ca.generate_certificate()
    root_ca.show_certificate(pem=False)
    root_ca.display_privatekey_details()
    root_ca.show_publickey()

if __name__ == "__main__":
    main()

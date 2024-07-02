from controllers import Installer


def install():
    """genera tutta l'infrastruttira della PKI compreso il certificato root"""
    installer = Installer()
    installer.clean_structure()
    installer.scaffolding()

    print("genera una passprhase per la CA")
    installer.generate_passphrase()

    print("genera la chiave privata CA")
    installer.create_ca_key()

    print("genera il certificato CA")
    installer.create_ca_crt()

    print("verifica il certificato")
    installer.verify_ca_crt()

    print("ottinene e salva lachiave pubblica CA")
    installer.generate_public_key()

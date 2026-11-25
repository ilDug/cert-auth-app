from core.config import get_settings

def main():
    settings = get_settings()
    print("Hello from openssl!")

    folder = settings.PKI
    for item in folder.iterdir():
        print(item)


if __name__ == "__main__":
    main()

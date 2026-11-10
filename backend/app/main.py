from core .config import settings


if __name__ == "__main__":
    print("Hello from backend!")
    print(f"Settings: {list(settings.LIB.glob('**/*'))}")


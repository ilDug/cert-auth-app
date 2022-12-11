import uvicorn
from config import MODE


def main():
    if MODE == "DEVELOPMENT":
        print("il Server si avvia in modalità DEVELOPMENT")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

    if MODE == "PRODUCTION":
        print("il Server si avvia in modalità PRODUCTION")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)

    else:
        print(
            "ERROR: nessuna modalità di run (PRODUCTIOM/DEVELOPMENT) è stata definita nella variabili d'ambiente"
        )


if __name__ == "__main__":
    print("let get started MAIN")
    main()

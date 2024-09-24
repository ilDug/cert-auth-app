import uvicorn
from os import environ as env


if __name__ == "__main__":
    match env["MODE"]:
        case "DEVELOPMENT":
            print("il Server si avvia in modalità DEVELOPMENT")
            uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

        case "PRODUCTION":
            print("il Server si avvia in modalità PRODUCTION")
            uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)

        case _:
            print(
                "ERROR: nessuna modalità di run (PRODUCTIOM/DEVELOPMENT) è stata definita nella variabili d'ambiente"
            )

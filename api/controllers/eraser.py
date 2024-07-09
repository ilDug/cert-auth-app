from fastapi import HTTPException
from core.config import (
    PKI_PATH,
    PKI_DB,
    KEYS_PATH,
    REQS_PATH,
    CONFIGS_PATH,
    CERTS_PATH,
    PUBLIC_PATH,
)


class Eraser:

    def certificate(self, subject: str) -> bool:
        """elimina il certificato che ha il nome subject"""
        if self._is_root(subject):
            raise HTTPException(400, "Non è possibile eliminare il certificato root")

        id = self._get_id(subject)
        if not id:
            raise HTTPException(404, "Certificato non trovato")

        self._remove_from_db(subject)

        if not self._delete_files(subject, id):
            raise HTTPException(500, "Errore durante l'eliminazione dei file")

        return True

    def _delete_files(self, subject: str, id: str) -> bool:
        """elimina i file associati al certificato con nome subject"""
        paths = [
            KEYS_PATH,
            REQS_PATH,
            CONFIGS_PATH,
            CERTS_PATH,
            PUBLIC_PATH,
        ]  # lista dei path da controllare

        # per ogni path, per ogni file, se il nome del certificato è presente nel nome del file, elimina il file
        try:
            for path in paths:
                for file in path.iterdir():
                    if subject in file.name:
                        file.unlink()
            # nella cartella newcerts, elimina tutti i file con l'id del certificato
            for file in (PKI_PATH / "newcerts").iterdir():
                if id in file.name:
                    file.unlink()
            return True
        except Exception as e:
            print(e)
            return False

    def _get_id(self, subject: str) -> str:
        """restituisce l'ID del certificato con nome subject"""
        with PKI_DB.open("r") as db:
            for line in db:
                if subject in line:
                    return line.split("\t")[3]

    def _remove_from_db(self, subject: str):
        """rimuove il certificato dal database"""
        # find a line in a file and remove it
        with PKI_DB.open("r") as db:
            lines = db.readlines()  # read all lines
        with PKI_DB.open("w") as db:
            for line in lines:
                if subject not in line:  # skip the line to remove
                    db.write(line)

    def _is_root(self, subject: str) -> bool:
        """verifica se il certificato è root"""
        return subject == "ca" or subject == "_passphrase"

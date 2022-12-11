import os
from pathlib import Path
import subprocess

from .installer import Installer
import typer
from core.settings import CA_KEY_PATH, PASSPRHASE_PATH, CA_CRT_PATH, IMPORT_PATH


class Importer(Installer):
    def __init__(self) -> None:
        super().__init__()

        # controlla che esista la cartella di importaizone e che contanga i file
        if not IMPORT_PATH.exists() or not any(IMPORT_PATH.iterdir()):
            raise typer.Exit(
                "la cartella di importazione '/import' non contiene i file necessari,  caricare nella cartelal il certificato (.crt) e la chiave privata (.key)"
            )

    def import_ca(self):
        crt = self.import_crt()
        key = self.import_key()

        if crt and key:
            CA_KEY_PATH.write_text(key.read_text())
            CA_CRT_PATH.write_text(crt.read_text())
            self.register_passphrase()
        else:
            typer.Exit("non sono stati trovati i file necessari all'importazione")

    def import_crt(self) -> Path:
        for file in IMPORT_PATH.iterdir():
            if file.is_file() and file.suffix == ".crt":
                return file

    def import_key(self) -> Path:
        for file in IMPORT_PATH.iterdir():
            if file.is_file() and file.suffix == ".key":
                return file

    def register_passphrase(self):
        passphrase = typer.prompt("inserire la passphrase")
        PASSPRHASE_PATH.write_text(passphrase)
        PASSPRHASE_PATH.chmod(400)

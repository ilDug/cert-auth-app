from typing import Annotated

from controllers import Importer, Installer, PKIController
from core.config import AppConfig
from core.install import install
from core.utils import remove_tmp_file
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, UploadFile
from fastapi.responses import FileResponse
from models import RootPackage

router = APIRouter(tags=["import"])


@router.delete("/pki/reset")
async def reset_pki(cnf: AppConfig):
    pki = Installer(cnf)
    pki.clean_structure()
    print("PKI directory creation...")
    install()
    return True


@router.get("/pki/export")
async def export_pki(background_tasks: BackgroundTasks, cnf: AppConfig):
    pki = PKIController(cnf)
    pathfile = pki.export()
    filename = pathfile.name
    background_tasks.add_task(remove_tmp_file, pathfile)
    return FileResponse(pathfile, media_type="application/zip", filename=filename)


@router.get("/pki/download-root")
async def download_root(background_tasks: BackgroundTasks, cnf: AppConfig):
    pki = PKIController(cnf)
    pathfile = pki.download_ca_root()
    filename = pathfile.name
    background_tasks.add_task(remove_tmp_file, pathfile)
    return FileResponse(pathfile, media_type="application/zip", filename=filename)


@router.post("/pki/import/archive")
async def import_pki_zip(file: UploadFile, cnf: AppConfig):
    if file.content_type not in ["application/zip", "application/zip-compressed", "application/x-zip-compressed"]:
        raise HTTPException(400, "il file deve essere un archivio zip")

    importer = Importer(cnf)
    importer.clean_structure()
    return await importer.extract_pki(file)


@router.post("/pki/import/root")
async def import_root(
    package: Annotated[RootPackage, Body(...)], cnf: AppConfig
) -> bool:
    """genera tutta l'infrastruttira della PKI importando la chiave ed il certificato root. Eventuali strutture esistenti verranno cancellate"""
    crt = package.crt
    key = package.key
    passphrase = package.passphrase

    importer = Importer(cnf)
    importer.clean_structure()
    importer.scaffolding()

    print("importa i files")
    await importer.import_root(crt, key, passphrase)

    print("ottinene e salva la chiave pubblica CA")
    importer.generate_public_key()

    print("verifica il certificato")
    importer.verify_ca_crt()

    return True

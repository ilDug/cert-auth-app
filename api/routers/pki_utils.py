from pathlib import Path
from fastapi import APIRouter, Body, BackgroundTasks, Form, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from controllers import Installer, PKIController, Importer
from core.install import install
from core.utils.remove_tmp_file import remove_tmp_file
from core.models import RootPackage

router = APIRouter(tags=["import"])


@router.delete("/pki/reset")
async def reset_pki():
    pki = Installer()
    pki.clean_structure()
    print("PKI directory creation...")
    install()
    return True


@router.get("/pki/export")
async def export_pki(background_tasks: BackgroundTasks):
    pki = PKIController()
    pathfile = pki.export()
    filename = pathfile.name
    background_tasks.add_task(remove_tmp_file, pathfile)
    return FileResponse(pathfile, media_type="application/zip", filename=filename)


@router.get("/pki/download-root")
async def download_root(background_tasks: BackgroundTasks):
    pki = PKIController()
    pathfile = pki.download_ca_root()
    filename = pathfile.name
    background_tasks.add_task(remove_tmp_file, pathfile)
    return FileResponse(pathfile, media_type="application/zip", filename=filename)


@router.post("/pki/import/archive")
async def import_pki_zip(file: UploadFile):
    if file.content_type != "application/zip":
        raise HTTPException(400, "il file deve essere un archivio zip")

    importer = Importer()
    importer.clean_structure()
    return await importer.extract_pki(file)


@router.post("/pki/import/root")
async def import_root(package: RootPackage = Body(...)):
    """genera tutta l'infrastruttira della PKI importando la chiave ed il certificato root. Eventuali strutture esistenti verranno cancellate"""
    crt = package.crt
    key = package.key
    passphrase = package.passphrase

    importer = Importer()
    importer.clean_structure()
    importer.scaffolding()

    print("importa i files")
    await importer.import_root(crt, key, passphrase)

    print("ottinene e salva la chiave pubblica CA")
    importer.generate_public_key()

    print("verifica il certificato")
    importer.verify_ca_crt()

    return True

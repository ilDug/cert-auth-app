from fastapi import Request


async def pki_middleware(request: Request, call_next):
    """controlla che sia istanziata una pki"""
    response = await call_next(request)
    return response

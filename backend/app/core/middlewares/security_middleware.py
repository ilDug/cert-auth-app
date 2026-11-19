from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

SECURITY_COOKIE_KEY = "X-Cert-Auth-Token"


class SecurityTokenMiddleware(BaseHTTPMiddleware):
    """Protegge le richieste API con un token di sicurezza gestito tramite cookie.

    Per i percorsi che iniziano con ``/api``, accetta solo richieste con
    ``Sec-Fetch-Site: same-origin`` e rifiuta con HTTP 401 se il token atteso
    non è configurato, se il cookie ``X-Cert-Auth-Token`` manca o se il suo
    valore non coincide con il token atteso.

    Le richieste non API non vengono sottoposte a questi controlli.

    Se i controlli hanno esito positivo (o il percorso non è API), inoltra la
    richiesta al gestore successivo. Quando un token è configurato, aggiunge
    alla risposta il cookie con tale valore, limitato a ``/api`` e impostato
    con ``SameSite=Strict``, ``Secure`` e ``HttpOnly``.
    """
    context_endpoint: str = "/api"

    def __init__(self, app: ASGIApp, token: str | None):
        super().__init__(app)
        self.token = token

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        path = request.url.path

        # Se non viene specificato un token di sicurezza, non applicare il middleware alle richieste API
        if self.token is None:
            return await call_next(request)

        if path.startswith(self.context_endpoint):

            # Reject requests that are not same-origin
            if request.headers.get("sec-fetch-site") != "same-origin":
                return JSONResponse(
                    status_code=401,
                    content={"error": "Richiesta non autorizzata - origine non valida"},
                    headers={
                        "X-Error": "Richiesta non autorizzata - origine non valida"
                    },
                )

            # Reject requests if the security token is not set
            if not self.token:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "Richiesta non autorizzata - token non configurato"
                    },
                    headers={
                        "X-Error": "Richiesta non autorizzata - token non configurato"
                    },
                )

            # Reject requests if the security cookie is not present
            if SECURITY_COOKIE_KEY not in request.cookies:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Richiesta non autorizzata - cookie mancante"},
                    headers={"X-Error": "Richiesta non autorizzata - cookie mancante"},
                )

            # Check if the security token in the cookie matches the expected token
            token = request.cookies[SECURITY_COOKIE_KEY]
            if token != self.token:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Richiesta non autorizzata - token non valido"},
                    headers={"X-Error": "Richiesta non autorizzata - token non valido"},
                )

        response = await call_next(request)
        if self.token:
            response.set_cookie(
                key=SECURITY_COOKIE_KEY,
                value=self.token,
                samesite="Strict",
                secure=True,
                httponly=True,
                path=self.context_endpoint,
            )
        return response

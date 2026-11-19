# comunicazione privata tra backend e frontend                                                                       
                                                                                                                      
Creare un cookie token  `SECURITY_TOKEN` iniziale che permetta solo al client di accedere alle API del backend. Questo token deve essere generato in modo sicuro durante la creazione del container per garantire la sicurezza della comunicazione.               
                                                                                                                    
Questo serve ad evitare che le chiamate alle API del backend possano essere effettuate da utenti non autorizzati o da client non validi. Il token deve essere inviato dal client al backend in ogni richiesta, e il backend deve verificarne la validità prima di rispondere alla richiesta.                                                
                                                                                                                    
Il token deve essere inviato tramite header HTTP, ad esempio utilizzando l'header "X-Cert-Auth-Token". In questo modo, il backend può facilmente estrarre il token dalla richiesta e verificarne la validità.                              

Il cookie deve essere generato all'avvio del container e condiviso sia dal backend che dal frontend. In questo modo, entrambi i componenti possono utilizzare lo stesso token per autenticarsi e comunicare in modo sicuro. 

## logica di verifica del token

Il backend deve controllare la presenza del token di sicurezza in ogni richiesta. Se il token non è presente o non è valido, il backend deve rifiutare la richiesta. Questo garantisce che solo i client autorizzati possano accedere alle API del backend.

Per fare questa verifica utilizzare un middleware di FastAPI.

Il middleware deve estrarre il token dall'header della richiesta e confrontarlo con il token di sicurezza generato all'avvio del container. Se il token non corrisponde, il middleware deve bloccare la richiesta e restituire un errore di autorizzazione.

In FastAPI, questo può essere implementato utilizzando la funzione `@app.middleware("http")` per intercettare tutte le richieste in arrivo, verificare il token e decidere se consentire o meno l'accesso alle API.

Esempio di implementazione:

```python
from fastapi import Request, HTTPException
from core.config import settings

@app.middleware("http")
async def check_security_token(request: Request, call_next):
    token = request.headers.get("X-Cert-Auth-Token")
    if token != settings.SECURITY_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await call_next(request)
    return response
```

## Invio iniziale del token

Il token di sicurezza deve essere inviato dal client al backend in ogni richiesta. Questo può essere fatto impostando l'header HTTP "X-Cert-Auth-Token" con il valore del token generato all'avvio del container. In questo modo, il backend può verificare la validità del token prima di rispondere alla richiesta. 

Il client deve ottenere il token dal backend all'avvio o dalla configurazione del container, e poi includerlo in ogni richiesta successiva tramite l'header "X-Cert-Auth-Token".

In questo modo, il backend può garantire che solo i client autorizzati possano accedere alle API, migliorando la sicurezza complessiva dell'applicazione. Il Frontend non deve mai memorizzare il token in modo permanente, ma deve inviarlo in ogni richiesta al backend tramite l'header "X-Cert-Auth-Token".

Il set del cookie avviene con una prima richiesta dei file statici del frontend, che permette al backend di inviare il token di sicurezza al client in modo sicuro. Successivamente, il client deve includere il token in tutte le richieste successive tramite l'header "X-Cert-Auth-Token".
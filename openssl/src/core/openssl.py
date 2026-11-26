"""OpenSSL command definitions for passphrase generation."""

from icecream import ic


# Command parser for OpenSSL commands with placeholders.
def parse_cmd(cmd: str, values: dict[str, str]) -> list[str]:
    # ic(cmd.format(**values))
    return cmd.replace(" ", "÷").format(**values).split("÷")


# openssl rand -base64 32 | tr -d '/.+'
PASSPHRASE = "openssl rand -base64 32"

PRIVATEKEY_GEN = "openssl genpkey -algorithm RSA -aes-256-cbc -pass pass:{passphrase} -pkeyopt rsa_keygen_bits:{bits} -out {output}"

# mostra i dettagli del della chiave privata
PRIVATEKEY_SHOW = (
    "openssl pkey -in {keypath} -noout -text -passin file:{passphrasepath}"
)

# mostra la chiave pubblica a partire dalla chiave privata
# PUBLICKEY_FROM_KEY_SHOW = (
#     "openssl pkey -in {keypath} -pubout -noout -text -passin file:{passphrasepath}"
# )

# mostra la chiave pubblica in formato PEM a partire dal certificato
PUBLICKEY_FROM_CRT_SHOW = "openssl x509 -in {crtpath} -pubkey -noout"

# Opzione                         | Significato
# openssl req                     | Crea una richiesta o un certificato.
# -config <configpath>            | Legge la configurazione dal file indicato.
# -new                            | Crea una nuova richiesta.
# -x509                           | Produce un certificato X.509 autofirmato.
# -days <days>                    | Imposta la validità del certificato in giorni.
# -sha256                         | Usa SHA-256 per la firma.
# -batch                          | Evita le domande interattive per la richiesta.
# -extensions v3_root_ca          | Applica le estensioni della sezione v3_root_ca.
# -passin pass:<passphrase>       | Usa la passphrase fornita per leggere la chiave privata.
# -key <cakeypath>                | Usa la chiave privata esistente indicata.
# -out <cacrtpath>                | Scrive il certificato nel file indicato.
ROOT_CRT_GEN = "openssl req -config {configpath} -new -x509 -sha256 -batch -extensions v3_root_ca -passin file:{passphrasepath} -key {cakeypath} -out {cacrtpath}"


# comando per visualizzare i dettagli del certificato
CRT_SHOW = "openssl x509 -in {crtpath} -noout -text"


# INTERMEDIATE_CSR_GEN = "openssl req -config {configpath} -new -sha256 -batch -verbose -extensions v3_intermediate_ca -passin file:{passphrasepath} -key {cakeypath} -out {csrpath}"

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
    "openssl pkey -in {keypath} -passin file:{passphrasepath} -noout -text"
)

KEY_GEN = "openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:{bits} -out {output}"

CSR_GEN = "openssl req -config {configpath} -new -sha256 -batch -verbose -key {keypath} -out {csrpath}"

CSR_VERIFY = "openssl req -in {csrpath} -noout -verify -text"

# mostra la chiave pubblica a partire dalla chiave privata
# PUBLICKEY_FROM_KEY_SHOW = (
#     "openssl pkey -in {keypath} -pubout -noout -text -passin file:{passphrasepath}"
# )

CRT_SIGN_SERVER = "openssl ca -config {intermediateconfigpath} -batch -notext -verbose -extfile {extpath} -extensions server_cert -days {days} -md sha256 -in {csrpath} -out {output} -passin file:{intermediatepassphrasepath}"

CRT_SIGN_CLIENT = "openssl ca -config {intermediateconfigpath} -batch -notext -verbose -extfile {extpath} -extensions client_cert -days {days} -md sha256 -in {csrpath} -out {output} -passin file:{intermediatepassphrasepath}"

# comando per visualizzare i dettagli del certificato
CRT_SHOW = "openssl x509 -in {crtpath} -noout -text"

# comando per verificare un certificato rispetto a un certificato CA
CRT_VERIFY = "openssl verify -CAfile {CAcrtpath} {crtpath}"

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

ROOT_SIGN_INTERMEDIATE_CRT = "openssl ca -config {rootconfigpath} -batch -notext -extensions v3_intermediate_ca -md sha256 -in {csrpath} -out {output} -passin file:{passphrasepath}"

INTERMEDIATE_CSR_GEN = "openssl req -config {intermediateconfigpath} -new -sha256 -batch -verbose -reqexts v3_intermediate_req -passin file:{passphrasepath} -key {intermediatekeypath} -out {csrpath}"

INTERMEDIATE_CSR_VERIFY = "openssl req -in {csrpath} -noout -verify -text"

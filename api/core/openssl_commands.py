from dataclasses import dataclass
from pathlib import Path
from string import Template


PRIV_KEY_GEN = Template("openssl genrsa -out $keypath $bits")
# PRIV_KEY_GEN.substitute(keypath=None,bits=2048')

PRIV_KEY_PRINT = Template("openssl rsa  -in $keypath -noout -text")
# PRIV_KEY_PRINT.substitute(keypath=None')


REQ_GEN = Template(
    "openssl req -config $configpath -new -sha256 -verbose -batch -key $keypath -out $csrpath"
)
# REQ_GEN.substitute(configpath=None, keypath=None, csrpath=None)

REQ_PRINT = Template("openssl req -text -noout -verbose -in $csrpath")
# REQ_PRINT.substitute(csrpath=None)


CERT_GEN = Template(
    "openssl ca -config $confpath -notext -md sha256 -days $days -verbose -batch -extfile $extpath -extensions req_ext -passin file:'$passphrsepath' -in $csrpath -out $crtpath"
)
# CERT_GEN.substitute(
#     confpat=None, days=365, extpath=None, passphrsepath=None, csrpath=None, crtpath=None
# )

CERT_PRINT = Template("openssl x509 -noout -text -in $crtpath")
# CERT_PRINT.substitute(crtpath=None)

CERT_VERIFY = Template("openssl verify -CAfile $capath $crtpath")
# CERT_VERIFY.substitute(capath=None, crtpath=None)


PUB_KEY_GEN = Template("openssl x509 -pubkey -noout -in $crtpath -out $pubkeypath")
# PUB_KEY_GEN.substitute(crtpath=None,pubkeypath=None)

PUB_KEY_PRINT = Template("openssl rsa -pubout -in $keypath")
# PUB_KEY_PRINT.substitute(keypath=None)

CA_KEY_GEN = Template(
    "openssl genrsa -aes256 -passout file:$passphrasepath -out $cakeypath 4096"
)
# CA_KEY_GEN.substitute(passphrasepath=None, cakeypath=None)

CA_CRT_GEN = Template(
    "openssl req -config $configpath -new -x509 -nodes -days $days -sha256 -extensions v3_ca -passin file:$passphrasepath -key $cakeypath -out $cacrtpath"
)
# CA_CRT_GEN.substitute(configpath=None,days=365,passphrasepath=None,cakeypath=None, cacrtpath=None)

CA_PUB_KEY_GEN = Template("openssl x509 -pubkey -noout -in $cacrtpath -out $pubkeypath")
# CA_PUB_KEY_GEN.substitute(cacrtpath=None, pubkeypath=None)


PASSPHRASE_GEN = Template("openssl rand -base64 -out '$passphrasepath' $length")
# PASSPHRASE_GEN = Template("openssl rand -base64  $length")
# PASSPHRASE_GEN.substitute(passphrasepath=None, length=24)

# OpenSSL configuration templates

The `configs/` directory contains OpenSSL configuration templates for a root CA,
an intermediate CA, generic certificate requests, and server/client certificate
extensions:

- `root-ca.cnf` creates the self-signed root and signs the intermediate CA.
- `intermediate-ca.cnf` creates the intermediate CA request and issues
  end-entity certificates.
- `certificate.cnf` creates a request for an end-entity certificate.
- `server.ext` and `client.ext` give issued certificates their distinct
  `serverAuth` and `clientAuth` roles. They are not CA certificates.

The templates use OpenSSL's `${ENV::NAME}` expansion. Set the required
environment variables in the process that runs OpenSSL to customize values at
runtime; the templates themselves do not contain deployment-specific subjects,
paths, or certificate identities.

| Template | Runtime variables |
| --- | --- |
| `root-ca.cnf` | `ROOT_CA_DIR`, `ROOT_COUNTRY`, `ROOT_STATE`, `ROOT_LOCALITY`, `ROOT_ORGANIZATION`, `ROOT_ORG_UNIT`, `ROOT_COMMON_NAME`, `ROOT_EMAIL` |
| `intermediate-ca.cnf` | `INTERMEDIATE_CA_DIR`, `INTERMEDIATE_COUNTRY`, `INTERMEDIATE_STATE`, `INTERMEDIATE_LOCALITY`, `INTERMEDIATE_ORGANIZATION`, `INTERMEDIATE_ORG_UNIT`, `INTERMEDIATE_COMMON_NAME`, `INTERMEDIATE_EMAIL` |
| `certificate.cnf` | `CERT_COUNTRY`, `CERT_STATE`, `CERT_LOCALITY`, `CERT_ORGANIZATION`, `CERT_ORG_UNIT`, `CERT_COMMON_NAME`, `CERT_EMAIL` |
| `server.ext` | `SERVER_SAN` (for example, `DNS:api.example.test,IP:192.0.2.10`) |
| `client.ext` | `CLIENT_SAN` (for example, `URI:spiffe://example.test/workload/client-1`) |

The CA directory variables must point to the matching CA directories, which
must contain the database, serial-number, and key/certificate paths configured
in the files. To issue a leaf certificate, pass the matching extension file and
section to `openssl ca`, for example `-extfile configs/server.ext -extensions
server_cert` or `-extfile configs/client.ext -extensions client_cert`. Do not
copy CSR extensions into issued certificates; the intermediate template
deliberately sets `copy_extensions = none`.

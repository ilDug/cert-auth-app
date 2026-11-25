# OpenSSL configuration templates

The `configs/` directory contains OpenSSL configuration templates for a root CA,
an intermediate CA, generic certificate requests, and server/client certificate
extensions:

- `root-ca.cnf` creates the self-signed root and signs the intermediate CA.
- `intermediate-ca.cnf` creates the intermediate CA request and issues
  end-entity certificates.
- `leaf-certificate.cnf` creates a request for an end-entity certificate.
- `server.ext` and `client.ext` give issued certificates their distinct
  `serverAuth` and `clientAuth` roles. They are not CA certificates.

`ConfigController.compile_root_config()` renders `root-ca.cnf` into the root
CA directory. Pass a `RootCertificateConfigModel` containing `root_ca_dir`,
`country`, `state`, `locality`, `organization`, `organizational_unit`, and
`common_name`. The certificate configuration models validate and escape these
values for OpenSSL: they must be non-empty and contain no control characters.
The templates omit `emailAddress` from the subject rather than setting it to an
empty value, which OpenSSL rejects.
The model fields contain the escaped values. The root template uses Python `string.Template`
placeholders such as `${country}`; `$$dir` becomes OpenSSL's `$dir` in the
compiled file. The template must be compiled before passing it to OpenSSL.

All templates use Python `string.Template` placeholders. Render each template
before passing it to OpenSSL. The other templates require these values:

| Template | Template values |
| --- | --- |
| `intermediate-ca.cnf` | `intermediate_ca_dir`, `country`, `state`, `locality`, `organization`, `organizational_unit`, `common_name` |
| `leaf-certificate.cnf` | `country`, `state`, `locality`, `organization`, `organizational_unit`, `common_name` |
| `server.ext` | `san` (for example, `DNS:api.example.test,IP:192.0.2.10`) |
| `client.ext` | `san` (for example, `URI:spiffe://example.test/workload/client-1`) |

`compile_intermediate_config()` and `compile_leaf_config()` validate their
inputs with the corresponding models. Callers rendering the extension
templates must validate and escape their values before substitution.

The CA directory paths must point to the matching CA directories, which
must contain the database, serial-number, and key/certificate paths configured
in the files. To issue a leaf certificate, pass the matching extension file and
section to `openssl ca`, for example `-extfile configs/server.ext -extensions
server_cert` or `-extfile configs/client.ext -extensions client_cert`. Do not
copy CSR extensions into issued certificates; the intermediate template
deliberately sets `copy_extensions = none`.

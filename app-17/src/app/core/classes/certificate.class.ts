

export class Certificate {
    constructor(c: Partial<Certificate>) {
        Object.assign(this, c)
    }
    status: string
    exp_date: Date
    revoke_date: Date
    serial: number
    filename_unknown: string
    common_name: string
}

export class CertificateSigningRequest {
    constructor(c: Partial<CertificateSigningRequest>) {
        Object.assign(this, c)
    }
    subject: string
    alt_names: string[] = []
    days: number = 1825
}

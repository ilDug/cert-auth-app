export interface Certificate {
    status: string;
    exp_date: Date;
    revoke_date: Date;
    serial: number;
    filename_unknown: string;
    common_name: string;
}

export interface CertificateSigningRequest {
    subject: string;
    alt_names: string[];
    days: number;
}
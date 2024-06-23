import { Subject } from "rxjs";

export class UploadOptions {
    constructor(o: Partial<UploadOptions>) {
        o.validExtensions = o.validExtensions ?? ["jpg", "jpeg", "png", "tiff", 'pdf'];
        o.maxFileSize = 3000000;
        o.prefix = o.prefix ?? "";
        Object.assign(this, o);
    }

    /** estensioni suportate */
    validExtensions: string[];

    /** dimensione massima del file in byte */
    maxFileSize: number;

    /** prefisso del nomefile */
    prefix: string;
}


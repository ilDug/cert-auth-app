import { Subject } from 'rxjs';



export interface IUploadOptions {
    /** estensioni suportate */
    validExtensions?: string[];

    /** dimensione massima del file in byte */
    maxFileSize?: number;

    /** prefisso da assegnare al nome del file */
    prefix?: string;
}





export class UploadOptions implements IUploadOptions {
    /** estensioni suportate */
    validExtensions: string[];

    /** dimensione massima del file in byte */
    maxFileSize: number;

    /** prefisso del nomefile */
    prefix: string;

    constructor() {
        this.validExtensions = ["jpg", "jpeg", "png", "tiff", 'pdf'];
        this.maxFileSize = 3000000
    }

}




export class UploadSet {
    public file?: File;
    public base64: string
    public filename: string;
    public src: string;
    public progress: Subject<number>;
    public completed: boolean = false;
    public options: UploadOptions;
    public data: any;
    get prefix() { return this.options.prefix ?? "" }


    /**
     * 
     * @param filename nome del file
     * @param file il file in formato File
     * @param options opzioni di caricamento
     */
    constructor(filename: string, file?: File, options?: IUploadOptions) {

        /** inizializza il progress */
        this.progress = new Subject<number>();

        /** inizializza le opzioni */
        this.defaultOptions(options);

        this.file = file;

        this.filename = filename.trim().replace(/\s/g, "-");


        if (!this.checkFileExtension(file)) throw new Error(`L'estensione del file non è supportata. ALLOWED EXT: ${JSON.stringify(this.options.validExtensions)}`);
        if (!this.checkFileDimension(file)) throw new Error(`Il file è troppo grande per essere caricato. MAX SIZE: ${this.options.maxFileSize / 1000} kb.`);


        let reader: FileReader = new FileReader();
        reader.onload = (e: Event) => {
            
            const base64: string | any = reader.result;
            this.src = base64;

            const regex = new RegExp(/(data:)(.+)(;base64,)/)
            const rawdata = base64.replace(regex, '');
            this.base64 = rawdata;
        }

        if (file) reader.readAsDataURL(file);
    }




    /** inizializza le opzioni dek Set */
    private defaultOptions(opts: IUploadOptions) {
        let options = new UploadOptions();

        if (opts.hasOwnProperty('validExtensions')) options.validExtensions = opts['validExtensions'];
        if (opts.hasOwnProperty('prefix')) options.prefix = opts['prefix'];
        if (opts.hasOwnProperty('maxFileSize')) options.maxFileSize = opts['maxFileSize'];

        this.options = options;
        console.log(this.options);

    }





    /**
     * metodo privato che controlla il File passato come argomento per vedere se corrisponde alle regole di caricamento
     * @param file il file da controllare
     */
    private checkFileExtension(file: File): boolean {
        const extension = file.name
            .split(".")
            .splice(-1)[0]
            .toLowerCase();
        return this.options.validExtensions.indexOf(extension) > -1;
    }




    /**
     * controlla che il file da caricare non abbia una dimnesione maggiore del consetito
     * @param file il file da controllare
     */
    private checkFileDimension(file: File): boolean {
        return file.size <= this.options.maxFileSize;
    }


}



import { Directive, ElementRef, EventEmitter, HostBinding, HostListener, Input, Output } from '@angular/core';
import { NgxUploadListDirective } from './ngx-upload-list.directive';
import { UploadOptions, UploadSet } from './uploas-set';

@Directive({
    selector: '[NgxUploadArea]'
})
export class NgxUploadAreaDirective {

    constructor() { }

    private isHover: boolean;

    @Input() uploadOptions: Partial<UploadOptions>;
    // @Input() uploadList: NgxUploadListDirective

    /** emette il UploadSet a seguito dell'aggiunta del file */
    @Output() add: EventEmitter<UploadSet> = new EventEmitter();

    /** emette errori di aggiunta */
    @Output() error: EventEmitter<string> = new EventEmitter();

    @HostListener("drop", ["$event"]) onDropListener = this.onDrop;
    @HostListener("dragover", ["$event"]) onDragOverListener = this.onDragOver;
    @HostListener("dragleave", ["$event"]) onDragLeaveListener = this.onDragLeave;
    @HostListener('click') clickListener = this.selectFile;

    @HostBinding('class.drag-hover') get hover() { return this.isHover };
    @HostBinding('attr.droppable') droppable = true;


    /**
     * crea un UploadSet e lo emette attraverso l'evento "add"
     * in caso di errore emette l'evento "error"
     * @param file oggetto File da caricare
     * @param filename nome del file
     */
    private createSet(file: File, filename: string) {
        console.log(file, filename);

        let opts = this.uploadOptions || {};

        try {
            /** crea un nuovo set per il file */
            const f = new UploadSet(file.name, file, opts);
            /** emette l'aggiunta del file */
            this.add.emit(f);
            /** carica il file nella lista */
            // if (!this.uploadList) throw new Error("Non è stata individuata la lista dei file. UPLOAD_LIST_ERROR");

            // this.uploadList.add(f)

            console.log(f);


        } catch (error) {
            this.error.emit(error);
            console.error(error)
        }
    }



    onDrop(e) {
        e.preventDefault();
        const data: DataTransfer = e.dataTransfer;
        const file: File = data.files[0];
        this.createSet(file, file.name)
        this.isHover = false;
    }



    onDragOver(e) {
        e.stopPropagation();
        e.preventDefault();
        // this.setAreaStyle('add')
        this.isHover = true;
    }



    onDragLeave() {
        // this.setAreaStyle('remove')
        this.isHover = false;
    }

    /**
     * handler per il file selezionato con il bottone
     */
    public selectFile() {
        /** crea l'elemento */
        const inputfile: HTMLInputElement = document.createElement("input");
        inputfile.type = "file"

        /** aggiunge un listener */
        inputfile.onchange = (e: Event) => {
            const file: File = inputfile.files[0];
            this.createSet(file, file.name)
        }

        inputfile.click();
    }

}

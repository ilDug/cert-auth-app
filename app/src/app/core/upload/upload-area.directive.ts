import { Directive, input, output, signal } from '@angular/core';
import { UploadOptions } from './upload-options.class';

@Directive({
    selector: '[UploadArea]',
    standalone: true,
    host: {
        '(drop)': 'onDrop($event)',
        '(dragover)': 'onDragOver($event)',
        '(dragleave)': 'onDragLeave($event)',
        '(click)': 'selectFile()',
        '[class.drag-hover]': 'isHover()', // classe da aggiungere in caso di hover
        '[hover]': 'isHover()', // attributo da aggiungere in caso di hover
        '[attr.droppable]': 'true'
    }
})
export class UploadAreaDirective {
    // emette il file aggiunto
    add = output<File>();

    // emette errori di aggiunta
    error = output<string>();

    //opzioni di caricamento
    uploadOptions = input<Partial<UploadOptions>>();

    // indica se il mouse è sopra l'area di caricamento
    isHover = signal<boolean>(false);

    // azioni da eseguire al drop
    onDrop(event: DragEvent) {
        const data: DataTransfer = event.dataTransfer; // recupera i dati del drop
        const file: File = data.files[0]; // recupera il file

        if (!this.checkFileExtension(file)) {
            // emette l'errore
            this.error.emit(`L'estensione del file non è supportata. ALLOWED EXT: ${JSON.stringify(this.uploadOptions().validExtensions)}`);
            return false;
        }
        if (!this.checkFileDimension(file)) {
            this.error.emit(`Il file è troppo grande per essere caricato. MAX SIZE: ${this.uploadOptions().maxFileSize / 1000} kb.`); // emette l'errore
            return false ;
        }




        this.add.emit(file); // emette il file

        this.isHover.set(false); // resetta il flag di hover
        return false; // prevent default
    }

    // azioni da eseguire al dragover
    onDragOver(event: DragEvent) {
        this.isHover.set(true); // setta il flag di hover
        return false; // prevent default
    }

    // azioni da eseguire al dragleave
    onDragLeave(event: DragEvent) {
        this.isHover.set(false); // resetta il flag di hover
        return false; // prevent default
    }

    // azioni da eseguire al click
    selectFile() {
        const input: HTMLInputElement = document.createElement('input'); // crea un input
        input.type = 'file'; // setta il tipo di input

        input.onchange = (e: Event) => { // azioni da eseguire al cambio del valore dell'input
            const file: File = input.files[0]; // recupera il file
            // this.createSet(file, file.name); // crea il set
        }
        input.click(); // simula il click sull'input

    }


    // metodo privato che controlla il file passato come argomento per vedere se corrisponde alle regole di caricamento
    private checkFileExtension(file: File): boolean {
        // recupera l'estensione del file
        const extension = file.name
            .split('.')
            .splice(-1)[0]
            .toLowerCase();

        return this.uploadOptions().validExtensions.includes(extension); // controlla se l'estensione è supportata
    }

    // metodo privato che controlla la dimensione del file passato come argomento
    private checkFileDimension(file: File): boolean {
        return file.size <= this.uploadOptions().maxFileSize; // controlla la dimensione del file
    }

}

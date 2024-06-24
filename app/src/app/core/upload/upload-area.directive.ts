import { Directive, effect, inject, input, output, signal } from '@angular/core';
import { UploadOptions } from './upload-options.class';
import { UploadService } from './upload.service';

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
    uploadOptions = input<Partial<UploadOptions>>({});
    #optionsEffect = effect(() => this.#upload$.uploadOptions = new UploadOptions(this.uploadOptions()));

    // indica se il mouse è sopra l'area di caricamento
    isHover = signal<boolean>(false);

    // inject the main service
    #upload$ = inject(UploadService);

    // azioni da eseguire al drop
    onDrop(event: DragEvent) {
        const data: DataTransfer = event.dataTransfer; // recupera i dati del drop
        const file: File = data.files[0]; // recupera il file

        this.#onAddFile(file); // aggiunge il file alla lista

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
            this.#onAddFile(file); // aggiunge il file alla lista
        }
        input.click(); // simula il click sull'input

    }

    
    #onAddFile(file: File) {
        try {
            this.#upload$.addFileToList(file); // aggiunge il file alla lista
            this.add.emit(file); // emette il file
        } catch (e) {
            this.error.emit(e.message); // emette l'errore
            return false; // prevent default
        }
    }


}

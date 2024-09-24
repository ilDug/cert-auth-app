import { Directive, model, output, signal } from '@angular/core';

@Directive({
    selector: '[fileDrop]',
    standalone: true,
    host: {
        '(drop)': 'onDrop($event)',
        '(dragover)': 'onDragOver($event)',
        '(dragleave)': 'onDragLeave($event)',
        '[class.drag-hover]': 'isHover()',
        '[hover]': 'isHover()',
        '[attr.droppable]': 'true',
        '(click)': 'selectFile()'
    }
})
export class FileDropDirective {

    // contenuto del file
    value = model.required<string>(); 

    // indica se il mouse è sopra l'area di caricamento
    isHover = signal<boolean>(false);

    // emette errori di aggiunta
    error = output<string>();

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

    // azioni da eseguire all'aggiunta di un file
    #onAddFile(file: File) {
        try {
            const reader = new FileReader(); // crea un reader

            reader.onload = (e: Event) => { 
                const content: string = reader.result as string; // recupera il contenuto del file
                this.value.set(content); // setta il contenuto del file
            }
            
            reader.readAsText(file); // legge il file come testo

        } catch (e) {
            this.error.emit(e.message ?? e); // emette l'errore
            return false; // prevent default
        }
    }
}

import { WritableSignal, computed, effect, signal } from "@angular/core";
import { toSignal } from "@angular/core/rxjs-interop";
import { Subject } from "rxjs";

export class UploadItem {
    constructor(file: File) {
        this.file = signal(file);

        //crea un reader per leggere il file
        const reader = new FileReader();

        reader.onload = (e: Event) => {
            // imposta il src dell'immagine (ammesso che lo sia)
            const base64: string = reader.result as string;
            this.src.set(base64);

            // estrae il base64 dal file eliminando i metadati
            const regex = new RegExp(/(data:)(.+)(;base64,)/)
            const rawdata = base64.replace(regex, '');
            this.base64.set(rawdata);
        };

        // legge il file come base64
        reader.readAsDataURL(this.file());
    }

    file: WritableSignal<File>;
    filename = computed(() => this.file()?.name.trim().replace(/\s/g, "- "));
    size = computed(() => Math.round(this.file()?.size / 1000));
    src = signal<string>(undefined);
    base64 = signal<string>(undefined);
    progress$ = new Subject<number>();
    text = computed(() => {
        try {
            return atob(this.base64());
        } catch {
            return "BINARY FILE";
        }
    })
    // progress = toSignal(this.progress$);
}

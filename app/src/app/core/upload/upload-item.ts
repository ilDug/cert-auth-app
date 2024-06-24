import { WritableSignal, computed, signal } from "@angular/core";
import { Subject, Subscription } from "rxjs";

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

        this.progressSubscription = this.progress$.subscribe(this.onLoad);
    }

    file: WritableSignal<File>;
    filename = computed(() => this.file()?.name.trim().replace(/\s/g, "- "));
    size = computed(() => Math.round(this.file()?.size / 1000));
    src = signal<string>(undefined);
    base64 = signal<string>(undefined);
    
    progress$ = new Subject<number>();
    progress = signal<number>(0);
    private progressSubscription: Subscription;

    text = computed(() => {
        try {
            return atob(this.base64());
        } catch {
            return "BINARY FILE";
        }
    })

    error = signal<string>(undefined);
    status = signal<"PENDING" | "SUCCESS" | "FAIL">(undefined);
    pending = computed(() => this.status() == "PENDING");
    completed = computed(() => this.status() == "SUCCESS");
    failed = computed(() => this.status() == "FAIL");

    // pipe //
    private onLoad = {
        next: p => {
            this.status.set("PENDING");
            this.progress.set(p);
        },
        error: err => {
            this.status.set("FAIL");
            this.error.set(err);
        },
        complete: () => {
            this.status.set("SUCCESS");
        }
    }

    unsubscribe() {
        this.progressSubscription.unsubscribe();
    }


}



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

    // file signal 
    file: WritableSignal<File>;

    // filename signal
    filename = computed(() => this.file()?.name.trim().replace(/\s/g, "- "));

    // file size signal
    size = computed(() => Math.round(this.file()?.size / 1000));

    // src image property for preview thumbnail
    src = signal<string>(undefined);

    // base64 signal for file content
    base64 = signal<string>(undefined);
    
    // progress Subject for upload progress
    progress$ = new Subject<number>();

    // progress signal for upload progress updated by the onLoad method
    progress = signal<number>(0);

    // Subscription to the progress Subject
    private progressSubscription: Subscription;

    // computed signal for the content of the file
    text = computed(() => {
        try {
            return atob(this.base64());
        } catch {
            return "BINARY FILE";
        }
    })

    // error message from server
    error = signal<string>(undefined);

    // status signal for the upload status
    status = signal<"PENDING" | "SUCCESS" | "FAIL">(undefined);

    // computed signal for the status
    pending = computed(() => this.status() == "PENDING");

    // computed signal for the status
    completed = computed(() => this.status() == "SUCCESS");
    
    // computed signal for the status
    failed = computed(() => this.status() == "FAIL");

    // onLoad pipe for the progress Subject
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

    // unsubscribe from the progress Subject
    unsubscribe() {
        this.progressSubscription.unsubscribe();
    }


}



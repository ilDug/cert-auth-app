import { Directive, computed, effect, input, output, signal } from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { Subject } from 'rxjs';

@Directive({
    selector: '[UploadItem]',
    exportAs: 'UploadItem',
    standalone: true
})
export class UploadItemDirective {

    constructor() {
        this.progress$
            .asObservable()
            .pipe(
                takeUntilDestroyed()
            )
            .subscribe({
                next: p => this.progress.set(p),
                error: err => {
                    this.status.set("FAIL");
                    this.error.set(err);
                },
                complete: () => {
                    this.status.set("SUCCESS");
                    this.loaded.emit(true);
                }
            });
    }

    file = input.required<File>();
    filename = computed(() => this.file().name.trim().replace(/\s/g, "- "));

    src = signal<string>(undefined);
    base64 = signal<string>(undefined);

    // messaggio di errore
    error = signal<string>(undefined);

    progress$ = new Subject<number>();
    progress = signal<number>(0);


    #readerEffect = effect(() => {
        if (!this.file()) return;

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
    });

    status = signal<"PENDING" | "SUCCESS" | "FAIL">("PENDING");
    pending = computed(() => this.status() == "PENDING");
    completed = computed(() => this.status() == "SUCCESS");
    failed = computed(() => this.status() == "FAIL");


    /////// OUTPUTS ///////

    // emette quado il file è stato caricato correttamente sul server
    loaded = output<boolean>();
    // emette quando il file è da rimuovere
    remove = output<boolean>();

}

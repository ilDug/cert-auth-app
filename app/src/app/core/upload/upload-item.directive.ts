import { DestroyRef, Directive, computed, effect, inject, input, output, signal } from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { Subject, filter, take } from 'rxjs';
import { UploadListDirective } from './upload-list.directive';
import { UploadService } from './upload.service';
import { UploadItem } from './upload-item';

@Directive({
    selector: '[UploadItem]',
    exportAs: 'UploadItem',
    standalone: true
})
export class UploadItemDirective {

    constructor() {
        // this.list.upload
        //     .pipe(takeUntilDestroyed(this.df))
        //     .subscribe(() => {
        //         if (this.pending()) this.upload();
        //     });
    }

    #upload$ = inject(UploadService);
    // private list = inject(UploadListDirective);
    // private df = inject(DestroyRef);

    item = input.required<UploadItem>();
    file = computed(() => this.item().file());

    // file properties
    filename = computed(() => this.item().filename())
    size = computed(() => this.item().size());
    src = computed(() => this.item().src());
    base64 = computed(() => this.item().base64());
    text = computed(() => this.item().text());

    // messaggio di errore
    error = signal<string>(undefined);

    // progress$ = new Subject<number>();
    progress = signal<number>(0);

    status = signal<"PENDING" | "SUCCESS" | "FAIL">("PENDING");
    pending = computed(() => this.status() == "PENDING");
    completed = computed(() => this.status() == "SUCCESS");
    failed = computed(() => this.status() == "FAIL");


    /////// OUTPUTS ///////

    // // emette quado il file è stato caricato correttamente sul server
    // loaded = output<boolean>();
    // // emette quando il file è da rimuovere
    // remove = output<boolean>();


    // upload() {
    //     this.progress$
    //         .asObservable()
    //         .pipe(
    //             takeUntilDestroyed(this.df)
    //         )
    //         .subscribe({
    //             next: p => this.progress.set(p),
    //             error: err => {
    //                 this.status.set("FAIL");
    //                 this.error.set(err);
    //             },
    //             complete: () => {
    //                 this.status.set("SUCCESS");
    //                 this.loaded.emit(true);
    //             }
    //         });

    //     this.upload$.upload(this.item());
    // }

}



    // #readerEffect = effect(() => {
    //     if (!this.file()) return;

    //     //crea un reader per leggere il file
    //     const reader = new FileReader();

    //     reader.onload = (e: Event) => {
    //         // imposta il src dell'immagine (ammesso che lo sia)
    //         const base64: string = reader.result as string;
    //         this.item().src.set(base64);

    //         // estrae il base64 dal file eliminando i metadati
    //         const regex = new RegExp(/(data:)(.+)(;base64,)/)
    //         const rawdata = base64.replace(regex, '');
    //         this.item().base64.set(rawdata);
    //     };

    //     // legge il file come base64
    //     reader.readAsDataURL(this.file());
    // });
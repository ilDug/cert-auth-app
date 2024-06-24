import { HttpClient, HttpErrorResponse, HttpEvent, HttpEventType } from "@angular/common/http";
import { Injectable, computed, inject, signal } from "@angular/core";
import { Observable, catchError, delay, filter, forkJoin, map, merge, of, tap } from "rxjs";
import { UploadOptions } from "./upload-options.class";
import { UploadItem } from "./upload-item";

@Injectable()
export class UploadService {
    #http = inject(HttpClient);

    endpoint: string = null;

    items = signal<UploadItem[]>([]);

    //opzioni di caricamento
    uploadOptions: UploadOptions;

    /******************************************************************** */
    // FILES MANAGER
    addFileToList(file: File) {
        if (!this.checkFilesNumber()) {
            throw new Error('UploadService: max number of files reached');
        }

        if (!this.checkFileExtension(file)) {
            throw new Error(`UploadService: file extension not supported. ALLOWED EXT: ${JSON.stringify(this.uploadOptions.validExtensions)}`);
        }

        if (!this.checkFileDimension(file)) {
            throw new Error(`UploadService: file is too big to be uploaded. MAX SIZE: ${this.uploadOptions.maxFileSize / 1000} kb.`);
        }

        this.items.update(items => [...items, new UploadItem(file)]);
    }

    // rimuove un file dalla lista
    removeFileFromList(item: UploadItem) {
        const i = this.items().indexOf(item);
        if (i < 0) return;
        this.items()[i].unsubscribe();
        this.items.update(items => {
            items.splice(i, 1);
            return [...items]
        });
    }

    // elimina tutti i file dalla lista
    clearItemList() {
        this.items().forEach(item => item.unsubscribe());
        this.items.set([]);
    }

    /******************************************************************** */
    // CHECKERS

    // metodo privato che controlla il file passato come argomento per vedere se corrisponde alle regole di caricamento
    private checkFileExtension(file: File): boolean {
        // recupera l'estensione del file
        const extension = file.name
            .split('.')
            .splice(-1)[0]
            .toLowerCase();

        return this.uploadOptions.validExtensions.includes(extension); // controlla se l'estensione è supportata
    }

    // metodo privato che controlla la dimensione del file passato come argomento
    private checkFileDimension(file: File): boolean {
        return file.size <= this.uploadOptions.maxFileSize; // controlla la dimensione del file
    }


    // metodo privato che controlla il numero di file caricati
    private checkFilesNumber(): boolean {
        return this.items().length < this.uploadOptions.maxFilesNum;
    }


    /******************************************************************** */
    // UPLOAD HANDLERS

    /** intercetta gli eventi PROGRESS ed aggiorna il Subject progress dell' UploadSet */
    protected handleProgressResponse = (item: UploadItem) => (event: HttpEvent<any>) => {
        if (event.type == HttpEventType.UploadProgress) {
            // calculate the progress percentage
            const percentDone = Math.round(100 * event.loaded / event.total);
            // pass the percentage into the progress-stream
            item.progress$.next(percentDone);

            console.log(`UPLOAD PROGRESS EVENT: ${percentDone}`);

            return null;
        } else return event // se non è un evento di progress ritorna l'evento
    }

    // intercetta l'evento di risposta finale
    protected handleFinalResponse = (item: UploadItem) => (event: HttpEvent<any>) => {
        if (event.type == HttpEventType.Response) {
            const result = event.body;

            /** se il file è caricato il server resituisce un codice 200 */
            if (result) item.progress$.complete();

            console.log(`UPLOAD FINAL EVENT: ${result}`);

            return result
        } else return event // se non è un evento di risposta ritorna l'evento 
    }

    // intercetta l'evento di errore
    protected handleErrorResponse = (item: UploadItem) => (err: HttpErrorResponse): Observable<null> => {
        /** problemi di caricamento */
        item.progress$.error(err.error);

        console.log(`UPLOAD ERROR EVENT: ${err.error}`);
        console.log(err);
        return of(null);
    }

    /******************************************************************** */
    // UPLOAD METHODS

    uploadItem(item: UploadItem): Observable<any> {
        if (!this.endpoint)
            throw new Error('UploadService: endpoint not set');

        const formData = new FormData();
        formData.append('file', item.file(), item.filename());

        const req = this.#http.post(this.endpoint, formData, {
            reportProgress: true,
            observe: 'events'
        });

        const _ = req.pipe(
            /** filtra solo gli eventi UploadProgress e Response*/
            filter((event: HttpEvent<any>) => [HttpEventType.UploadProgress, HttpEventType.Response].includes(event.type)),

            /** intercetta l'evento di progress */
            map(this.handleProgressResponse(item)),

            /** filtra solo gli eventi Response */
            filter((event: HttpEvent<any>) => event.type == HttpEventType.Response),

            /** elabora le riposte di errore */
            catchError(this.handleErrorResponse(item)),


            /** filtra le risposte non nulle */
            filter(res => res !== null),

            /** intercetta l'evento di risposta finale */
            map(this.handleFinalResponse(item)),
        )

        return of(item).pipe(
            delay(1000),
            tap(() => item.progress$.next(50)),
            delay(1000),
            tap(() => item.progress$.next(100)),
            delay(1000),
            tap(() => item.progress$.complete()),
        )

        return _;
    }


    uploadAll(waitAtTheEnd: boolean = false): Observable<any> | Observable<any[]> {
        const requests = this.items()
            .filter(item => !item.completed())
            .map(item => this.uploadItem(item));

        return waitAtTheEnd
            ? forkJoin(requests) /** emette alla  fine */
            : merge(...requests)/** emette uno alla volta */
    }
}

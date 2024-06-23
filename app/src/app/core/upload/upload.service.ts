import { HttpClient, HttpErrorResponse, HttpEvent, HttpEventType } from "@angular/common/http";
import { Injectable, inject, signal } from "@angular/core";
import { Observable, catchError, filter, map, of } from "rxjs";
import { UploadItemDirective } from "./upload-item.directive";

@Injectable({
    providedIn: 'root'
})
export class UploadService {
    #http = inject(HttpClient);

    endpoint: string = null;

    /** intercetta gli eventi PROGRESS ed aggiorna il Subject progress dell' UploadSet */
    protected handleProgressResponse = (file: UploadItemDirective) => (event: HttpEvent<any>) => {
        if (event.type == HttpEventType.UploadProgress) {
            // calculate the progress percentage
            const percentDone = Math.round(100 * event.loaded / event.total);
            // pass the percentage into the progress-stream
            file.progress$.next(percentDone);

            console.log(`UPLOAD PROGRESS EVENT: ${percentDone}`);

            return null;
        } else return event // se non è un evento di progress ritorna l'evento
    }

    // intercetta l'evento di risposta finale
    protected handleFinalResponse = (file: UploadItemDirective) => (event: HttpEvent<any>) => {
        if (event.type == HttpEventType.Response) {
            const result = event.body;

            /** se il file è caricato il server resituisce un codice 200 */
            if (result) file.progress$.complete();

            console.log(`UPLOAD FINAL EVENT: ${result}`);

            return result
        } else return event // se non è un evento di risposta ritorna l'evento 
    }

    // intercetta l'evento di errore
    protected handleErrorResponse = (file: UploadItemDirective) => (err: HttpErrorResponse): Observable<null> => {
        /** problemi di caricamento */
        file.progress$.error(err.error);

        console.log(`UPLOAD ERROR EVENT: ${err.error}`);
        console.log(err);
        return of(null);
    }


    upload(item: UploadItemDirective): Observable<any> {
        if (!this.endpoint)
            throw new Error('UploadService: endpoint not set');

        const formData = new FormData();
        formData.append('file', item.file(), item.filename());

        const req = this.#http.post(this.endpoint, formData, {
            reportProgress: true,
            observe: 'events'
        });

        return req.pipe(
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
    }
}

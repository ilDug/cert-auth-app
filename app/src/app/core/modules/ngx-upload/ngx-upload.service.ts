import { HttpEvent, HttpEventType, HttpErrorResponse, HttpClient } from "@angular/common/http";
import { Inject, Injectable } from "@angular/core";
import { catchError, filter, map, Observable, of, pipe } from "rxjs";
import { UploadStrategy, UPLOAD_ENDPOINT, UPLOAD_STRATEGY } from "./injection-token";
import { UploadSet } from "./uploas-set";


@Injectable({
    providedIn: 'root'
})
export class NgxUploadService {

    constructor(
        protected http: HttpClient,
        @Inject(UPLOAD_ENDPOINT) protected url: string,
        @Inject(UPLOAD_STRATEGY) protected strategy: UploadStrategy
    ) { }

    /**
     * carica i file con protocollo Http POST
     */
    public upload(file: UploadSet): Observable<string> {
        if (this.strategy == "BASE64") return this.uploadBase64(file)
        if (this.strategy == "FORMDATA") return this.uploadFormData(file)
        else return this.uploadFormData(file)
    }

    /** intercetta glie eventi PROGRESS ed aggiorna il Subject progress dell' UploadSet */
    protected handleProgressResponse = (file: UploadSet) => (event: HttpEvent<any>) => {
        if (event.type == HttpEventType.UploadProgress) {
            // calculate the progress percentage
            const percentDone = Math.round(100 * event.loaded / event.total);
            // pass the percentage into the progress-stream
            file.progress.next(percentDone);

            console.log(`DAG PROGRESS EVENT: ${percentDone}`);

            // return null;
        }
        return event
        // else return event
    }

    protected handleFinalResponse = (file: UploadSet) => (event: HttpEvent<any>) => {
        if (event.type == HttpEventType.Response) {
            const result: Response = event.body;

            /** se il file è caricato il server resituisce un codice 200 */
            if (result) file.progress.complete();

            /** indica che  l'upload Set è stato caricato (anche in caso di errore) */
            file.completed = true;

            console.log(`DAG FINAL EVENT: ${result}`);

            return result
        } else return event
    }

    protected handleErrorReponse = (file: UploadSet) => (err: HttpErrorResponse) => {
        /** problemi di caricamento */
        file.progress.error(err.error);

        console.log(`DAG ERROR EVENT:`);
        console.log(err);
        return of(null);
    }


    protected filterHttpEventType = (allowedEvents: HttpEventType[]) => pipe(
        filter((event: HttpEvent<any>) => allowedEvents.includes(event.type))
    )
    // filter((event: HttpEvent<any>) => event.type != HttpEventType.Sent), //0
    // filter((event: HttpEvent<any>) => event.type != HttpEventType.UploadProgress), //1
    // filter((event: HttpEvent<any>) => event.type != HttpEventType.ResponseHeader), //2
    // filter((event: HttpEvent<any>) => event.type != HttpEventType.DownloadProgress), //3
    // filter((event: HttpEvent<any>) => event.type != HttpEventType.Response), //4
    // filter((event: HttpEvent<any>) => event.type != HttpEventType.User),//5


    protected responseParser = (file: UploadSet) => pipe(
        this.filterHttpEventType([HttpEventType.Response, HttpEventType.UploadProgress]),
        /** ascolta il progress e lo emette attravesro il subject del fileset */
        map(this.handleProgressResponse(file)),
        /** filtra gli eventi lasciando passare solo le HttpResponse (codice = 4) */
        this.filterHttpEventType([HttpEventType.Response]),
        /** elabora gli errori */
        catchError(this.handleErrorReponse(file)),
        /** filtra gli eventi lasciando passare solo le HttpResponse (codice = 4) */
        filter(res => res !== null),
        /** gestisce le risposte finali */
        map(this.handleFinalResponse(file)),
    )



    // ######################################################################
    public uploadBase64(file: UploadSet): Observable<any> {
        const { filename, base64 } = file
        const body = { filename: filename, base64: base64 }
        const req = this.http.post<string>(this.url, body, { reportProgress: true, observe: 'events' })

        return req.pipe(
            this.responseParser(file)
        )
    }

    // ######################################################################
    public uploadFormData(file: UploadSet): Observable<any> {
        const formdata = new FormData()
        formdata.append('file', file.file, file.filename)

        if (file.data) {
            formdata.append('data', file.data)
            // formdata.append('data', JSON.stringify(file.data))
        }

        const req = this.http.post(this.url, formdata, {
            // headers: new HttpHeaders({ "Content-Type": 'multipart/form-data', }),
            reportProgress: true,
            observe: 'events'
        })

        return req.pipe(
            this.responseParser(file)
        )

    }


}

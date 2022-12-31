import { HttpClient, HttpParams, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, catchError, finalize, lastValueFrom, map, Observable, of, pipe, tap } from 'rxjs';
import { Certificate, CertificateSigningRequest } from './core/classes/certificate.class';
import { ENPOINT } from './core/core.service';

@Injectable({
    providedIn: 'root'
})
export class PKIService {

    constructor(
        /** Angular Client HTTP */
        protected http: HttpClient,

        /** indirizzo del server API */
        @Inject(ENPOINT) protected url: string,
    ) { }


    /** il parametro da parssareper le rigchieste get */
    protected query: any | { [key: string]: any };

    private parseQuery = (query: any): HttpParams => {
        const params: HttpParams = new HttpParams();

        if (typeof query === 'object') {
            for (const key in query) {
                params.append(key, query[key]);
            }
        } else {
            params.set('query', query);
        }
        return params;
    }

    private extractFilenameForBlob = pipe(
        map((res: HttpResponse<Blob>) => {
            const contentDisposition = res.headers.get('content-disposition')
            let [match, filename] = contentDisposition.match(/filename="(.+)"/)
            return { blob: res.body, filename: filename }
        }))

    private downloadBlob = pipe(
        map(({ blob, filename }) => {
            const a = document.createElement('a')
            const objectUrl = URL.createObjectURL(blob)
            a.href = objectUrl
            a.download = filename;
            a.click();
            URL.revokeObjectURL(objectUrl);
            return filename as string
        })
    )

    public exportPki(): Observable<string> {
        return this.http.get(`${this.url}/pki/export`, { responseType: 'blob', observe: 'response' })
            .pipe(
                this.extractFilenameForBlob,
                this.downloadBlob
            )
    }

    public downloadRoot(): Observable<string> {
        return this.http.get(`${this.url}/pki/download-root`, { responseType: 'blob', observe: 'response' })
            .pipe(
                this.extractFilenameForBlob,
                this.downloadBlob
            )
    }


    public resetPki(): Observable<boolean> {
        return this.http.delete<boolean>(`${this.url}/pki/reset`)
    }


}

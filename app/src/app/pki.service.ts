import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, catchError, finalize, lastValueFrom, map, Observable, of, tap } from 'rxjs';
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


    public exportPki(): Observable<string> {
        return this.http.get(`${this.url}/pki/export`, { responseType: 'blob', observe: 'response' })
            .pipe(
                map(res => {
                    const contentDisposition = res.headers.get('content-disposition')
                    let [match, filename] = contentDisposition.match(/filename="(.+)"/)
                    return { blob: res.body, filename: filename }
                }),
                map(({ blob, filename }) => {
                    const a = document.createElement('a')
                    const objectUrl = URL.createObjectURL(blob)
                    a.href = objectUrl
                    a.download = filename;
                    a.click();
                    URL.revokeObjectURL(objectUrl);
                    return filename
                })
            )
    }


}

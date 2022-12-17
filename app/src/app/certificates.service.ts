import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, catchError, finalize, lastValueFrom, map, Observable, of, tap } from 'rxjs';
import { Certificate, CertificateSigningRequest } from './core/classes/certificate.class';
import { ENPOINT } from './core/core.service';

@Injectable({
    providedIn: 'root'
})
export class CertificatesService extends BehaviorSubject<string[]>{

    constructor(
        /** Angular Client HTTP */
        protected http: HttpClient,

        /** indirizzo del server API */
        @Inject(ENPOINT) protected url: string,
    ) {
        /**
         * inizializza sempre con null perchè permette di far
         * capire se la lista è già stata popolata dalla risposta del server
         * */
        super(null)
        this.load();
    }


    /** proprietà che indica se la richiesta non è ancora stata evasa */
    get loading(): boolean { return this.value === null }


    /** il parametro da parssareper le rigchieste get */
    protected query: any | { [key: string]: any };


    /** elabora ongi singolo oggetto della lista restituita dal server API */
    protected itemParser(item: Partial<string>): string {
        return item
    }


    item(subject: string, type: "info" | "pem" | "file"): Observable<string> {
        let url = `${this.url}/display/certificate/${type}/${subject}`
        return this.http.get(url, { responseType: 'text' as 'text' })
    }

    /** esergue la richiesta al server per recuperare la lista di oggetti */
    public load(query?: any | any[]): Promise<string[]> {
        this.next(null)

        this.query = query ?? null;
        const params: HttpParams = this.parseQuery(query);

        const _ = this.http.get<string[]>(`${this.url}/certificates`, { params: params })
            .pipe(
                catchError((err: HttpErrorResponse) => of([])),
                map(list => list.map(this.itemParser)),
                tap(list => this.next(list)),
            )

        return lastValueFrom(_)
    }


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


    /** method to INSERT object to server */
    public add(csr: CertificateSigningRequest): Observable<string> {
        this.next(null)
        return this.http.post(`${this.url}/generate/certificate`, csr, { responseType: 'text' as 'text' })
            .pipe(
                tap(_ => console.log(_)),
                finalize(() => this.load(this.query))
            )
    }



    /** method to DELETE object from server */
    public remove(_id: string): Observable<boolean> {
        this.next(null)
        return this.http.delete<boolean>(`${this.url}/${_id}`)
            .pipe(
                finalize(() => this.load(this.query))
            )
    }





}

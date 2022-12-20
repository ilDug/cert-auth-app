import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, catchError, lastValueFrom, map, Observable, of, tap } from 'rxjs';
import { Certificate } from './core/classes';
import { ENPOINT } from './core/core.service';

@Injectable({
    providedIn: 'root'
})
export class KeysService extends BehaviorSubject<string[]>{

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



    /** esergue la richiesta al server per recuperare la lista di oggetti */
    public load(query?: any | any[]): Promise<string[]> {
        this.next(null)

        this.query = query ?? null;
        const params: HttpParams = this.parseQuery(query);

        const _ = this.http.get<string[]>(`${this.url}/keys`, { params: params })
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


}

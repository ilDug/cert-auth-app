import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Inject, Injectable, InjectionToken } from '@angular/core';
import { BehaviorSubject, catchError, finalize, lastValueFrom, map, Observable, of, tap } from 'rxjs';



/** indirizzo base del SERVER API,  da completare in ciascun SERVICESr */
export const ENPOINT = new InjectionToken<string>('indirizzo base del SERVER API, da completare in ciascun SERVICES')


@Injectable({
    providedIn: 'root'
})
export abstract class CoreService<T> extends BehaviorSubject<T[]>{


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
    protected abstract itemParser(item: Partial<T>): T


    /** restituisce un singolo oggetto della lista */
    public item(_id: string): T {
        if (this.value === null) return null;
        return this.value.find(_ => _['_id'] === _id)
    }


    /** esergue la richiesta al server per recuperare la lista di oggetti */
    public load(query?: any | any[]): Promise<T[]> {
        this.next(null)

        this.query = query ?? null;
        const params: HttpParams = this.parseQuery(query);

        const _ = this.http.get<T[]>(`${this.url}`, { params: params })
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
    public add(object: T): Observable<T> {
        this.next(null)
        return this.http.post<T>(`${this.url}`, object)
            .pipe(
                map(this.itemParser),
                finalize(() => this.load(this.query))
            )
    }



    /** method to UPDATE object to server */
    public edit(object: T): Observable<T> {
        this.next(null)
        return this.http.put<T>(`${this.url}/${object['_id']}`, object)
            .pipe(
                map(this.itemParser),
                finalize(() => this.load(this.query))
            )
    }



    /** method to DELETE object from server */
    public remove(_id: T): Observable<boolean> {
        this.next(null)
        return this.http.delete<boolean>(`${this.url}/${_id}`)
            .pipe(
                finalize(() => this.load(this.query))
            )
    }

}

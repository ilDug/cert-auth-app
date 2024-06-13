import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, computed, effect, inject, signal } from '@angular/core';
import { Certificate } from '../classes';
import { Observable, finalize, lastValueFrom, map, tap } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class KeysService {
    // Angular Client HTTP
    private http = inject(HttpClient);

    // indicalo stato del caricamento
    private PENDING = signal(false);

    // lista di certificati
    collection = signal<string[]>([]);

    // query per la richiesta al server
    query = signal<any | { [key: string]: any }>(null);

    // parametro da passare per le richieste get
    #params = computed<HttpParams>(() => {
        const params: HttpParams = new HttpParams();

        if (typeof this.query() === 'object') {
            for (const key in this.query()) {
                params.append(key, this.query()[key]);
            }
        } else {
            params.set('query', this.query());
        }
        return params;
    });


    // esegue la richiesta al server per recuperare la lista di oggetti
    #loadKeysEffect = effect(() => {
        this.PENDING.set(true);

        const _ = this.http.get<string[]>(`/api/keys`, { params: this.#params() })
            .pipe(
                tap(list => this.collection.set(list)),
                finalize(() => this.PENDING.set(false))
            )
        lastValueFrom(_);
    }, { allowSignalWrites: true });


    privateKey(subject: string, type: "info" | "pem" | "file"): Observable<string> {
        let url = `/api/display/privatekey/${type}/${subject}`
        return this.http.get(url, { responseType: 'text' as 'text' })
    }

    publicKey(subject: string, type: "info" | "pem" | "file"): Observable<string> {
        let url = `/api/display/publickey/${type}/${subject}`
        return this.http.get(url, { responseType: 'text' as 'text' })
    }

}

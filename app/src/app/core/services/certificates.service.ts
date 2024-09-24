import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Injectable, computed, effect, inject, signal } from '@angular/core';
import { Certificate, CertificateSigningRequest } from '../classes';
import { catchError, of, map, tap, finalize, lastValueFrom, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class CertificatesService {
    // Angular Client HTTP
    private http = inject(HttpClient);

    // indicalo stato del caricamento
    private PENDING = signal(false);

    // se modificato, ricarica la lista di certificati
    #refresh = signal(0);

    refresh() {
        this.#refresh.update(r => r + 1);
        return this.#refresh();
    }

    // lista di certificati
    collection = signal<Certificate[]>([]);

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
    #loadCertificatesEffect = effect(() => {
        console.log(`loading certificates... attempt: ${this.#refresh()}`);

        this.PENDING.set(true);

        const _ = this.http.get<Certificate[]>(`/api/certificates`, { params: this.#params() })
            .pipe(
                catchError((err: HttpErrorResponse) => of([])),
                map(list => list.map((item: Partial<Certificate>) => new Certificate(item))),
                tap(list => this.collection.set(list)),
                finalize(() => this.PENDING.set(false))
            )

        lastValueFrom(_);

    }, { allowSignalWrites: true });


    // interrga il server restituendo il certificato richiesto nella forma specificata
    select(subject: string, type: "info" | "pem" | "file"): Observable<string> {
        let url = `/api/display/certificate/${type}/${subject}`
        return this.http.get(url, { responseType: 'text' as 'text' })
    }


    /** method to INSERT object to server */
    add(csr: CertificateSigningRequest): Observable<string> {
        return this.http.post(`/api/generate/certificate`, csr, { responseType: 'text' as 'text' })
            .pipe(
                finalize(() => this.refresh())
            )
    }

    /** method to DELETE object from server */
    remove(subject: string): Observable<boolean> {
        return this.http.delete<boolean>(`/api/erase/certificate/${subject}`)
            .pipe(
                finalize(() => this.refresh())
            )
    }
}

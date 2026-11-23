import { HttpClient, HttpErrorResponse, HttpParams, httpResource } from '@angular/common/http';
import { Injectable, computed, effect, inject, linkedSignal, signal } from '@angular/core';
// import { Certificate, CertificateSigningRequest } from '../classes';
import { Certificate, CertificateSigningRequest } from '../interfaces';
import { catchError, of, map, tap, finalize, lastValueFrom, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class CertificatesService {
    private http = inject(HttpClient);

    #parser = (response: Certificate[]) => response.map(item => ({ ...item, exp_date: new Date(item.exp_date), revoke_date: new Date(item.revoke_date) }))


    certificateResource = httpResource<Certificate[]>(() => `/api/certificates`, { defaultValue: [], parse: this.#parser })
    collections = this.certificateResource.value
    PENDING = linkedSignal<boolean>(() => this.certificateResource.isLoading())
    ERROR = this.certificateResource.error


    // interrga il server restituendo il certificato richiesto nella forma specificata
    select(subject: string, type: "info" | "pem" | "file"): Observable<string> {
        this.PENDING.set(true);
        let url = `/api/display/certificate/${type}/${subject}`
        return this.http.get(url, { responseType: 'text' as 'text' })
            .pipe(
                finalize(() => this.certificateResource.reload())
            )
    }


    /** method to INSERT object to server */
    add(csr: CertificateSigningRequest): Observable<string> {
        this.PENDING.set(true);
        return this.http.post(`/api/generate/certificate`, csr, { responseType: 'text' as 'text' })
            .pipe(
                finalize(() => this.certificateResource.reload())
            )
    }

    /** method to DELETE object from server */
    remove(subject: string): Observable<boolean> {
        this.PENDING.set(true);
        return this.http.delete<boolean>(`/api/erase/certificate/${subject}`)
            .pipe(
                finalize(() => this.certificateResource.reload())
            )
    }
}

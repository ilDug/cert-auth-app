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

    #parser = (response: Certificate[]) => response.map(item => ({
        ...item,
        exp_date: new Date(item.exp_date),
        revoke_date: item.revoke_date ? new Date(item.revoke_date) : null
    }))


    resource = httpResource<Certificate[]>(() => `/api/certificates`, { defaultValue: [], parse: this.#parser })
    list = this.resource.value
    PENDING = linkedSignal<boolean>(() => this.resource.isLoading())
    ERROR = this.resource.error

    /** method to INSERT object to server */
    add(csr: CertificateSigningRequest): Observable<string> {
        this.PENDING.set(true);
        return this.http.post(`/api/generate/certificate`, csr, { responseType: 'text' as 'text' })
            .pipe(
                finalize(() => this.resource.reload())
            )
    }

    /** method to DELETE object from server */
    remove(subject: string): Observable<boolean> {
        this.PENDING.set(true);
        return this.http.delete<boolean>(`/api/erase/certificate/${subject}`)
            .pipe(
                finalize(() => this.resource.reload())
            )
    }
}

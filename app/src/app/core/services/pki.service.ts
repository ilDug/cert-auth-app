import { HttpClient, HttpResponse } from "@angular/common/http";
import { Injectable, inject } from "@angular/core";
import { pipe, map, Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class PKIService {
    // Angular Client HTTP
    private http = inject(HttpClient);

    // estrarre il nome del file dal blob della risposta e ritorna un oggetto con il blob e il nome del file
    private extractFilenameForBlob = pipe(
        map((res: HttpResponse<Blob>) => {
            const contentDisposition = res.headers.get('content-disposition')
            let [match, filename] = contentDisposition.match(/filename="(.+)"/)
            return { blob: res.body, filename: filename }
        }))

    // scaricare il blob come file e ritorna il nome del file
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

    // esporta il PKI e scarica il file
    public exportPki(): Observable<string> {
        return this.http.get(`/api/pki/export`, { responseType: 'blob', observe: 'response' })
            .pipe(
                this.extractFilenameForBlob,
                this.downloadBlob
            )
    }

    // scarica il file del root certificate
    public downloadRoot(): Observable<string> {
        return this.http.get(`/api/pki/download-root`, { responseType: 'blob', observe: 'response' })
            .pipe(
                this.extractFilenameForBlob,
                this.downloadBlob
            )
    }

    // resetta il PKI
    public resetPki(): Observable<boolean> {
        return this.http.delete<boolean>(`/api/pki/reset`)
    }


    // public uploadRoot(crt: UploadSet, key: UploadSet, passphrase: string) {
    //     const formdata = new FormData();
    //     formdata.append('crt', crt.file)
    //     formdata.append('key', key.file)
    //     formdata.append('passphrase', passphrase)

    //     return this.http.post(`/api/pki/import/root`, formdata)
    // }


}

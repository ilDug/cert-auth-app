import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpResponse, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, tap, finalize, catchError } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { NgxToastService } from '@ildug/ngx-toast';



@Injectable()
export class LogInterceptor implements HttpInterceptor {
    constructor(private toast: NgxToastService) { }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        const started = Date.now();

        // extend server response observable with logging
        return next.handle(req)
            .pipe(
                tap(event => {
                    const ok = event instanceof HttpResponse ? 'succeeded' : 'failed'
                    const elapsed = Date.now() - started;
                    const msg = `${req.method} "${req.urlWithParams}" ${ok} in ${elapsed} ms.`;
                    if (event instanceof HttpResponse) console.log(msg, event);
                }),
                catchError((error: HttpErrorResponse) => {
                    this.toast.error(error.error, 10000)
                    // this.toast.error(error.statusText, 10000)
                    return throwError(() => error)
                })
            );

    }
}

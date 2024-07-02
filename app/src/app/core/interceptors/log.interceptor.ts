import { HttpErrorResponse, HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { NgxToastService } from '@ildug/ngx-toast';
import { catchError, tap, throwError } from 'rxjs';

export const logInterceptor: HttpInterceptorFn = (req, next) => {

    const toast = inject(NgxToastService)

    return next(req)
        .pipe(
            tap(event => {
                const ok = event instanceof HttpResponse ? 'succeeded' : 'failed'
                const msg = `${req.method} "${req.urlWithParams}" ${ok} `;
                if (event instanceof HttpResponse) console.log(msg, event);
            }),
            catchError((error: HttpErrorResponse) => {
                console.log('error', error);

                toast.error(error.error, 10000)
                return throwError(() => error)
            })
        )
};

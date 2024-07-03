import { HttpErrorResponse, HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { NgxToastService } from '@ildug/ngx-toast';
import { catchError, tap, throwError } from 'rxjs';

export const logInterceptor: HttpInterceptorFn = (req, next) => {

    const toast = inject(NgxToastService)

    return next(req)
        .pipe(
            tap(event => {
                const msg = `${req.method} "${req.urlWithParams}"`;
                if (event instanceof HttpResponse) console.log(msg, event);
            }),
            catchError((err: HttpErrorResponse) => {
                console.log('response error =====>', err);

                const { headers } = err

                const error = headers.has('X-Error')
                    ? headers.get('X-Error')
                    : err.error.error

                toast.error(error, 10000)
                return throwError(() => err)
            })
        )
};

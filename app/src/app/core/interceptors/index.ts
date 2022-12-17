import { HTTP_INTERCEPTORS } from "@angular/common/http";
import { LogInterceptor } from './log-interceptor';
// import { AuthInterceptor } from './auth-interceptor';
// import { OptimisticConcurrencyControlInterceptor } from './occ-interceptor';


/** Http interceptor providers in outside-in order */
export const httpInterceptorProviders = [
    // { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    // { provide: HTTP_INTERCEPTORS, useClass: OptimisticConcurrencyControlInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: LogInterceptor, multi: true },
];

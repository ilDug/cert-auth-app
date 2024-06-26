import { ApplicationConfig, LOCALE_ID, provideExperimentalZonelessChangeDetection, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';

import { routes } from './app.routes';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient, withInterceptors } from '@angular/common/http';


import { APP_BASE_HREF, PlatformLocation, registerLocaleData } from '@angular/common'
import localeIt from '@angular/common/locales/it';
import { logInterceptor } from './core/interceptors/log.interceptor';
registerLocaleData(localeIt);

export const appConfig: ApplicationConfig = {
    providers: [
        provideExperimentalZonelessChangeDetection(),
        provideRouter(routes, withComponentInputBinding()),
        provideAnimationsAsync(),
        provideHttpClient(withInterceptors([logInterceptor])),
        { provide: LOCALE_ID, useValue: 'it-IT' },
        provideAnimationsAsync(),
        // { provide: APP_BASE_HREF, useFactory: (pl: PlatformLocation) => pl.getBaseHrefFromDOM(), deps: [PlatformLocation] },
    ]
};

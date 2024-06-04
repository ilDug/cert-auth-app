import { ApplicationConfig, LOCALE_ID, provideExperimentalZonelessChangeDetection, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';

import { routes } from './app.routes';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';


import { APP_BASE_HREF, PlatformLocation, registerLocaleData } from '@angular/common'
import localeIt from '@angular/common/locales/it';
registerLocaleData(localeIt);

export const appConfig: ApplicationConfig = {
    providers: [
        provideExperimentalZonelessChangeDetection(),
        // provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes, withComponentInputBinding()),
        provideAnimationsAsync(),
        provideHttpClient(),
        { provide: LOCALE_ID, useValue: 'it-IT' },
        // { provide: APP_BASE_HREF, useFactory: (pl: PlatformLocation) => pl.getBaseHrefFromDOM(), deps: [PlatformLocation] },
    ]
};

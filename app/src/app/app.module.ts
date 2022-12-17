import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CoreModule } from './core/core.module';
import { RouterModule } from '@angular/router';
import { CertificatesComponent } from './certificates/certificates.component';
import { SettingsComponent } from './settings/settings.component';
import { KeysComponent } from './keys/keys.component';
import { AddCertificateComponent } from './certificates/add-certificate/add-certificate.component';
import { CertsListComponent } from './certificates/certs-list/certs-list.component';
import { CertDisplayComponent } from './certificates/cert-display/cert-display.component';
import { ENPOINT } from './core/core.service';
import { APIURL } from '../environments'
import { NgxToastModule } from '@ildug/ngx-toast';
import { httpInterceptorProviders } from './core/interceptors';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
    declarations: [
        AppComponent,
        CertificatesComponent,
        SettingsComponent,
        KeysComponent,
        AddCertificateComponent,
        CertsListComponent,
        CertDisplayComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        CoreModule,
        RouterModule,
        NgxToastModule

    ],
    providers: [
        { provide: ENPOINT, useValue: APIURL },
        httpInterceptorProviders,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }

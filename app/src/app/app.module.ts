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
import { KeysListComponent } from './keys/keys-list/keys-list.component';
import { KeysDisplayComponent } from './keys/keys-display/keys-display.component';
import { NgxConfirmModule } from '@ildug/ngx-confirm';
import { NgxUploadModule } from './core/modules/ngx-upload';
import { ImportPkiComponent } from './settings/import-pki/import-pki.component';
import { ImportRootComponent } from './settings/import-root/import-root.component';

@NgModule({
    declarations: [
        AppComponent,
        CertificatesComponent,
        SettingsComponent,
        KeysComponent,
        AddCertificateComponent,
        CertsListComponent,
        CertDisplayComponent,
        KeysListComponent,
        KeysDisplayComponent,
        ImportPkiComponent,
        ImportRootComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        CoreModule,
        RouterModule,
        NgxToastModule,
        NgxConfirmModule,
        NgxUploadModule

    ],
    providers: [
        { provide: ENPOINT, useValue: APIURL },
        httpInterceptorProviders,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }

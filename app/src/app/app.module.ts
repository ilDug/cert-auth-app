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

@NgModule({
  declarations: [
    AppComponent,
    CertificatesComponent,
    SettingsComponent,
    KeysComponent
  ],
  imports: [
    BrowserModule,
      AppRoutingModule,
      BrowserAnimationsModule,
      CoreModule,
      RouterModule

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

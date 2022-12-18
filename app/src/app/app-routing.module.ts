import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CertDisplayComponent } from './certificates/cert-display/cert-display.component';
import { CertificatesComponent } from './certificates/certificates.component';
import { CertsListComponent } from './certificates/certs-list/certs-list.component';
import { KeysDisplayComponent } from './keys/keys-display/keys-display.component';
import { KeysListComponent } from './keys/keys-list/keys-list.component';
import { KeysComponent } from './keys/keys.component';
import { SettingsComponent } from './settings/settings.component';

const routes: Routes = [
    { path: "", pathMatch: "full", redirectTo: "certificates" },
    {
        path: "certificates", component: CertificatesComponent, children: [
            { path: "", component: CertsListComponent },
            { path: ":cert", component: CertDisplayComponent },
        ]
    },
    {
        path: "keys", component: KeysComponent, children: [
            { path: "", component: KeysListComponent },
            { path: "/:key", component: KeysDisplayComponent }
        ]
    },
    { path: "settings", component: SettingsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

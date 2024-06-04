import { Routes } from '@angular/router';
import { CertificatesComponent } from './certificates/certificates.component';
import { CertsListComponent } from './certificates/certs-list/certs-list.component';
import { SettingsComponent } from './settings/settings.component';
import { KeysComponent } from './keys/keys.component';
import { KeysListComponent } from './keys/keys-list/keys-list.component';
import { KeysDisplayComponent } from './keys/keys-display/keys-display.component';

export const routes: Routes = [
    { path: "", pathMatch: "full", redirectTo: "certificates" },
    {
        path: "certificates",
        component: CertificatesComponent,
        title: "Certificates",
        children: [
            { path: "", component: CertsListComponent },
            { path: ":cert", component: CertsListComponent },
        ]
    },
    {
        path: "keys",
        component: KeysComponent,
        title: "Keys",
        children: [
            { path: "", component: KeysListComponent },
            { path: ":key", component: KeysDisplayComponent }
        ]
    },
    { path: "settings", component: SettingsComponent, title: "Settings" }
];

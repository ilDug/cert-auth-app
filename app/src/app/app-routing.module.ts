import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CertificatesComponent } from './certificates/certificates.component';
import { KeysComponent } from './keys/keys.component';
import { SettingsComponent } from './settings/settings.component';

const routes: Routes = [
    { path: "", pathMatch: "full", redirectTo: "certificates" },
    { path: "certificates", component: CertificatesComponent },
    { path: "keys", component: KeysComponent },
    { path: "settings", component: SettingsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

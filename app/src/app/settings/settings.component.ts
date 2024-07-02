import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ImportPkiComponent } from './import-pki/import-pki.component';
import { ImportRootComponent } from './import-root/import-root.component';
import { NgxToastModule, NgxToastService } from '@ildug/ngx-toast';
import { NgxConfirmDirective } from '@ildug/ngx-confirm';
import { CertificatesService, KeysService, PKIService } from '../core';

@Component({
    selector: 'ca-settings',
    standalone: true,
    imports: [RouterModule, ImportPkiComponent, ImportRootComponent, NgxToastModule, NgxConfirmDirective],
    templateUrl: './settings.component.html',
    styles: ``
})
export class SettingsComponent {
    toast = inject(NgxToastService)
    pki$ = inject(PKIService);
    cert$ = inject(CertificatesService);
    key$ = inject(KeysService);

    downloadPKI() {
        this.pki$.exportPki().subscribe(filename => this.toast.info(`PKI esportata con successo ${filename}`, 3000))
    }

    resetPKI() {
        this.pki$.resetPki().subscribe({
            next: success => {
                this.cert$.refresh();
                this.key$.refresh();
                this.toast.info("reset completato", 3000);
            },
            error: err => this.toast.error("Errore lato server", 3000)
        })
    }
}

import { Component } from '@angular/core';
import { NgxToastService } from '@ildug/ngx-toast';
import { PKIService } from '../pki.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent {
    constructor(
        public pki$: PKIService,
        private toast: NgxToastService
    ) { }


    downloadPki() {
        this.pki$.exportPki().subscribe(filename => this.toast.info(`PKI con successo ${filename}`, 3000))
    }

    downloadRoot() {
        this.pki$.downloadRoot().subscribe(filename => this.toast.info(`ROOT CA scaricata con successo`, 3000))
    }


    resetPki() {
        this.pki$.resetPki().subscribe({
            next: success => this.toast.info("reset completato", 3000),
            error: err => this.toast.error("Errore lato server", 3000)
        })
    }
}

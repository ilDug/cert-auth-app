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
}

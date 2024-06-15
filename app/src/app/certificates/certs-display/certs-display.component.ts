import { Component, effect, inject, input, signal } from '@angular/core';
import { CertificatesService } from '../../core';
import { CommonModule } from '@angular/common';
import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { MatTooltip } from '@angular/material/tooltip';
import { PemDownloadDirective } from '../../core/pem-download.directive';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'ca-certs-display',
  standalone: true,
  imports: [CommonModule,  CdkCopyToClipboard, MatTooltip, PemDownloadDirective, RouterLink],
  templateUrl: './certs-display.component.html',
  styles: ``
})
export class CertsDisplayComponent {

    certs$ = inject(CertificatesService);
    subject = input<string>(null, { alias: "cert" });

    tab = signal<string>("info");

    pem = signal<string>(null);
    info = signal<string>(null);

    #loadEffect = effect(()=>{
        if(!this.subject()) return;
        this.certs$.select(this.subject(), "pem").subscribe(this.pem.set);
        this.certs$.select(this.subject(), "info").subscribe(this.info.set);
    })


    remove() {
        throw new Error("Method not implemented.");
    }

}

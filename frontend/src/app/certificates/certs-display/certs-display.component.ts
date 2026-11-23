import { Component, effect, inject, input, signal } from '@angular/core';
import { CertificatesService } from '../../core';
import { CommonModule } from '@angular/common';
import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { MatTooltip } from '@angular/material/tooltip';
import { PemDownloadDirective } from '../../core/pem-download.directive';
import { Router, RouterLink } from '@angular/router';
import { NgxConfirmDirective } from '@ildug/ngx-confirm';
import { httpResource } from '@angular/common/http';

@Component({
    selector: 'ca-certs-display',
    imports: [CommonModule, CdkCopyToClipboard, MatTooltip, PemDownloadDirective, RouterLink, NgxConfirmDirective],
    templateUrl: './certs-display.component.html',
    styles: ``
})
export class CertsDisplayComponent {
    router = inject(Router);
    certs$ = inject(CertificatesService);
    subject = input<string>(null, { alias: "cert" });

    tab = signal<string>("info");

    pemResource = httpResource.text<string>(() => `/api/display/certificate/pem/${this.subject()}`)
    infoResource = httpResource.text<string>(() => `/api/display/certificate/info/${this.subject()}`)

    pem = this.pemResource.value;
    info = this.infoResource.value;


    remove() {
        this.certs$.remove(this.subject())
            .subscribe(
                () => this.router.navigate(['/certificates']),
            )
    }

}

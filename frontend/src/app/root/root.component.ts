import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { Component, inject, signal } from '@angular/core';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink, RouterOutlet } from '@angular/router';
import { CertificatesService, PKIService } from '../core';

import { toSignal } from '@angular/core/rxjs-interop';
import { PemDownloadDirective } from '../core/pem-download.directive';
import { httpResource } from '@angular/common/http';

@Component({
    selector: 'ca-root',
    imports: [RouterLink, RouterOutlet, CdkCopyToClipboard, MatTooltip, PemDownloadDirective],
    templateUrl: './root.component.html',
    styles: ``
})
export class RootComponent {
    certs$ = inject(CertificatesService);
    pki$ = inject(PKIService);

    pemResource = httpResource.text<string>(() => `/api/display/certificate/pem/ca`);
    infoResource = httpResource.text<string>(() => `/api/display/certificate/info/ca`);

    pem = this.pemResource.value;
    info = this.infoResource.value;


    downloadRoot() {
        this.pki$.downloadRoot().subscribe();
    }
}

import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { Component, inject, signal } from '@angular/core';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink, RouterOutlet } from '@angular/router';
import { CertificatesService, PKIService } from '../core';
import { CommonModule } from '@angular/common';
import { toSignal } from '@angular/core/rxjs-interop';
import { PemDownloadDirective } from '../core/pem-download.directive';

@Component({
    selector: 'ca-root',
    standalone: true,
    imports: [RouterLink, RouterOutlet, CdkCopyToClipboard, MatTooltip, CommonModule, PemDownloadDirective],
    templateUrl: './root.component.html',
    styles: ``
})
export class RootComponent {
    certs$ = inject(CertificatesService);
    pki$ = inject(PKIService);

    pem = toSignal<string>(this.certs$.select("ca", "pem"));
    info = toSignal<string>(this.certs$.select("ca", "info"));


    downloadRoot() {
        this.pki$.downloadRoot().subscribe();
    }
}

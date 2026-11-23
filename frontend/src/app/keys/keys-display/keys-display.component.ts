import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { CommonModule } from '@angular/common';
import { Component, computed, input, signal } from '@angular/core';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink } from '@angular/router';
import { PemDownloadDirective } from '../../core/pem-download.directive';
import { httpResource } from '@angular/common/http';

@Component({
    selector: 'ca-keys-display',
    imports: [CommonModule, CdkCopyToClipboard, MatTooltip, PemDownloadDirective, RouterLink],
    templateUrl: './keys-display.component.html',
    styles: ``
})
export class KeysDisplayComponent {
    subject = input<string>(null, { alias: "key" });
    tab = signal<string>("info");

    privatePemResource = httpResource(() => `/api/display/privatekey/pem/${this.subject()}`)
    publicPemResource = httpResource(() => `/api/display/publickey/pem/${this.subject()}`)
    keyInfoResource = httpResource(() => `/api/display/privatekey/info/${this.subject()}`)

    PENDING = computed(() =>
        this.privatePemResource.isLoading()
        || this.publicPemResource.isLoading()
        || this.keyInfoResource.isLoading()
    )

    privateKeyPem = signal<string>(null);
    keyInfo = signal<string>(null);
    publicKeyPem = signal<string>(null);
}

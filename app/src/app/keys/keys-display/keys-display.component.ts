import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { CommonModule } from '@angular/common';
import { Component, effect, inject, input, signal } from '@angular/core';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink } from '@angular/router';
import { PemDownloadDirective } from '../../core/pem-download.directive';
import { KeysService } from '../../core';

@Component({
    selector: 'ca-keys-display',
    standalone: true,
    imports: [CommonModule, CdkCopyToClipboard, MatTooltip, PemDownloadDirective, RouterLink],
    templateUrl: './keys-display.component.html',
    styles: ``
})
export class KeysDisplayComponent {
    keys$ = inject(KeysService);
    subject = input<string>(null, { alias: "key" });

    tab = signal<string>("info");

    privPem = signal<string>(null);
    info = signal<string>(null);
    pubPem = signal<string>(null);

    #loadEffect = effect(() => {
        if (!this.subject()) return;
        this.keys$.privateKey(this.subject(), "pem").subscribe(this.privPem.set);
        this.keys$.privateKey(this.subject(), "info").subscribe(this.info.set);
        this.keys$.publicKey(this.subject(), "pem").subscribe(this.pubPem.set);
    })
}

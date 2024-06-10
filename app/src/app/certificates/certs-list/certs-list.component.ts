import { Component, inject } from '@angular/core';
import { CertificatesService } from '../../core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'ca-certs-list',
    standalone: true,
    imports: [CommonModule, RouterModule],
    templateUrl: './certs-list.component.html',
    styles: ``
})
export class CertsListComponent {
    certs$ = inject(CertificatesService);
}

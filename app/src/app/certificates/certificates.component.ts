import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { filter, switchMap } from 'rxjs';
import { CertificatesService } from '../certificates.service';
import { CertificateSigningRequest } from '../core/classes/certificate.class';
import { AddCertificateComponent } from './add-certificate/add-certificate.component';

@Component({
  selector: 'app-certificates',
  templateUrl: './certificates.component.html',
  styleUrls: ['./certificates.component.scss']
})
export class CertificatesComponent {
    constructor(
        private dialog: MatDialog,
        private certs$: CertificatesService,
    ) { }

    addCertificate() {
        this.dialog.open(AddCertificateComponent, { hasBackdrop: false, minWidth: "50%" })
            .afterClosed()
            .pipe(
                filter(_ => !!_),
                switchMap((csr: CertificateSigningRequest) => this.certs$.add(csr))
            )
            .subscribe()
    }
}

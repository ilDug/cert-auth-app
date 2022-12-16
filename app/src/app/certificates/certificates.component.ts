import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddCertificateComponent } from './add-certificate/add-certificate.component';

@Component({
  selector: 'app-certificates',
  templateUrl: './certificates.component.html',
  styleUrls: ['./certificates.component.scss']
})
export class CertificatesComponent {
    constructor(
        private dialog: MatDialog
    ) { }

    addCertificate() {
        this.dialog.open(AddCertificateComponent, { hasBackdrop: false, minWidth: "50%" })
    }
}

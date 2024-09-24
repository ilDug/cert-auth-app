import { Component, inject } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { AddCertificateDialogComponent } from '../certificates/add-certificate-dialog/add-certificate-dialog.component';
import { CertificatesService } from '../core';

@Component({
  selector: 'ca-certificates',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  templateUrl: './certificates.component.html',
  styles: ``
})
export class CertificatesComponent {
    private dialog = inject(MatDialog);
    certs$ = inject(CertificatesService);

    addCertificate(){
        this.dialog.open(AddCertificateDialogComponent, { hasBackdrop: false, minWidth: "50vw" })
    }

    reload() {
        this.certs$.refresh();
    }
}

import { Component, inject } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { CertificatesService } from '../core';
import { AddCertificateDialogComponent } from '../certificate/add-certificate-dialog/add-certificate-dialog.component';

@Component({
  selector: 'ca-certificates',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  templateUrl: './certificates.component.html',
  styles: ``
})
export class CertificatesComponent {
    private dialog = inject(MatDialog);

    addCertificate(){
        this.dialog.open(AddCertificateDialogComponent, { hasBackdrop: false, minWidth: "50vw" })
    }
}

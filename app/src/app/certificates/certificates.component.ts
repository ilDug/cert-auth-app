import { Component, inject } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
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
    private certs$ = inject(CertificatesService);

    addCertificate(){

    }
}

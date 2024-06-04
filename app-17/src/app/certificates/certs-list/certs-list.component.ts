import { Component } from '@angular/core';
import { CertificatesService } from 'src/app/certificates.service';

@Component({
  selector: 'app-certs-list',
  templateUrl: './certs-list.component.html',
  styleUrls: ['./certs-list.component.scss']
})
export class CertsListComponent {
    constructor(
        public certs$: CertificatesService
    ) { }


}

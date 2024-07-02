import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { NgxErrorsModule } from '@ildug/ngx-errors';
import { CertificateSigningRequest, CertificatesService } from '../../core';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { NgxToastService } from '@ildug/ngx-toast';

@Component({
    selector: 'ca-add-certificate-dialog',
    standalone: true,
    imports: [MatDialogModule, ReactiveFormsModule, CommonModule, NgxErrorsModule, MatCheckboxModule],
    templateUrl: './add-certificate-dialog.component.html',
    styles: ``
})
export class AddCertificateDialogComponent {
    toast = inject(NgxToastService);
    #ref = inject(MatDialogRef);
    cert$ = inject(CertificatesService);
    min: number = 2;
    max: number = 1825;

    form = new FormGroup({
        subject: new FormControl('', [Validators.required]),
        days: new FormControl(360, [Validators.required, Validators.min(this.min), Validators.max(this.max)]),
        wildcard: new FormControl(true),
    });


    addCertificate() {

        if (this.form.invalid) return;

        const { subject, days, wildcard } = this.form.value;
        const csr = new CertificateSigningRequest({ subject, days });
        if (wildcard) {
            csr.alt_names.push(`*.${subject}`);
        }

        this.cert$.add(csr).subscribe(() => {
            this.toast.info(`${subject} certificate added`, 5000);
            this.#ref.close();
        });
    }



}


import { Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgxErrorsModule } from '@ildug/ngx-errors';
import { CertificatesService } from '../../core';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { NgxToastService } from '@ildug/ngx-toast';
import { CertificateSigningRequest } from '../../core/interfaces';
import { form, FormField, required, min, max } from '@angular/forms/signals';


interface AddCertificateFormModel {
    subject: string;
    days: number;
    wildcard: boolean;
}

@Component({
    selector: 'ca-add-certificate-dialog',
    imports: [MatDialogModule, ReactiveFormsModule, NgxErrorsModule, MatCheckboxModule, FormField],
    templateUrl: './add-certificate-dialog.component.html',
    styles: ``
})
export class AddCertificateDialogComponent {
    toast = inject(NgxToastService);
    #ref = inject(MatDialogRef);
    cert$ = inject(CertificatesService);

    model = signal<AddCertificateFormModel>({
        subject: '',
        days: 360,
        wildcard: true
    });

    form = form(this.model, (schema) => {
        required(schema.subject, { message: 'Subject is required' });
        min(schema.days, 2, { message: 'Minimum value is 2' });
        max(schema.days, 1825, { message: 'Maximum value is 1825' });
    })


    addCertificate(event: SubmitEvent) {
        event.preventDefault();

        const { subject, days, wildcard } = this.model();
        const csr: CertificateSigningRequest = { subject, days, alt_names: [] }

        if (wildcard) {
            csr.alt_names.push(`*.${subject}`);
        }

        this.cert$.add(csr).subscribe(() => {
            this.toast.info(`${subject} certificate added`, 5000);
            this.#ref.close();
        });
    }



}

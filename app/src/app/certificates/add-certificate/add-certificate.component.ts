import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { CertificateSigningRequest } from 'src/app/core/classes/certificate.class';

@Component({
    selector: 'app-add-certificate',
    templateUrl: './add-certificate.component.html',
    styleUrls: ['./add-certificate.component.scss']
})
export class AddCertificateComponent implements OnInit {

    constructor(
        private dialogRef: MatDialogRef<AddCertificateComponent>
    ) { }

    form: FormGroup

    ngOnInit(): void {
        const controls = {
            subject: new FormControl(null, [Validators.required]),
            wildcard: new FormControl(true),
            days: new FormControl(1825, [Validators.min(2)])
        }

        this.form = new FormGroup(controls)
    }


    save() {
        if (this.form.invalid) return;

        let { subject, wildcard, days } = this.form.value
        let csr = new CertificateSigningRequest({ subject: subject, days: days })
        if (wildcard)
            csr.alt_names.push(`*.${subject}`)

        this.dialogRef.close(csr)
    }

}

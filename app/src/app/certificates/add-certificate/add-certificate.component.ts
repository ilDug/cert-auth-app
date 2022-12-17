import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
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
            subject: new FormControl(null),
            wildcard: new FormControl(true)
        }

        this.form = new FormGroup(controls)
    }


    save() {
        if (this.form.invalid) return;

        let { subject, wildcard } = this.form.value
        let csr = new CertificateSigningRequest({ subject: subject })
        if (wildcard)
            csr.alt_names.push(`*.${subject}`)

        this.dialogRef.close(csr)
    }

}

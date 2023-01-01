import { Component, ViewChild } from '@angular/core';
import { NgxToastService } from '@ildug/ngx-toast';
import { pipe, tap } from 'rxjs';
import { UploadSet, UPLOAD_ENDPOINT, UPLOAD_STRATEGY } from 'src/app/core/modules/ngx-upload';
import { NgxUploadListDirective } from 'src/app/core/modules/ngx-upload/ngx-upload-list.directive';
import { NgxUploadService } from 'src/app/core/modules/ngx-upload/ngx-upload.service';
import { PKIService } from 'src/app/pki.service';
import { APIURL } from 'src/environments.prod.';

@Component({
    selector: 'app-import-root',
    templateUrl: './import-root.component.html',
    styleUrls: ['./import-root.component.scss'],
    providers: [
        { provide: UPLOAD_ENDPOINT, useValue: APIURL + "/pki/import/root" },
        { provide: UPLOAD_STRATEGY, useValue: "FORMDATA" },
        NgxUploadService
    ]

})
export class ImportRootComponent {

    constructor(
        private toast: NgxToastService,
        private pki$: PKIService
    ) { }

    @ViewChild('flcrt', { static: true }) certList: NgxUploadListDirective
    @ViewChild('flkey', { static: true }) keysList: NgxUploadListDirective

    public passphrase: string

    onError(e) {
        this.toast.error(e, 3000)
    }

    submit() {
        const crt: UploadSet = this.certList.files[0]
        const key: UploadSet = this.keysList.files[0]

        if (!this.passphrase || !crt || !key) return;

        this.pki$.uploadRoot(crt, key, this.passphrase)
            .pipe(
                tap(_ => this.certList.markAsUploaded()),
                tap(_ => this.keysList.markAsUploaded()),
            )
            .subscribe({
                next: success => this.toast.info("Evvai,  importazione avvenuta", 3000),
                error: err => this.toast.error(err, 3000),
            })
    }

}

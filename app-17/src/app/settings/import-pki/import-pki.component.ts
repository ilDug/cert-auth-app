import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { NgxToastService } from '@ildug/ngx-toast';
import { UPLOAD_ENDPOINT, UPLOAD_STRATEGY } from 'src/app/core/modules/ngx-upload';
import { NgxUploadListDirective } from 'src/app/core/modules/ngx-upload/ngx-upload-list.directive';
import { NgxUploadService } from 'src/app/core/modules/ngx-upload/ngx-upload.service';
import { PKIService } from 'src/app/pki.service';
import { APIURL } from 'src/environments';

@Component({
    selector: 'app-import-pki',
    templateUrl: './import-pki.component.html',
    styleUrls: ['./import-pki.component.scss'],
    providers: [
        { provide: UPLOAD_ENDPOINT, useValue: APIURL + "/pki/import/archive" },
        { provide: UPLOAD_STRATEGY, useValue: "FORMDATA" },
        NgxUploadService
    ]
})
export class ImportPkiComponent {
    constructor(
        public pki$: PKIService,
        public toast: NgxToastService
    ) { }

    @ViewChild('fl', { static: true }) fl: NgxUploadListDirective

    import() {
        if (this.fl.empty) return;
        if (this.fl.length > 1) return;
        this.fl.uploadAll()
    }

    onError(e) {
        this.toast.error(e, 3000)
    }

}

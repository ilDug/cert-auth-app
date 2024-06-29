import { CommonModule, } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { UploadModule, UploadOptions, UploadService } from '../../core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatButtonModule } from '@angular/material/button';
import { NgxToastService } from '@ildug/ngx-toast';

@Component({
    selector: 'ca-import-pki',
    standalone: true,
    imports: [CommonModule, UploadModule, MatProgressBarModule],
    templateUrl: './import-pki.component.html',
    styles: ``,
    providers: [UploadService]
})
export class ImportPkiComponent {
    private toast = inject(NgxToastService);

    uploadOptions: UploadOptions = new UploadOptions({
        validExtensions: ["zip"],
        maxFileSize: 4000000,
        maxFilesNum: 1
    })

    error = signal<string>(null);

    onError(e) {
        this.error.set(e);
        setTimeout(() => this.error.set(null), 5000);
    }

    onLoad(e) {
        console.log(e);
    }

    onComplete(e) {
        console.log('Upload complete', e);
        this.toast.info('Upload complete', 5000);
    }
}

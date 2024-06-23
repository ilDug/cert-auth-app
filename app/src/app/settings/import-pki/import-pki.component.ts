import { CommonModule, } from '@angular/common';
import { Component, signal } from '@angular/core';
import { UploadModule, UploadOptions, UploadService } from '../../core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatButtonModule } from '@angular/material/button';

@Component({
    selector: 'ca-import-pki',
    standalone: true,
    imports: [CommonModule, UploadModule, MatProgressBarModule, MatButtonModule],
    templateUrl: './import-pki.component.html',
    styles: ``,
    providers: [UploadService]
})
export class ImportPkiComponent {

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
}

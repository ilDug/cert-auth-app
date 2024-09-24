import { Directive, inject, input } from '@angular/core';
import { UploadService } from './upload.service';
import { UploadItem } from './upload-item';

@Directive({
    selector: '[uploadRemoveItem]',
    standalone: true,
    host: {
        '(click)': 'removeFileFromList()',
        '[style.cursor]': '"pointer"',
    }
})
export class UploadRemoveDirective {

    #upload = inject(UploadService);

    item = input.required<UploadItem>({ alias: 'uploadRemoveItem' });

    removeFileFromList() {
        console.log('Removing file from list', this.item());

        this.#upload.removeFileFromList(this.item());
        return false;
    }

}

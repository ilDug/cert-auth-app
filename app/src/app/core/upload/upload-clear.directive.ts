import { Directive, inject, input, output } from '@angular/core';
import { UploadService } from './upload.service';

@Directive({
    selector: '[uploadClear]',
    standalone: true,
    host: {
        '(click)': 'clearItemList()',
        '[style.cursor]': '"pointer"',
    }
})
export class UploadClearDirective {

    #upload$ = inject(UploadService);

    clearItemList() {
        this.#upload$.clearItemList();
        return false;
    }
}
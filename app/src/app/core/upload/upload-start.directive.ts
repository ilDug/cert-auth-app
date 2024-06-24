import { Directive, inject, output } from '@angular/core';
import { UploadService } from './upload.service';

@Directive({
  selector: '[uploadStart]',
  standalone: true, 
  host: {
    '(click)': 'startUpload()',
    '[style.cursor]': '"pointer"',
  }
})
export class UploadStartDirective {

    #upload = inject(UploadService);
    load = output<any>();
    complete = output();
    fail = output<string>();

    startUpload() {
        this.#upload.uploadAll()
            .subscribe({
                next: res => this.load.emit(res),
                error: err => this.fail.emit(err),
                complete: () => this.complete.emit()
            })
    }

}

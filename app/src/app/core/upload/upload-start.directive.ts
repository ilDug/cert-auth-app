import { Directive, inject, input, output } from '@angular/core';
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


    waitAtTheEnd = input(false);
    removeAfterDelay = input<number>(null);

    startUpload() {
        this.#upload.uploadAll(this.waitAtTheEnd())
            .subscribe({
                next: res => this.load.emit(res),
                error: err => this.fail.emit(err),
                complete: () => {
                    this.complete.emit();
                    if (this.removeAfterDelay() === null) return;
                    setTimeout(() => {
                        this.#upload.items()
                            .filter(item => item.completed())
                            .forEach(item => this.#upload.removeFileFromList(item))
                    }, this.removeAfterDelay())
                }
            })
    }

}

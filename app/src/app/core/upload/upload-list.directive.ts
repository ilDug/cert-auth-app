import { Directive, computed, effect, inject, input, output, signal, viewChildren } from '@angular/core';
import { UploadService } from './upload.service';
import { UploadItemDirective } from './upload-item.directive';
import { Observable, merge, of } from 'rxjs';

@Directive({
    selector: '[UploadList]',
    exportAs: 'UploadList',
    standalone: true
})
export class UploadListDirective {

    upload$ = inject(UploadService)

    uploaded = output<any>();

    files = signal<File[]>([]);
    length = computed(() => this.files().length);
    empty = computed(() => this.length() === 0);

    endpoint = input.required<string>();
    #endpointEffect = effect(() => this.upload$.endpoint = this.endpoint());

    items = viewChildren(UploadItemDirective);

    requests = computed<Observable<string>[]>(() => {
        console.log('files', this.files());
        return this.items()
            .filter(item => !item.completed)
            .map(item => this.upload$.upload(item));
    });

    add(file: File) {
        this.files.update(files => [...files, file]);
    }

    remove(file: File) {
        this.files.update(files => files.filter(f => f !== file));
    }

    upload() {
        /** emette uno alla volta */
        const s = merge(...this.requests())
            .subscribe(results => this.uploaded.emit(results));

        /** emette alla  fine */
        // const s = forkJoin(uploadRequests).subscribe(results => this.uploadEvent.emit(results));
    }
}

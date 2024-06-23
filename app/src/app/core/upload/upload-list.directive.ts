import { AfterViewInit, Directive, QueryList, ViewChildren, computed, effect, inject, input, output, signal, viewChildren } from '@angular/core';
import { UploadService } from './upload.service';
import { UploadItemDirective } from './upload-item.directive';
import { Observable, Subject, merge, of } from 'rxjs';

@Directive({
    selector: '[UploadList]',
    exportAs: 'UploadList',
    standalone: true
})
export class UploadListDirective {

    #upload$ = inject(UploadService);
    // upload = new Subject();

    files = this.#upload$.files; // SIGNAL<File[]>([]);
    items = this.#upload$.items; // SIGNAL<UploadItem[]>([]);
    
    length = computed(() => this.files().length);
    empty = computed(() => this.length() === 0);

    endpoint = input.required<string>();
    #endpointEffect = effect(() => this.#upload$.endpoint = this.endpoint());

    clear() {
        this.#upload$.clearFileList();
    }
}


// items = viewChildren(UploadItemDirective);

// requests = computed<Observable<string>[]>(() => {
//     console.log('files', this.files());
//     return this.items()
//         .filter(item => !item.completed)
//         .map(item => this.upload$.upload(item));
// });


/** emette uno alla volta */
// const s = merge(...this.requests())
//     .subscribe(results => this.uploaded.emit(results));

/** emette alla  fine */
// const s = forkJoin(uploadRequests).subscribe(results => this.uploadEvent.emit(results));

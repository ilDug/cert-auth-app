import { Directive, computed, effect, inject, input } from '@angular/core';
import { UploadService } from './upload.service';

@Directive({
    selector: '[UploadList]',
    exportAs: 'UploadList',
    standalone: true
})
export class UploadListDirective {

    #upload$ = inject(UploadService);
    // upload = new Subject();

    // files = this.#upload$.files; // SIGNAL<File[]>([]);
    items = this.#upload$.items; // SIGNAL<UploadItem[]>([]);
    length = computed(() => this.items().length);
    empty = computed(() => this.length() === 0);

    endpoint = input.required<string>();
    #endpointEffect = effect(() => this.#upload$.endpoint = this.endpoint());

    clear() {
        this.#upload$.clearItemList();
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

import { Directive, computed, effect, inject, input, output, signal, viewChildren } from '@angular/core';
import { UploadService } from './upload.service';
import { UploadItemDirective } from './upload-item.directive';
import { Observable, Subject, merge, of } from 'rxjs';

@Directive({
    selector: '[UploadList]',
    exportAs: 'UploadList',
    standalone: true
})
export class UploadListDirective {


    upload$ = inject(UploadService)
    upload = new Subject();

    files = signal<File[]>([]);
    length = computed(() => this.files().length);
    empty = computed(() => this.length() === 0);

    // numero massimo di file ammessi 
    filesLimit = input<number>(1); 

    endpoint = input.required<string>();
    #endpointEffect = effect(() => this.upload$.endpoint = this.endpoint());

    // aggiiunge un file alla lista
    add(file: File) {
        if (this.length() >= this.filesLimit()) {
            throw new Error(`Numero massimo di file raggiunto. MAX: ${this.filesLimit()}`);
        }
        this.files.update(files => [...files, file]);
    }

    // elimina tutti i file dalla lista
    clear() {
        this.files.set([]);
    }

    // rimuove un file dalla lista
    remove(file: File) {
        this.files.update(files => files.filter(f => f !== file));
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

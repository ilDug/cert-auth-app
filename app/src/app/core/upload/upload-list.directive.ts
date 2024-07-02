import { Directive, computed, effect, inject, input } from '@angular/core';
import { UploadService } from './upload.service';

@Directive({
    selector: '[UploadList]',
    exportAs: 'UploadList',
    standalone: true
})
export class UploadListDirective {

    // UploadService instance
    #upload$ = inject(UploadService);

    // SIGNAL<UploadItem[]>([]) from UploadService
    items = this.#upload$.items;

    // the number of items in the list
    length = computed(() => this.items().length);

    // true if the list is empty
    empty = computed(() => this.length() === 0);

    // the server endpoint for the upload
    endpoint = input.required<string>();

    // update the endpoint in the UploadService when the directive's endpoint input changes
    #endpointEffect = effect(() => this.#upload$.endpoint = this.endpoint());

    // add an item to the list of uploads in the UploadService
    clear() {
        this.#upload$.clearItemList();
    }
}

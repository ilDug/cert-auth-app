import { Directive, forwardRef, HostListener, Inject } from '@angular/core';
import { NgxUploadItemDirective } from './ngx-upload-item.directive';

@Directive({
    selector: '[NgxUploadRemove]'
})
export class NgxUploadRemoveDirective {

    constructor(
        @Inject(forwardRef(() => NgxUploadItemDirective)) private fileItem: NgxUploadItemDirective
    ) { }


    @HostListener('click', ['$event'])
    remove(e: Event) {
        e.stopPropagation();
        e.preventDefault();
        this.fileItem.remove.emit()
        this.fileItem.removeItemFromInjectedList(0);
    }
}

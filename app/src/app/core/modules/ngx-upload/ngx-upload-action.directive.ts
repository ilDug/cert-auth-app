import { Directive, forwardRef, HostListener, Inject } from '@angular/core';
import { NgxUploadListDirective } from './ngx-upload-list.directive';

@Directive({
    selector: '[NgxUploadAction]'
})
export class NgxUploadActionDirective {

    constructor(
        @Inject(forwardRef(() => NgxUploadListDirective)) private fileList: NgxUploadListDirective
    ) { }


    @HostListener('click', ['$event'])
    upload(e: Event) {
        e.stopPropagation();
        e.preventDefault();
        this.fileList.uploadAll()
    }
}

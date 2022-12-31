import { Directive, EventEmitter, forwardRef, Inject, Input, Output } from '@angular/core';
import { NgxUploadListDirective } from './ngx-upload-list.directive';
import { UploadSet } from './uploas-set';

@Directive({
    selector: '[NgxUploadItem]'
})
export class NgxUploadItemDirective {

    constructor(
        @Inject(forwardRef(() => NgxUploadListDirective)) private fileList: NgxUploadListDirective
    ) { }

    public errorMessage: string;
    public progress: number = 0;
    // public color: string = "primary";

    public status: "PENDING" | "SUCCESS" | "FAIL" = "PENDING";
    public pending: boolean = true;
    public completed: boolean = false;
    public invalid: boolean = false;


    @Input('ngxUploadItem') ngxUploadItem: UploadSet;

    get file() { return this.ngxUploadItem }


    /** viene emesso quando l'immgine è stata caricata correttamente sul server */
    @Output() loaded = new EventEmitter();
    @Output() remove = new EventEmitter();



    ngOnChanges() {
        if (this.ngxUploadItem) {
            this.ngxUploadItem.progress
                .asObservable()
                .subscribe({
                    next: p => (this.progress = p),
                    error: err => this.onLoadError(err),
                    complete: () => this.onLoadComplete()
                });
        }
    }



    public onLoadError(err) {
        // this.color = "warn";
        this.invalid = true;
        this.pending = false;
        this.status = "FAIL"
        this.errorMessage = err;
    }



    public onLoadComplete() {
        // this.color = "accent";
        this.pending = false;
        this.completed = true;
        this.status = "SUCCESS";
        this.loaded.emit();
        this.removeItemFromInjectedList();
    }


    removeItemFromInjectedList(timeout = 10000) {
        setTimeout(() => this.fileList.remove(this.ngxUploadItem), timeout);
    }

}

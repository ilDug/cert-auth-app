import { Directive, EventEmitter, HostListener, OnDestroy, Output } from '@angular/core';
import { Subscription, Observable, merge } from 'rxjs';
import { NgxUploadService } from './ngx-upload.service';
import { UploadSet } from './uploas-set';

@Directive({
    selector: '[NgxUploadList]'
})
export class NgxUploadListDirective implements OnDestroy {

    constructor(
        private uploadService: NgxUploadService
    ) { }

    public files: UploadSet[] = [];
    get length(): number { return this.files.length }
    get empty(): boolean { return this.length === 0 }
    private sub: Subscription[] = []

    @HostListener('click', ['$event']) prevent(e) { e.stopPropagation(); e.preventDefault(); }
    @Output('upload') uploadEvent = new EventEmitter()


    add(us: UploadSet) {
        console.log("ngxUploadFileList, aggiunto file")
        this.files.push(us)
    }


    remove(us: UploadSet) {
        console.log("ngxUploadFileList, rimosso file")
        const i = this.files.indexOf(us)
        if (i > -1) this.files.splice(i, 1)
    }


    uploadAll() {
        console.log(("starting upload All"));

        let uploadRequests: Observable<string>[] = []
        for (let us of this.files) {
            /** se è già stato caricato o s c'è stato un errore non lo ricarica di nuovo */
            if (us.completed) continue;

            const req = this.uploadService.upload(us)
            uploadRequests.push(req)
        }

        /** emette uno alla volta */
        const s = merge(...uploadRequests).subscribe(results => this.uploadEvent.emit(results));

        /** emette alla  fine */
        // const s = forkJoin(uploadRequests).subscribe(results => this.uploadEvent.emit(results));
        this.sub.push(s)
    }

    markAsUploaded() {
        for (let us of this.files) {
            us.completed = true;
            us.progress.complete()
        }
    }

    // uploadCustom(endpoint: string) {
    //     /** solo il primo file della lista */
    //     const s = this.uploadService
    //         .uploadCustom(this.files[0], endpoint)
    //         .subscribe(results => this.uploadEvent.emit([results]))

    //     this.sub.push(s)
    // }

    ngOnDestroy() { this.sub.forEach(s => s.unsubscribe()) }
}

import { NgModule } from '@angular/core';
import { UploadAreaDirective } from './upload-area.directive';
import { UploadListDirective } from './upload-list.directive';
import { UploadClearDirective } from './upload-clear.directive';
import { UploadStartDirective } from './upload-start.directive';
import { UploadRemoveDirective } from './upload-remove.directive';


@NgModule({
    imports: [
        UploadAreaDirective,
        UploadListDirective,
        UploadClearDirective,
        UploadStartDirective,
        UploadRemoveDirective
    ],
    exports: [
        UploadAreaDirective,
        UploadListDirective,
        UploadClearDirective,
        UploadStartDirective,
        UploadRemoveDirective
    ]
})
export class UploadModule { }

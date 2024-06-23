import { NgModule } from '@angular/core';
import { UploadAreaDirective } from './upload-area.directive';
import { UploadItemDirective } from './upload-item.directive';
import { UploadListDirective } from './upload-list.directive';


@NgModule({
    imports: [
        UploadAreaDirective,
        UploadItemDirective,
        UploadListDirective
    ],
    exports: [
        UploadAreaDirective, 
        UploadItemDirective,
        UploadListDirective
    ]
})
export class UploadModule { }

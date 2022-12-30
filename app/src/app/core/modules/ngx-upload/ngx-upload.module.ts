import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxUploadAreaDirective } from './ngx-upload-area.directive';
import { NgxUploadItemDirective } from './ngx-upload-item.directive';
import { NgxUploadItemRemoveDirective } from './ngx-upload-item-remove.directive';
import { NgxUploadListDirective } from './ngx-upload-list.directive';
import { NgxUploadActionDirective } from './ngx-upload-action.directive';



@NgModule({
  declarations: [
    NgxUploadAreaDirective,
    NgxUploadItemDirective,
    NgxUploadItemRemoveDirective,
    NgxUploadListDirective,
    NgxUploadActionDirective
  ],
  imports: [
    CommonModule
  ],
  exports: [
    NgxUploadAreaDirective,
    NgxUploadItemDirective,
    NgxUploadItemRemoveDirective,
    NgxUploadListDirective,
    NgxUploadActionDirective
  ]
})
export class NgxUploadModule { }

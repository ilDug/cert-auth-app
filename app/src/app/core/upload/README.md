# NGX-UPLOAD

upload file to server, using angular v18.

## Installation

Install the package `@ildug/ngx-upload` via **npm**:

```shell
npm install @ildug/ngx-upload --save
```

This command downloads and installs the package and its dependencies into your project.

Once the installation is complete, you can start using `@ildug/ngx-upload `in your project.

Please note that you may need to configure and import the package according to its documentation to ensure it works properly in your application.

## Add the module to Component

This module can be used in standalone Angular components. 
It provides the necessary functionality and dependencies for the component to work independently.


Usage:

1. Import this module in the component's module file.
2. Add the module to the `imports` array of the component's module.
3. Use the component in your template by adding its selectors.
4. Add the service to `providers` list. Each component must specify an instance of `NgxUploadService`, allowing you to add more than one (with different endpoints).

Example:

```typescript
import { NgxUploadModule, NgxUploadOptions, NgxUploadService } from '@ildug/ngx-upload';

@Component({
  ...
  imports: [
    NgxUploadModule
  ],
  providers: [
    NgxUploadService
  ]
  ...
})
export class MyComponent { 
    ... 

    uploadOptions: UploadOptions = new UploadOptions({
        validExtensions: ["zip"],
        maxFileSize: 4000000,
        maxFilesNum: 2
    })

    ... 
}
```

## Directives

### NgxUploadArea

Add the directive `UploadArea` into html template.

```html
<div
    class="drop-area t-center grid-1"
    UploadArea
    [uploadOptions]="myOptions"
    (error)="onError($event)"
>
    <p class="t-main">drop pki archive (or click to select)</p>
</div>
```

This area can be used to load files.
It can be dropped or selected with **file manager** , by clicking the area.

When you drag a file over the area, the class `.drag-hover` and the attribute `hover` will be automatically added.

```css
.drop-area[hover],
.drop-area.drag-hover {
    background: var(--my-hover-bg-color);
}
```

-   `UploadArea` [*directive*]: set the element as drop area where to load the files.
-   `[uploadOptions]` [*@Input, optional*]: Some options can be passed to check the behaviour of uploader.
    -   `validExtensions` [*string array*]: the allowed extensione. default: _["jpg", "jpeg", "png", "tiff", 'pdf']_
    -   `maxFileSize` [*number*]: the max size of each file in bytes.
    -   `maxFilesNum` [*number, default=1*]: How many file to upload.
-   `(error)` [*@Output, optional*]: Emits the error message when the file does not respect the rules defined in **[uploadOptions]**.

## NgxUploadList

Add the directive `UploadArea` into html template.

```html
<div class="upload-list" #myList="UploadList" UploadList endpoint="/api/pki/import/archive">
    @for (item of myList.items(); track $index) { ... item element ... }
</div>
```

-   `UploadList` [*directive*]: set the directive to element. define also the template variable #myList.
-   `endpoint` [*@Input*]: set the directive to element. define also the template variable #myList.
-   `clear()` [*method*]: clear the list of items.
-   `items` [*property, Signal\<item[]>*]: the list of items to iterate.
-   `length` [*property, Signal\<number>*]: number of items in the list.
-   `empty` [*property, Signal\<boolean>*]: true if the list is empty.

### UploadItem properties

-  `filename` [*Signal\<string>*] : the  original file name
-  `size` [*Signal\<number>*]: the file size in kB
-  `src` [*Signal\<base64 string>*]: a base64 string to be used if image thumbnail
-  `progress` [*Signal\<number>*]: the percentage of loading 
-  `text` [*Signal\<string>*]: the content of file as text (binary file throws error)
-  `error` [*Signal\<string>*]: the error message returned from server
-  `status` [*Signal\<"PENDING" | "SUCCESS" | "FAIL">*] : the loading status 
-  `pending` [*Signal\<boolean>*] : boolean that refers to status property
-  `completed` [*Signal\<boolean>*]  : boolean that refers to status property
-  `failed` [*Signal\<boolean>*]  : boolean that refers to status property

```html
<div class="grid-1 g-3 pos-relative mb-3 bg-gray p-3 br-6">
    <i class="fa-2x fa-duotone fa-file"></i>

    <span>{{ item.filename() }}</span>
    <span>{{ item.size() }} kB</span>

    <div class="flex g-3">
        @switch (item.status()) { @case("SUCCESS") {
            <i class="fa-lg fa-regular fa-check t-goal"></i>
        } @case("PENDING") {
            <i class="fa-lg fa-regular fa-sync t-charm fa-spin"></i>
        } @case("FAIL") {
            <i class="fa-lg fa-regular fa-exclamation-triangle t-warn"></i>
        } }
        <mat-progress-bar mode="determinate" [value]="item.progress()"></mat-progress-bar>
    </div>

    <span class="t-error">{{ item.failed() ? item.error() : "" }}</span>

    @if (item.completed()) {
    <span class="t-main">{{"Caricamento completato" }}</span>
    }

    <span class="pos-absolute" style="right: 1rem; top: 1rem" [uploadRemoveItem]="item">
        <i class="fa-solid fa-circle-xmark t-error"></i>
    </span>
</div>
```

## NgxUploadRemoveDirective

Use this directive to remove an item from the list, passing the reference of item to it.

```html
<span [uploadRemoveItem]="item">
    <i class="fa-solid fa-circle-xmark t-error"></i>
</span>
```

## NgxUploadClearDirective

This directive clear the entire list of item.

```html
@if(!list.empty()){
    <button class="btn btn-error mr-3" uploadClear>
        <i class="fa-sharp fa-solid fa-circle-xmark me-2"></i>Clear
    </button>
}
```

## NgxUploadStartDirective

To initiate the upload of all items through the service, add this directive to trigger the upload process.

The result of the upload is emitted by the `load` output, and any error messages are emitted by the `fail` output.

Once the upload is completed, the result is emitted by the `complete` output.

```html
<button
    class="btn btn-main"
    uploadStart
    [removeAfterDelay]="2000"
    [waitAtTheEnd]="false"
    (complete)="onComplete()"
    (load)="onLoad($event)"
    (fail)="onError($event)"
>
    <i class="fa-light fa-file-arrow-up me-2"></i>Import PKI
</button>
```

There are some options to control the behavior of the upload process:

-  `removeAfterDelay` [*@Input*] : Number of milliseconds of delay that the service waits before removing each completed item. If it is `null`, the items won't be removed.
-  `waitAtTheEnd` [*@Input*] : You can choose the method to trigger the upload. All items are uploaded concurrently, but
    - if `true`, the service emits the result after all requests are completed. This uses the **forkJoin** method.
    - if `false` [default], the service emits the result as soon as a single item is completed. This uses the **merge** method.

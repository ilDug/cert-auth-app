import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FileDropDirective, UploadModule, UploadOptions, UploadService } from '../../core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
    selector: 'ca-import-root',
    standalone: true,
    imports: [CommonModule,  MatProgressBarModule, ReactiveFormsModule, FileDropDirective],
    templateUrl: './import-root.component.html',
    styles: ``,
})
export class ImportRootComponent {

    error = signal<string>(null);
    
    passphrase = new FormControl(null, Validators.required);
    certificate = signal<string>(null);
    privateKey = signal<string>(null);
}

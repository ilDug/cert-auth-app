import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { CertificatesService, FileDropDirective, KeysService, PKIService } from '../../core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { toSignal } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { NgxToastService } from '@ildug/ngx-toast';

@Component({
    selector: 'ca-import-root',
    standalone: true,
    imports: [CommonModule, MatProgressBarModule, ReactiveFormsModule, FileDropDirective],
    templateUrl: './import-root.component.html',
    styles: ``,
})
export class ImportRootComponent {
    private pki$ = inject(PKIService);
    private cert$ = inject(CertificatesService);
    private key$ = inject(KeysService);

    toast = inject(NgxToastService);

    // form control for passphrase
    passphraseCtrl = new FormControl(null, Validators.required);

    // passpharse signal to get the value from the form control
    passphrase = toSignal(
        this.passphraseCtrl
            .valueChanges
            .pipe(map(v => v.trim()))
        , { initialValue: null }
    );

    // certificate and private key signals to get the values from the file drop directive
    certificate = signal<string>(null);
    privateKey = signal<string>(null);

    // invalid signal to check if all values are valid
    invalid = computed(() => {
        console.log(this.passphrase());
        return this.passphraseCtrl.invalid || !this.certificate() || !this.privateKey();
    })

    // send the certificate and private key to the server 
    importRoot() {
        if (this.invalid()) return;

        this.pki$.uploadRoot(this.certificate(), this.privateKey(), this.passphrase())
            .subscribe({
                next: () => {
                    this.cert$.refresh();
                    this.key$.refresh();
                    this.toast.info('Root certificate imported successfully', 5000);
                },
                error: err => this.toast.error(err, 5000)
            })
    }
}

import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ImportPkiComponent } from './import-pki/import-pki.component';
import { ImportRootComponent } from './import-root/import-root.component';
import { NgxToastModule, NgxToastService } from '@ildug/ngx-toast';
import { NgxConfirmDirective } from '@ildug/ngx-confirm';

@Component({
  selector: 'ca-settings',
  standalone: true,
    imports: [RouterModule, ImportPkiComponent, ImportRootComponent, NgxToastModule, NgxConfirmDirective],
  templateUrl: './settings.component.html',
  styles: ``
})
export class SettingsComponent {
    toast = inject(NgxToastService) 

    alert() {
        this.toast.info('Questo è un messaggio di alert')
    }
}

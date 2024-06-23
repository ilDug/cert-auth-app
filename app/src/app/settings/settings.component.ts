import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ImportPkiComponent } from './import-pki/import-pki.component';
import { ImportRootComponent } from './import-root/import-root.component';

@Component({
  selector: 'ca-settings',
  standalone: true,
  imports: [RouterModule, ImportPkiComponent, ImportRootComponent],
  templateUrl: './settings.component.html',
  styles: ``
})
export class SettingsComponent {

}

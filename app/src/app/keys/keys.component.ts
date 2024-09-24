import { Component, inject } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { RouterLink, RouterOutlet } from '@angular/router';
import { KeysService } from '../core';

@Component({
  selector: 'ca-keys',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  templateUrl: './keys.component.html',
  styles: ``
})
export class KeysComponent {
    key$ = inject(KeysService);

    reload() {
        this.key$.refresh();
    }
}

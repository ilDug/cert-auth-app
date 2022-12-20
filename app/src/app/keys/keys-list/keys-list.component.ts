import { Component } from '@angular/core';
import { KeysService } from 'src/app/keys.service';

@Component({
  selector: 'app-keys-list',
  templateUrl: './keys-list.component.html',
  styleUrls: ['./keys-list.component.scss']
})
export class KeysListComponent {
    constructor(
        public keys$: KeysService
    ) { }
}

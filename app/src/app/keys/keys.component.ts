import { Component } from '@angular/core';
import { KeysService } from '../keys.service';

@Component({
  selector: 'app-keys',
  templateUrl: './keys.component.html',
  styleUrls: ['./keys.component.scss']
})
export class KeysComponent {
    constructor(
        public keys$: KeysService
    ) { }
}

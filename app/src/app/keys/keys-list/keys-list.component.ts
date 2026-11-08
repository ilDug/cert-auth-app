
import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { KeysService } from '../../core';

@Component({
    selector: 'ca-keys-list',
    imports: [RouterModule],
    templateUrl: './keys-list.component.html',
    styles: ``
})
export class KeysListComponent {

    keys$ = inject(KeysService);
    
}

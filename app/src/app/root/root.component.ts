import { CdkCopyToClipboard } from '@angular/cdk/clipboard';
import { Component } from '@angular/core';
import { MatTooltip } from '@angular/material/tooltip';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'ca-root',
  standalone: true,
  imports: [RouterLink, RouterOutlet, CdkCopyToClipboard, MatTooltip],
  templateUrl: './root.component.html',
  styles: ``
})
export class RootComponent {

}

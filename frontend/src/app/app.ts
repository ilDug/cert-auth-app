import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  imports: [RouterOutlet],
  selector: 'ca-root',
  styles: [],
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('frontend');
}

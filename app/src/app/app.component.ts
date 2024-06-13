import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { ToastDirective } from '@ildug/ngx-toast';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [RouterOutlet, ToastDirective, RouterLink, RouterLinkActive],
    template: `
    <header dagToast class="w-100" style="height: 2rem;"></header>
    <section id="main-container" >
        <nav>
            <div id="logo">
                <i class="fa-duotone fa-landmark-dome"></i>
                <p>CERT-AUTH</p>
            </div>
            <div id="nav-links">
                <ul>
                    <li [routerLink]="['/certificates']" routerLinkActive="active">
                        <i class="fa-solid fa-file-certificate"></i>
                        <span class="link-description">certificati</span>
                    </li>
                    <li [routerLink]="['/keys']" routerLinkActive="active">
                        <i class="fa-solid fa-key-skeleton-left-right"></i>
                        <span class="link-description">chiavi</span>
                    </li>                    
                    <li [routerLink]="['/keys']" routerLinkActive="active">
                        <i class="fa-solid fa-route-interstate"></i>
                        <span class="link-description">root</span>
                    </li>
                    <li [routerLink]="['/settings']" routerLinkActive="active">
                        <i class="fa-solid fa-cog"></i>
                        <span class="link-description">impostazioni</span>
                    </li>
                </ul>
            </div>
        </nav>
        
        <div id="application">
            <router-outlet />
        </div>
    </section>
  `,
    styles: [],
})
export class AppComponent {
}

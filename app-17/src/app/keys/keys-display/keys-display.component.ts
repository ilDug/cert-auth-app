import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Limbo } from '@ildug/sub-limbo';
import { Observable, map, tap } from 'rxjs';
import { CertificatesService } from 'src/app/certificates.service';
import { KeysService } from 'src/app/keys.service';

@Component({
  selector: 'app-keys-display',
  templateUrl: './keys-display.component.html',
  styleUrls: ['./keys-display.component.scss']
})
export class KeysDisplayComponent implements OnInit, OnDestroy {
    constructor(
        public keys$: KeysService,
        private route: ActivatedRoute
    ) { }

    public privPem$: Observable<string>;
    public privInfo$: Observable<string>;
    public pubPem$: Observable<string>;
    public subject: string;
    public tab: string = 'info'
    private sub: Limbo = new Limbo()


    ngOnInit(): void {
        this.sub.oblium = this.route.params
            .pipe(
                map(params => params['key']),
                tap(subject => this.subject = subject),
                tap(subject => {
                    this.privInfo$ = this.keys$.privatekey(subject, "info");
                    this.privPem$ = this.keys$.privatekey(subject, "pem");
                    this.pubPem$ = this.keys$.publickey(subject, "pem");
                })
            )
            .subscribe()
    }

    ngOnDestroy(): void { this.sub.forget() }
}

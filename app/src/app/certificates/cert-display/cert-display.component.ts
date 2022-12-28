import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Limbo } from '@ildug/sub-limbo';
import { delay, map, Observable, tap } from 'rxjs';
import { CertificatesService } from 'src/app/certificates.service';

@Component({
  selector: 'app-cert-display',
  templateUrl: './cert-display.component.html',
  styleUrls: ['./cert-display.component.scss']
})
export class CertDisplayComponent implements OnInit, OnDestroy {
    constructor(
        public certs$: CertificatesService,
        private route: ActivatedRoute
    ) { }

    public pem$: Observable<string>;
    public info$: Observable<string>;
    public subject: string;
    public tab: string = 'info'
    private sub: Limbo = new Limbo()


    ngOnInit(): void {
        this.sub.oblium = this.route.params
            .pipe(
                map(params => params['cert']),
                tap(subject => this.subject = subject),
                tap(subject => {
                    this.pem$ = this.certs$.item(subject, "pem");
                    this.info$ = this.certs$.item(subject, "info");
                })
            )
            .subscribe()
    }

    ngOnDestroy(): void { this.sub.forget() }
}

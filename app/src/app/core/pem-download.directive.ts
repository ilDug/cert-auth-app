import { Directive, input } from '@angular/core';

@Directive({
    selector: '[pem-download]',
    standalone: true,
    host: {
        "(click)": "download()"
    }
})
export class PemDownloadDirective {

    pem = input.required<string>({ alias: "pem-download" });
    filename = input.required<string>();

    download() {
        const blob = new Blob([this.pem()], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = this.filename();
        a.click();
        window.URL.revokeObjectURL(url);
    }

}

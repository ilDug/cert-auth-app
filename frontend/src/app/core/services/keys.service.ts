import { httpResource } from '@angular/common/http';
import { Service, linkedSignal } from '@angular/core';

@Service()
export class KeysService {
    resource = httpResource<string[]>(() => `/api/keys`)
    list = this.resource.value
    pending = linkedSignal<boolean>(() => this.resource.isLoading())
    error = this.resource.error
}

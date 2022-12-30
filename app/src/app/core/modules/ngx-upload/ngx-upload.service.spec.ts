import { TestBed } from '@angular/core/testing';

import { NgxUploadService } from './ngx-upload.service';

describe('NgxUploadService', () => {
  let service: NgxUploadService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NgxUploadService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

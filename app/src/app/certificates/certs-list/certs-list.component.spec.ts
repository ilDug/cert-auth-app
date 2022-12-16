import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CertsListComponent } from './certs-list.component';

describe('CertsListComponent', () => {
  let component: CertsListComponent;
  let fixture: ComponentFixture<CertsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CertsListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CertsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CertDisplayComponent } from './cert-display.component';

describe('CertDisplayComponent', () => {
  let component: CertDisplayComponent;
  let fixture: ComponentFixture<CertDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CertDisplayComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CertDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

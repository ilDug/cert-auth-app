import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportPkiComponent } from './import-pki.component';

describe('ImportPkiComponent', () => {
  let component: ImportPkiComponent;
  let fixture: ComponentFixture<ImportPkiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImportPkiComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImportPkiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

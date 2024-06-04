import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportRootComponent } from './import-root.component';

describe('ImportRootComponent', () => {
  let component: ImportRootComponent;
  let fixture: ComponentFixture<ImportRootComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImportRootComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImportRootComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

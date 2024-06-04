import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeysDisplayComponent } from './keys-display.component';

describe('KeysDisplayComponent', () => {
  let component: KeysDisplayComponent;
  let fixture: ComponentFixture<KeysDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KeysDisplayComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(KeysDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

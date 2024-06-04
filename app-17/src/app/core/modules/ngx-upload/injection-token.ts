import { InjectionToken } from '@angular/core';

export type UploadStrategy = "BASE64" | "FORMDATA";
export const UPLOAD_ENDPOINT = new InjectionToken<string>('Url for file upload');
export const UPLOAD_STRATEGY = new InjectionToken<UploadStrategy>('BASE64 or FORMDATA');

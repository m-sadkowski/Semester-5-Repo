import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; // <--- WAŻNE: To naprawia błąd ngModel

import { AppRoutingModule } from './app-routing-module'; // <--- WAŻNE: To naprawia błąd routerLink
import { App } from './app';
import { BrandListComponent } from './component/brand-list/brand-list'; 
import { BrandFormComponent } from './component/brand-form/brand-form';
import { BrandDetailsComponent } from './component/brand-details/brand-details';
import { ModelFormComponent } from './component/model-form/model-form'; 

@NgModule({
  declarations: [
    App,
    BrandListComponent,
    BrandFormComponent,
    BrandDetailsComponent,
    ModelFormComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule, // <--- Musi być w imports, żeby działał routerLink
    HttpClientModule,
    FormsModule       // <--- Musi być w imports, żeby działał ngModel
  ],
  providers: [
    provideBrowserGlobalErrorListeners()
  ],
  bootstrap: [App]
})
export class AppModule { }
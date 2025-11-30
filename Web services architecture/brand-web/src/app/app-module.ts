import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';
import { BrandListComponent } from './component/brand-list/brand-list'; 
import { BrandFormComponent } from './component/brand-form/brand-form';
import { BrandDetailsComponent } from './component/brand-details/brand-details';
import { ModelFormComponent } from './component/model-form/model-form'; 
import { ModelDetailsComponent } from './component/model-details/model-details';

@NgModule({
  declarations: [
    App,
    BrandListComponent,
    BrandFormComponent,
    BrandDetailsComponent,
    ModelFormComponent,
    ModelDetailsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    provideBrowserGlobalErrorListeners()
  ],
  bootstrap: [App]
})
export class AppModule { }
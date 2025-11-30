import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrandListComponent } from './component/brand-list/brand-list';
import { BrandFormComponent } from './component/brand-form/brand-form';
import { BrandDetailsComponent } from './component/brand-details/brand-details';
import { ModelFormComponent } from './component/model-form/model-form';

const routes: Routes = [
  { path: '', component: BrandListComponent },
  { path: 'create', component: BrandFormComponent },
  { path: 'brand/:id/edit', component: BrandFormComponent },
  { path: 'brand/:id', component: BrandDetailsComponent },
  { path: 'brand/:brandId/model/create', component: ModelFormComponent },
  { path: 'brand/:brandId/model/:modelId/edit', component: ModelFormComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Model } from '../dto/model';

@Injectable({ providedIn: 'root' })
export class ModelService {
  private readonly API_URL = '/api/models';
  constructor(private http: HttpClient) { }

  getModels(): Observable<Model[]> { return this.http.get<Model[]>(this.API_URL); }
  getModel(id: string): Observable<Model> { return this.http.get<Model>(`${this.API_URL}/${id}`); }
  getModelsByBrand(brandId: string): Observable<Model[]> { return this.http.get<Model[]>(`${this.API_URL}/brand/${brandId}`); }
  createModel(model: Model): Observable<Model> { return this.http.post<Model>(this.API_URL, model); }
  updateModel(id: string, model: Model): Observable<void> { return this.http.put<void>(`${this.API_URL}/${id}`, model); }
  deleteModel(id: string): Observable<void> { return this.http.delete<void>(`${this.API_URL}/${id}`); }
}
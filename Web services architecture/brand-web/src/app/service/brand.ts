import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Brand } from '../dto/brand';

@Injectable({ providedIn: 'root' })
export class BrandService {
  private readonly API_URL = '/api/brands';
  constructor(private http: HttpClient) { }

  getBrands(): Observable<Brand[]> { return this.http.get<Brand[]>(this.API_URL); }
  getBrand(id: string): Observable<Brand> { return this.http.get<Brand>(`${this.API_URL}/${id}`); }
  createBrand(brand: Brand): Observable<Brand> { return this.http.post<Brand>(this.API_URL, brand); }
  updateBrand(id: string, brand: Brand): Observable<Brand> { return this.http.put<Brand>(`${this.API_URL}/${id}`, brand); }
  deleteBrand(id: string): Observable<void> { return this.http.delete<void>(`${this.API_URL}/${id}`); }
}
import { Component, OnInit } from '@angular/core';
import { BrandService } from '../../service/brand';
import { Brand } from '../../dto/brand';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-brand-list',
  templateUrl: './brand-list.html',
  styleUrls: ['./brand-list.css'],
  standalone: false
})
export class BrandListComponent implements OnInit {
  
  brands$: Observable<Brand[]> | undefined;

  constructor(private brandService: BrandService) { }

  ngOnInit(): void {
    this.fetchBrands();
  }

  fetchBrands(): void {
    this.brands$ = this.brandService.getBrands();
  }

  deleteBrand(brand: Brand): void {
    this.brandService.deleteBrand(brand.id).subscribe(() => {
      this.fetchBrands();
    });
  }
}
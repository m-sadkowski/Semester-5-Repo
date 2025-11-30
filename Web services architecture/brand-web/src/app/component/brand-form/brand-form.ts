import { Component, OnInit } from '@angular/core';
import { BrandService } from '../../service/brand';
import { Brand } from '../../dto/brand';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-brand-form',
  templateUrl: './brand-form.html',
  styleUrls: ['./brand-form.css'],
  standalone: false
})
export class BrandFormComponent implements OnInit {
  
  brand: Brand = {
    id: '',
    name: '',
    country: ''
  };

  isEditMode = false;

  constructor(
    private brandService: BrandService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    
    if (id) {
      this.isEditMode = true;
      this.brandService.getBrand(id).subscribe({
        next: (data) => this.brand = data,
        error: (err) => console.error('Błąd pobierania marki:', err)
      });
    }
  }

  onSubmit(): void {
    if (this.isEditMode) {
      this.brandService.updateBrand(this.brand.id, this.brand).subscribe(() => {
        this.router.navigate(['/']);
      });
    } else {
      this.brandService.createBrand(this.brand).subscribe(() => {
        this.router.navigate(['/']);
      });
    }
  }
}
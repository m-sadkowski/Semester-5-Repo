import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BrandService } from '../../service/brand';
import { ModelService } from '../../service/model';
import { Brand } from '../../dto/brand';
import { Model } from '../../dto/model';

@Component({
  selector: 'app-brand-details',
  templateUrl: './brand-details.html',
  styleUrls: ['./brand-details.css'],
  standalone: false
})
export class BrandDetailsComponent implements OnInit {
  
  brand: Brand | undefined;
  models: Model[] = [];

  constructor(
    private route: ActivatedRoute,
    private brandService: BrandService,
    private modelService: ModelService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    console.log('Inicjalizacja szczegółów dla ID:', id);
    
    if (id) {
      this.brandService.getBrand(id).subscribe({
        next: (data) => {
          console.log('✅ Marka pobrana:', data);
          this.brand = data;
          this.cdr.detectChanges();
        },
        error: (err) => console.error('Błąd pobierania marki:', err)
      });

      this.fetchModels(id);
    }
  }

  fetchModels(brandId: string): void {
    console.log('Wysyłam zapytanie o modele dla brandId:', brandId);
    
    this.modelService.getModelsByBrand(brandId).subscribe({
      next: (data) => {
        console.log('✅ Modele pobrane:', data);
        this.models = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('❌ Błąd pobierania modeli:', err);
      }
    });
  }

  deleteModel(model: Model): void {
    if(!confirm('Czy na pewno chcesz usunąć ten model?')) return;

    this.modelService.deleteModel(model.id).subscribe(() => {
      this.models = this.models.filter(m => m.id !== model.id);
      this.cdr.detectChanges(); 
    });
  }
}
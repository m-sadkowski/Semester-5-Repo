import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; // <--- 1. Import
import { ActivatedRoute } from '@angular/router';
import { ModelService } from '../../service/model';
import { Model } from '../../dto/model';

@Component({
  selector: 'app-model-details',
  templateUrl: './model-details.html',
  standalone: false
})
export class ModelDetailsComponent implements OnInit {

  model: Model | undefined;
  brandId: string | undefined;

  constructor(
    private route: ActivatedRoute,
    private modelService: ModelService,
    private cdr: ChangeDetectorRef // <--- 2. Wstrzyknięcie
  ) { }

  ngOnInit(): void {
    this.brandId = this.route.snapshot.params['brandId'];
    const modelId = this.route.snapshot.params['modelId'];
    
    console.log('Inicjalizacja szczegółów modelu...');

    if (modelId) {
      this.modelService.getModel(modelId).subscribe({
        next: (data) => {
          console.log('✅ Dane pobrane:', data);
          this.model = data;
          
          // 3. WYMUSZENIE ODŚWIEŻENIA WIDOKU
          this.cdr.detectChanges(); 
        },
        error: (err) => console.error('Błąd:', err)
      });
    }
  }
}
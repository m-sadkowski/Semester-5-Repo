import { Component, OnInit } from '@angular/core';
import { ModelService } from '../../service/model';
import { Model } from '../../dto/model';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-model-form',
  templateUrl: './model-form.html',
  styleUrls: ['./model-form.css'],
  standalone: false
})
export class ModelFormComponent implements OnInit {

  model: Model = {
    id: '',
    name: '',
    year: 2020,
    engine: 1.0,
    brandId: ''
  };

  brandId: string = '';
  isEditMode: boolean = false;

  constructor(
    private modelService: ModelService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.brandId = this.route.snapshot.params['brandId'];
    this.model.brandId = this.brandId;

    const modelId = this.route.snapshot.params['modelId'];
    if (modelId) {
      this.isEditMode = true;
      this.modelService.getModel(modelId).subscribe(data => {
        this.model = data;
        this.model.brandId = this.brandId; 
      });
    }
  }

  onSubmit(): void {
    if (this.isEditMode) {
      this.modelService.updateModel(this.model.id, this.model).subscribe(() => {
        this.router.navigate(['/brand', this.brandId]);
      });
    } else {
      this.modelService.createModel(this.model).subscribe(() => {
        this.router.navigate(['/brand', this.brandId]);
      });
    }
  }
}
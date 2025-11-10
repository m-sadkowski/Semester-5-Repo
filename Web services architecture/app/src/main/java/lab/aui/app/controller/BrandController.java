package lab.aui.app.controller;

import lab.aui.app.domain.Brand;
import lab.aui.app.domain.BrandService;
import lab.aui.app.domain.BrandMapper;
import lab.aui.app.domain.ModelService;
import lab.aui.app.domain.command.CreateBrandCommand;
import lab.aui.app.domain.command.UpdateBrandCommand;
import lab.aui.app.domain.dto.BrandDto;
import lab.aui.app.domain.dto.BrandSummaryDto;
import lab.aui.app.domain.dto.ModelSummaryDto;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/brands")
@RequiredArgsConstructor
public class BrandController {

    private final BrandService brandService;
    private final ModelService modelService;

    @GetMapping
    public ResponseEntity<List<BrandSummaryDto>> getAllBrands() {
        return ResponseEntity.ok(brandService.getAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<BrandDto> getBrandById(@PathVariable("id") UUID id) {
        return ResponseEntity.ok(brandService.getById(id));
    }

    @PostMapping
    public ResponseEntity<BrandSummaryDto> createBrand(@RequestBody CreateBrandCommand command) {
        Brand brand = brandService.create(command);

        URI location = ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(brand.getId())
                .toUri();

        return ResponseEntity.created(location).body(BrandMapper.toSummaryDto(brand));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Void> updateBrand(@PathVariable("id") UUID id, @RequestBody UpdateBrandCommand command) {
        brandService.update(id, command);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteBrand(@PathVariable("id") UUID id) {
        brandService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{brandId}/models")
    public ResponseEntity<List<ModelSummaryDto>> getModelsForBrand(@PathVariable("brandId") UUID brandId) {
        List<ModelSummaryDto> models = modelService.getAllByBrandId(brandId);
        return ResponseEntity.ok(models);
    }
}
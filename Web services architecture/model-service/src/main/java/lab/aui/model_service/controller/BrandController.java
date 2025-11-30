package lab.aui.model_service.controller;

import lab.aui.model_service.domain.Brand;
import lab.aui.model_service.domain.BrandRepository;
import lab.aui.model_service.domain.Model;
import lab.aui.model_service.domain.ModelRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/brands")
@RequiredArgsConstructor
public class BrandController {

    private final BrandRepository brandRepository;
    private final ModelRepository modelRepository;

    @PostMapping
    public void createBrand(@RequestBody Brand brand) {
        brandRepository.save(brand);
    }

    @DeleteMapping("/{id}")
    @Transactional
    public void deleteBrand(@PathVariable UUID id) {
        List<Model> models = modelRepository.findAllByBrandId(id);
        modelRepository.deleteAll(models);
        brandRepository.deleteById(id);
    }

    @PutMapping("/{id}")
    public void updateBrand(@PathVariable UUID id, @RequestBody Brand brand) {
        Brand existingBrand = brandRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Brand not found in Model Service sync"));

        existingBrand.setName(brand.getName());

        brandRepository.save(existingBrand);
    }
}
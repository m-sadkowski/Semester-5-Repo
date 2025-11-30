package lab.aui.brand_service.controller;

import lab.aui.brand_service.command.CreateBrandCommand;
import lab.aui.brand_service.domain.BrandService;
import lab.aui.brand_service.dto.BrandDto;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/brands")
@RequiredArgsConstructor
public class BrandController {

    private final BrandService brandService;

    @GetMapping
    public List<BrandDto> getBrands() {
        return brandService.getAll();
    }

    @GetMapping("/{id}")
    public BrandDto getBrand(@PathVariable UUID id) {
        return brandService.getById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public BrandDto createBrand(@RequestBody CreateBrandCommand command) {
        return brandService.create(command);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteBrand(@PathVariable UUID id) {
        brandService.delete(id);
    }

    @PutMapping("/{id}")
    public void updateBrand(@PathVariable UUID id, @RequestBody CreateBrandCommand command) {
        brandService.update(id, command);
    }
}
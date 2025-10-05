package lab.aui.app;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class BrandService {
    private final BrandRepository brandRepository;

    public BrandService(BrandRepository brandRepository) {
        this.brandRepository = brandRepository;
    }

    public List<Brand> getAllBrands() {
        return brandRepository.findAll();
    }

    public Brand getBrandById(UUID id) {
        return brandRepository.findById(id).orElse(null);
    }

    public Optional<Brand> getBrandsByName(String name) {
        return brandRepository.findByName(name);
    }

    public Optional<Brand> getBrandsByCountry(String country) {
        return brandRepository.findByCountry(country);
    }

    public void saveBrand(Brand brand) {
        brandRepository.save(brand);
    }

    public void deleteBrand(UUID id) {
        brandRepository.deleteById(id);
    }
}

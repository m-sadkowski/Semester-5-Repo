package lab.aui.brand_service.domain;

import lab.aui.brand_service.command.CreateBrandCommand;
import lab.aui.brand_service.dto.BrandDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class BrandService {
    private final BrandRepository brandRepository;
    private final RestTemplate restTemplate;

    public List<BrandDto> getAll() {
        List<Brand> brands = brandRepository.findAll();
        return BrandMapper.toDto(brands);
    }

    public BrandDto getById(UUID id) {
        return brandRepository.findById(id)
                .map(BrandMapper::toDto)
                .orElseThrow(() -> new RuntimeException(String.format("Brand with id %s not found", id)));
    }

    public BrandDto getByName(String name) {
        return brandRepository.findByName(name)
                .map(BrandMapper::toDto)
                .orElseThrow(() -> new RuntimeException(String.format("Brand with name %s not found", name)));
    }

    public List<BrandDto> getAllByCountry(String country) {
        List<Brand> brands = brandRepository.findAllByCountry(country);
        return BrandMapper.toDto(brands);
    }

    public BrandDto create(CreateBrandCommand command) {
        Brand brand = BrandMapper.toEntity(command);
        brandRepository.save(brand);
        restTemplate.postForLocation("http://localhost:8082/api/brands", brand);
        return BrandMapper.toDto(brand);
    }

    @Transactional
    public void update(UUID id, CreateBrandCommand command) {
        Brand brand = brandRepository.findById(id)
                .orElseThrow(() -> new RuntimeException(String.format("Brand with id %s not found", id)));

        brand.setName(command.getName());
        brand.setCountry(command.getCountry());

        brandRepository.save(brand);

        restTemplate.put("http://localhost:8082/api/brands/" + id, brand);
    }

    public void delete(UUID id) {
        brandRepository.deleteById(id);
        restTemplate.delete("http://localhost:8082/api/brands/" + id);
    }
}
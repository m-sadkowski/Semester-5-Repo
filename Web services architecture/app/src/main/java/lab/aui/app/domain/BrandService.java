package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateBrandCommand;
import lab.aui.app.domain.dto.BrandDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class BrandService {
    private final BrandRepository brandRepository;

    public List<BrandDto> getAll() {
        List<Brand> brands = brandRepository.findAllWithModels();
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

    public void create(CreateBrandCommand command) {
        Brand brand = BrandMapper.toEntity(command);
        brandRepository.save(brand);
    }

    public void delete(UUID id) {
        brandRepository.deleteById(id);
    }
}

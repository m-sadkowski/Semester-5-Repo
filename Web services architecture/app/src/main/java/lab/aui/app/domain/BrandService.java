package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateBrandCommand;
import lab.aui.app.domain.command.UpdateBrandCommand;
import lab.aui.app.domain.dto.BrandDto;
import lab.aui.app.domain.dto.BrandSummaryDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class BrandService {
    private final BrandRepository brandRepository;

    public List<BrandSummaryDto> getAll() {
        List<Brand> brands = brandRepository.findAll();
        return BrandMapper.toSummaryDto(brands);
    }

    public BrandDto getById(UUID id) {
        return brandRepository.findById(id)
                .map(BrandMapper::toDto)
                .orElseThrow(() -> new ResourceNotFoundException(String.format("Brand with id %s not found", id)));
    }

    public BrandDto getByName(String name) {
        return brandRepository.findByName(name)
                .map(BrandMapper::toDto)
                .orElseThrow(() -> new ResourceNotFoundException(String.format("Brand with name %s not found", name)));
    }

    public List<BrandSummaryDto> getAllByCountry(String country) {
        List<Brand> brands = brandRepository.findAllByCountry(country);
        return BrandMapper.toSummaryDto(brands);
    }

    public Brand create(CreateBrandCommand command) {
        Brand brand = BrandMapper.toEntity(command);
        return brandRepository.save(brand);
    }

    public void update(UUID id, UpdateBrandCommand command) {
        Brand brand = brandRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(String.format("Brand with id %s not found", id)));
        BrandMapper.updateEntity(command, brand);
        brandRepository.save(brand);
    }

    public void delete(UUID id) {
        if (!brandRepository.existsById(id)) {
            throw new ResourceNotFoundException(String.format("Brand with id %s not found", id));
        }
        brandRepository.deleteById(id);
    }
}
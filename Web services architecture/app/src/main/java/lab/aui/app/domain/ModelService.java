package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateModelCommand;
import lab.aui.app.domain.dto.ModelDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ModelService {
    private final ModelRepository modelRepository;
    private final BrandRepository brandRepository;

    public List<ModelDto> getAll() {
        List<Model> models = modelRepository.findAllWithBrand();
        return ModelMapper.toDto(models);
    }

    public ModelDto getById(UUID id) {
        return modelRepository.findById(id)
                .map(ModelMapper::toDto)
                .orElseThrow(() -> new RuntimeException(String.format("Model with id %s not found", id)));
    }

    public List<ModelDto> getAllByName(String name) {
        List<Model> models = modelRepository.findAllByName(name);
        return ModelMapper.toDto(models);
    }

    public List<ModelDto> getAllByYear(int year) {
        List<Model> models = modelRepository.findAllByYear(year);
        return ModelMapper.toDto(models);
    }

    public List<ModelDto> getAllByEngine(double engine) {
        List<Model> models = modelRepository.findAllByEngine(engine);
        return ModelMapper.toDto(models);
    }

    public List<ModelDto> getAllByBrandId(UUID brandId) {
        List<Model> models = modelRepository.findAllByBrandId(brandId);
        return ModelMapper.toDto(models);
    }

    public void create(CreateModelCommand command) {
        Model model = ModelMapper.toEntity(command);
        Brand brand = brandRepository.findById(command.getBrandId())
                .orElseThrow(() -> new RuntimeException(String.format("Brand with id %s not found", command.getBrandId())));
        model.setBrand(brand);
        modelRepository.save(model);
    }

    public void delete(UUID id) {
        modelRepository.deleteById(id);
    }
}
package lab.aui.model_service.domain;

import lab.aui.model_service.domain.command.CreateModelCommand;
import lab.aui.model_service.domain.dto.ModelDto;
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
        return ModelMapper.toDto(modelRepository.findAllWithBrand());
    }

    public ModelDto getById(UUID id) {
        return modelRepository.findById(id)
                .map(ModelMapper::toDto)
                .orElseThrow(() -> new RuntimeException("Model not found: " + id));
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

    public ModelDto create(CreateModelCommand command) {
        Model model = ModelMapper.toEntity(command);
        Brand brand = brandRepository.findById(command.getBrandId())
                .orElseThrow(() -> new RuntimeException("Brand not found (make sure syncing works): " + command.getBrandId()));
        model.setBrand(brand);
        modelRepository.save(model);
        return ModelMapper.toDto(model);
    }

    public void update(UUID id, CreateModelCommand command) {
        Model model = modelRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Model not found: " + id));
        model.setName(command.getName());
        model.setYear(command.getYear());
        model.setEngine(command.getEngine());
        modelRepository.save(model);
    }

    public void delete(UUID id) {
        modelRepository.deleteById(id);
    }
}
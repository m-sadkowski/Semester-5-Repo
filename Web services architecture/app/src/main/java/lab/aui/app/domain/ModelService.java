package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateModelCommand;
import lab.aui.app.domain.command.UpdateModelCommand;
import lab.aui.app.domain.dto.ModelDto;
import lab.aui.app.domain.dto.ModelSummaryDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ModelService {
    private final ModelRepository modelRepository;
    private final BrandRepository brandRepository;

    public List<ModelSummaryDto> getAll() {
        List<Model> models = modelRepository.findAllWithBrand();
        return ModelMapper.toSummaryDto(models);
    }

    public ModelDto getById(UUID id) {
        return modelRepository.findById(id)
                .map(ModelMapper::toDto)
                .orElseThrow(() -> new ResourceNotFoundException(String.format("Model with id %s not found", id)));
    }

    public List<ModelSummaryDto> getAllByName(String name) {
        List<Model> models = modelRepository.findAllByName(name);
        return ModelMapper.toSummaryDto(models);
    }

    public List<ModelSummaryDto> getAllByYear(int year) {
        List<Model> models = modelRepository.findAllByYear(year);
        return ModelMapper.toSummaryDto(models);
    }

    public List<ModelSummaryDto> getAllByEngine(double engine) {
        List<Model> models = modelRepository.findAllByEngine(engine);
        return ModelMapper.toSummaryDto(models);
    }

    public List<ModelSummaryDto> getAllByBrandId(UUID brandId) {
        if (!brandRepository.existsById(brandId)) {
            throw new ResourceNotFoundException(String.format("Brand with id %s not found", brandId));
        }
        List<Model> models = modelRepository.findAllByBrandId(brandId);
        return ModelMapper.toSummaryDto(models);
    }

    public Model create(UUID brandId, CreateModelCommand command) {
        Model model = ModelMapper.toEntity(command);
        Brand brand = brandRepository.findById(brandId)
                .orElseThrow(() -> new ResourceNotFoundException(String.format("Brand with id %s not found", brandId)));
        model.setBrand(brand);
        return modelRepository.save(model);
    }

    public void update(UUID id, UpdateModelCommand command) {
        Model model = modelRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(String.format("Model with id %s not found", id)));
        ModelMapper.updateEntity(command, model);
        modelRepository.save(model);
    }

    public void delete(UUID id) {
        if (!modelRepository.existsById(id)) {
            throw new ResourceNotFoundException(String.format("Model with id %s not found", id));
        }
        modelRepository.deleteById(id);
    }
}
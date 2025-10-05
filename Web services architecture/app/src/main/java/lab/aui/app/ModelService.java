package lab.aui.app;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ModelService {
    private final ModelRepository modelRepository;
    
    public ModelService(ModelRepository modelRepository) {
        this.modelRepository = modelRepository;
    }
    
    public List<Model> getAllModels() {
        return modelRepository.findAll();
    }

    public Model getModelById(UUID id) {
        return modelRepository.findById(id).orElse(null);
    }

    public Optional<Model> getModelsByName(String name) {
        return modelRepository.findByName(name);
    }

    public Optional<Model> getModelsByYear(int year) {
        return modelRepository.findByYear(year);
    }

    public Optional<Model> getModelsByEngine(double engine) {
        return modelRepository.findByEngine(engine);
    }

    public Optional<Model> getModelsByBrand(Brand brand) {
        return modelRepository.findByBrand(brand);
    }

    public void saveModel(Model model) {
        modelRepository.save(model);
    }

    public void deleteModel(UUID id) {
        modelRepository.deleteById(id);
    }
}
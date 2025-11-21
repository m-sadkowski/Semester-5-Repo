package lab.aui.model_service.domain;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.UUID;

@Component
public class DataInitializer {
    private final ModelRepository modelRepository;
    private final BrandRepository brandRepository;

    public DataInitializer(ModelRepository modelRepository, BrandRepository brandRepository) {
        this.modelRepository = modelRepository;
        this.brandRepository = brandRepository;
    }

    @PostConstruct
    public void initialize() {
        Brand ford = Brand.builder().id(UUID.randomUUID()).name("Ford").build();
        Brand audi = Brand.builder().id(UUID.randomUUID()).name("Audi").build();
        brandRepository.saveAll(List.of(ford, audi));

        Model focus = Model.builder().id(UUID.randomUUID()).name("Focus").year(2010).engine(1.6).brand(ford).build();
        Model a4 = Model.builder().id(UUID.randomUUID()).name("A4").year(2015).engine(2.0).brand(audi).build();
        modelRepository.saveAll(List.of(focus, a4));
    }
}
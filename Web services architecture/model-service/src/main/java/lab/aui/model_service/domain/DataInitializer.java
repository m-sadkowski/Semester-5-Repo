package lab.aui.model_service.domain;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.UUID;

@Component
public class DataInitializer {
    private final ModelRepository modelRepository;
    private final BrandRepository brandRepository;

    public static final UUID FORD_ID = UUID.fromString("f4b3b3b3-3b3b-3b3b-3b3b-3b3b3b3b3b3b");
    public static final UUID AUDI_ID = UUID.fromString("a4b3b3b3-3b3b-3b3b-3b3b-3b3b3b3b3b3b");

    public DataInitializer(ModelRepository modelRepository, BrandRepository brandRepository) {
        this.modelRepository = modelRepository;
        this.brandRepository = brandRepository;
    }

    @PostConstruct
    public void initialize() {
        if (brandRepository.count() == 0) {
            Brand ford = Brand.builder().id(FORD_ID).name("Ford").build();
            Brand audi = Brand.builder().id(AUDI_ID).name("Audi").build();
            brandRepository.saveAll(List.of(ford, audi));

            Model focus = Model.builder()
                    .id(UUID.randomUUID())
                    .name("Focus")
                    .year(2010)
                    .engine(1.6)
                    .brand(ford)
                    .build();

            Model a4 = Model.builder()
                    .id(UUID.randomUUID())
                    .name("A4")
                    .year(2015)
                    .engine(2.0)
                    .brand(audi)
                    .build();

            modelRepository.saveAll(List.of(focus, a4));
        }
    }
}
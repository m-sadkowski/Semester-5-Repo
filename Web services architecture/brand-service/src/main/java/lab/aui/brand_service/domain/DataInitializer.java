package lab.aui.brand_service.domain;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.UUID;

@Component
public class DataInitializer {
    private final BrandRepository brandRepository;

    public static final UUID FORD_ID = UUID.fromString("f4b3b3b3-3b3b-3b3b-3b3b-3b3b3b3b3b3b");
    public static final UUID AUDI_ID = UUID.fromString("a4b3b3b3-3b3b-3b3b-3b3b-3b3b3b3b3b3b");

    public DataInitializer(BrandRepository brandRepository) {
        this.brandRepository = brandRepository;
    }

    @PostConstruct
    public void initialize() {
        if (brandRepository.count() == 0) {
            Brand ford = Brand.builder().id(FORD_ID).name("Ford").country("USA").build();
            Brand audi = Brand.builder().id(AUDI_ID).name("Audi").country("Germany").build();
            brandRepository.saveAll(List.of(ford, audi));
        }
    }
}
package lab.aui.brand_service.domain;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import java.util.List;
import java.util.UUID;

@Component
public class DataInitializer {

    private final BrandRepository brandRepository;

    public DataInitializer(BrandRepository brandRepository) {
        this.brandRepository = brandRepository;
    }

    @PostConstruct
    public void initialize() {
        if (brandRepository.count() == 0) {
            UUID vwId = UUID.fromString("f5875513-bf7b-4ae1-b8a5-5b70a1b90e76");
            UUID audiId = UUID.fromString("5d1da2ae-6a14-4b6d-8b4f-d117867118d4");

            Brand vw = Brand.create(vwId, "Volkswagen", "Germany");
            Brand audi = Brand.create(audiId, "Audi", "Germany");

            brandRepository.saveAll(List.of(vw, audi));

            System.out.println(">>> [Brand-Service] Zainicjowano marki: VW i Audi");
        }
    }
}
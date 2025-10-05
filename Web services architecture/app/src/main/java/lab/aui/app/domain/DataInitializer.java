package lab.aui.app.domain;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
class DataInitializer {
    private final BrandRepository brandRepository;
    private final ModelRepository modelRepository;

    public DataInitializer(BrandRepository brandRepository, ModelRepository modelRepository) {
        this.brandRepository = brandRepository;
        this.modelRepository = modelRepository;
    }

    @PostConstruct
    void initialize() {
        Brand vw = Brand.create("Volkswagen", "Germany");
        Brand audi = Brand.create("Audi", "Germany");
        brandRepository.saveAll(List.of(vw, audi));

        Model golfV = Model.create("Golf V", 2007, 1.9, vw);
        Model passatB6 = Model.create("Passat", 2006, 1.6, vw);
        Model touran = Model.create("Touran", 2011, 2.0, vw);
        Model a4 = Model.create("A4", 1998, 1.8, audi);
        Model q5 = Model.create("Q5", 2015, 3.0, audi);
        Model b6 = Model.create("B6", 1997, 2.2, audi);
        modelRepository.saveAll(List.of(golfV, passatB6, touran, a4, q5, b6));
    }
}

package lab.aui.app;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {
    private final BrandService brandService;
    private final ModelService modelService;

    public DataInitializer(BrandService brandService, ModelService modelService) {
        this.brandService = brandService;
        this.modelService = modelService;
    }

    @Override
    public void run(String... args) {
        List<Brand> brands = createTestData();
        for (Brand brand : brands) {
            brandService.saveBrand(brand);
        }
    }

    private static List<Brand> createTestData() {
        Brand vw = Brand.create("Volkswagen", "Germany");
        Model.create("Golf V", 2007, 1.9, vw);
        Model.create("Passat", 2006, 1.6, vw);
        Model.create("Touran", 2011, 2.0, vw);

        Brand audi = Brand.create("Audi", "Germany");
        Model.create("A4", 1998, 1.8, audi);
        Model.create("Q5", 2015, 3.0, audi);
        Model.create("B6", 1997, 2.2, audi);

        return List.of(vw, audi);
    }
}

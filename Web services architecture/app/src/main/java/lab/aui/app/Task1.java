package lab.aui.app;

import java.io.*;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ForkJoinPool;
import java.util.stream.Collectors;

class Task1 {
    static void execute() {
        List<Brand> brands = createTestData();
        Set<Model> models = getUniqueModels(brands);

        featureFirstAndSecond(brands);
        featureThird(models);
        featureFourth(models);
        featureFifth(models);
        featureSixth(brands);
        featureSeventh(brands);
    }

    private static List<Brand> createTestData() {
        Brand vw = Brand.create("Volkswagen", "Germany");
        Model.create("Golf V", 2007, 1.9, vw);
        Model.create("Passat", 2006, 1.6, vw);
        Model.create("Touran", 2011, 2.0, vw);

        Brand rm = Brand.create("Audi", "Germany");
        Model.create("A4", 1998, 1.8, rm);
        Model.create("Q5", 2015, 3.0, rm);
        Model.create("B6", 1997, 2.2, rm);

        return List.of(vw, rm);
    }

    private static Set<Model> getUniqueModels(List<Brand> brands) {
        return brands.stream()
                .flatMap(brand -> brand.getModels().stream())
                .collect(Collectors.toSet());
    }

    private static void featureFirstAndSecond(List<Brand> brands) {
        System.out.println("\nFeatures 1 & 2: ");
        brands.forEach(System.out::println);
    }

    private static void featureThird(Set<Model> modelsSet) {
        System.out.println("\nFeature 3: ");
        modelsSet.forEach(System.out::println);
    }

    private static void featureFourth(Set<Model> modelsSet) {
        System.out.println("\nFeature 4: ");
        modelsSet.stream()
                .filter(model -> model.getYear() > 2000)
                .sorted(Comparator.comparing(Model::getName))
                .forEach(System.out::println);
    }

    private static void featureFifth(Set<Model> modelsSet) {
        System.out.println("\nFeature 5: ");
        List<ModelDto> modelsDto = modelsSet.stream()
                .map(ModelMapper::toDto)
                .sorted()
                .toList();
        modelsDto.forEach(System.out::println);
    }

    private static void featureSixth(List<Brand> brands) {
        System.out.println("\nFeature 6: ");
        try (FileOutputStream fileOut = new FileOutputStream("brands.ser");
             ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
            out.writeObject(brands);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        try (FileInputStream fileIn = new FileInputStream("brands.ser");
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            List<Brand> newBrands = (List<Brand>) in.readObject();
            newBrands.forEach(System.out::println);
        } catch (IOException | ClassNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void featureSeventh(List<Brand> brands) {
        System.out.println("\nFeature 7: ");
        try (ForkJoinPool customPool = new ForkJoinPool(2)) {
            customPool.submit(() ->
                    brands.parallelStream().forEach(brand -> {
                        System.out.println(Thread.currentThread().getName()
                                + " is processing " + brand.getName());
                        brand.getModels().forEach(model -> {
                            try {
                                Thread.sleep(3000);
                            } catch (InterruptedException e) {
                                System.out.println(e.getMessage());
                            }
                            System.out.println(model);
                        });
                    })
            ).get();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}

package lab.aui.app.application;

import lab.aui.app.domain.BrandService;
import lab.aui.app.domain.ModelService;
import lab.aui.app.domain.command.CreateBrandCommand;
import lab.aui.app.domain.command.CreateModelCommand;
import lab.aui.app.domain.dto.BrandDto;
import lab.aui.app.domain.dto.ModelDto;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Scanner;
import java.util.UUID;

@Component
class AppCommandLineRunner implements CommandLineRunner {
    private final BrandService brandService;
    private final ModelService modelService;

    public AppCommandLineRunner(BrandService brandService, ModelService modelService) {
        this.brandService = brandService;
        this.modelService = modelService;
    }

    //@Override
    public void run(String... args) throws Exception {
        /*Scanner scanner = new Scanner(System.in);

        boolean running = true;

        printHelp();

        while (running) {
            System.out.print("\nEnter Command: ");
            String input = scanner.nextLine().trim().toLowerCase();

            switch (input) {
                case "help":
                    printHelp();
                    break;
                case "list brands":
                    listBrands();
                    break;
                case "list models":
                    listModels();
                    break;
                case "add brand":
                    addBrand(scanner);
                    break;
                case "add model":
                    addModel(scanner);
                    break;
                case "delete brand":
                    deleteBrand(scanner);
                    break;
                case "delete model":
                    deleteModel(scanner);
                    break;
                case "exit":
                    running = false;
                    System.out.println("Closing application...");
                    break;
                default:
                    System.out.println("Unknown command: " + input);
            }
        }

        scanner.close();*/
    }

    private void printHelp() {
        System.out.println("Available commands:");
        System.out.println("- list brands");
        System.out.println("- list models");
        System.out.println("- add brand");
        System.out.println("- add model");
        System.out.println("- delete brand");
        System.out.println("- delete model");
        System.out.println("- exit");
    }
    /*
    private void listBrands() {
        List<BrandDto> brands = brandService.getAll();
        if (brands.isEmpty()) {
            System.out.println("No available brands.");
            return;
        }
        System.out.println("Brands:");
        brands.forEach(System.out::println);
    }

    private void listModels() {
        List<ModelDto> models = modelService.getAll();
        if (models.isEmpty()) {
            System.out.println("No available models.");
            return;
        }
        System.out.println("Models:");
        models.forEach(System.out::println);
    }

    private void addBrand(Scanner scanner) {
        System.out.println("Create new brand [id name country]: ");
        UUID id = UUID.fromString(scanner.nextLine().trim().toLowerCase());
        String name = scanner.nextLine().trim();
        String country = scanner.nextLine().trim();
        CreateBrandCommand createBrandCommand = CreateBrandCommand.builder()
                .id(id)
                .name(name)
                .country(country)
                .build();
        brandService.create(createBrandCommand);
    }

    private void addModel(Scanner scanner) {
        System.out.println("Create new model [id name year engine brandId]: ");
        UUID id = UUID.fromString(scanner.nextLine().trim().toLowerCase());
        String name = scanner.nextLine().trim();
        int year = Integer.parseInt(scanner.nextLine().trim());
        double engine = Double.parseDouble(scanner.nextLine().trim());
        UUID brandId = UUID.fromString(scanner.nextLine().trim().toLowerCase());
        CreateModelCommand createModelCommand = CreateModelCommand.builder()
                .id(id)
                .name(name)
                .year(year)
                .engine(engine)
                .brandId(brandId)
                .build();
        modelService.create(createModelCommand);
    }

    private void deleteBrand(Scanner scanner) {
        System.out.println("Delete brand [id]: ");
        UUID id = UUID.fromString(scanner.nextLine().trim().toLowerCase());
        brandService.delete(id);
    }

    private void deleteModel(Scanner scanner) {
        System.out.println("Delete model [id]: ");
        UUID id = UUID.fromString(scanner.nextLine().trim().toLowerCase());
        modelService.delete(id);
    }
    */
}

package lab.aui.app;

import org.springframework.boot.CommandLineRunner;

import java.util.List;
import java.util.Scanner;

public class AppCommandLineRunner implements CommandLineRunner {
    private final BrandService brandService;
    private final ModelService modelService;

    public AppCommandLineRunner(BrandService brandService, ModelService modelService) {
        this.brandService = brandService;
        this.modelService = modelService;
    }

    @Override
    public void run(String... args) throws Exception {
        Scanner scanner = new Scanner(System.in);

        boolean running = true;

        printHelp();

        while (running) {
            System.out.print("\nWpisz komendę: ");
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
                case "quit":
                    running = false;
                    System.out.println("Closing application...");
                    break;
                default:
                    System.out.println("Unknown command: " + input);
            }
        }

        scanner.close();
    }

    private void printHelp() {
        System.out.println("Avabile commands:");
        System.out.println("- list brands - ");
        System.out.println("- list models - ");
        System.out.println("- add brand - ");
        System.out.println("- add model - ");
        System.out.println("- delete brand - ");
        System.out.println("- delete model - ");
        System.out.println("- exit - ");
    }
    private void listBrands() {
        List<Brand> brands = brandService.getAllBrands();
        if (brands.isEmpty()) {
            System.out.println("No available brands.");
            return;
        }
        System.out.println("Brands:");
        System.out.println(brands);
    }
    private void listModels() {
        List<Model> models = modelService.getAllModels();
        if (models.isEmpty()) {
            System.out.println("No available models.");
            return;
        }
        System.out.println("Models:");
        System.out.println(models);
    }
    private void addBrand(Scanner scanner) {}
    private void addModel(Scanner scanner) {}
    private void deleteBrand(Scanner scanner) {}
    private void deleteModel(Scanner scanner) {}
}

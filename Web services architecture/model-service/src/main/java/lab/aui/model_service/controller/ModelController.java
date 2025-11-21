package lab.aui.model_service.controller;

import lab.aui.model_service.domain.command.CreateModelCommand;
import lab.aui.model_service.domain.dto.ModelDto;
import lab.aui.model_service.domain.ModelService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/models")
@RequiredArgsConstructor
public class ModelController {

    private final ModelService modelService;

    @GetMapping
    public List<ModelDto> getModels() {
        return modelService.getAll();
    }

    @GetMapping("/{id}")
    public ModelDto getModel(@PathVariable UUID id) {
        return modelService.getById(id);
    }

    @GetMapping("/brand/{brandId}")
    public List<ModelDto> getModelsByBrand(@PathVariable UUID brandId) {
        return modelService.getAllByBrandId(brandId);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ModelDto createModel(@RequestBody CreateModelCommand command) {
        return modelService.create(command);
    }

    @PutMapping("/{id}")
    public void updateModel(@PathVariable UUID id, @RequestBody CreateModelCommand command) {
        modelService.update(id, command);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteModel(@PathVariable UUID id) {
        modelService.delete(id);
    }
}
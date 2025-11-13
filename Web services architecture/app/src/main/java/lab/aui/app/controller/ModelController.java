package lab.aui.app.controller;

import lab.aui.app.domain.Model;
import lab.aui.app.domain.ModelService;
import lab.aui.app.domain.ModelMapper;
import lab.aui.app.domain.command.CreateModelCommand;
import lab.aui.app.domain.command.UpdateModelCommand;
import lab.aui.app.domain.dto.ModelDto;
import lab.aui.app.domain.dto.ModelSummaryDto;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class ModelController {

    private final ModelService modelService;

    @GetMapping("/models")
    public ResponseEntity<List<ModelSummaryDto>> getAllModels() {
        return ResponseEntity.ok(modelService.getAll());
    }

    @GetMapping("/models/{id}")
    public ResponseEntity<ModelDto> getModelById(@PathVariable("id") UUID id) {
        return ResponseEntity.ok(modelService.getById(id));
    }

    @PostMapping("/brands/{brandId}/models")
    public ResponseEntity<ModelSummaryDto> createModelForBrand(@PathVariable("brandId") UUID brandId,
                                                               @RequestBody CreateModelCommand command) {
        Model model = modelService.create(brandId, command);

        URI location = ServletUriComponentsBuilder
                .fromCurrentContextPath() // ignoruje caly obecny adres i bierze bazę
                .path("/models/{id}")
                .buildAndExpand(model.getId())
                .toUri();

        return ResponseEntity.created(location).body(ModelMapper.toSummaryDto(model));
    }

    @PutMapping("/models/{id}")
    public ResponseEntity<Void> updateModel(
            @PathVariable("id") UUID id,
            @RequestBody UpdateModelCommand command) {

        modelService.update(id, command);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/models/{id}")
    public ResponseEntity<Void> deleteModel(@PathVariable("id") UUID id) {
        modelService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
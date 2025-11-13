package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateModelCommand;
import lab.aui.app.domain.command.UpdateModelCommand;
import lab.aui.app.domain.dto.ModelDto;
import lab.aui.app.domain.dto.ModelSummaryDto;
import lombok.experimental.UtilityClass;

import java.util.List;
import java.util.UUID;

@UtilityClass
public class ModelMapper {
    public static ModelDto toDto(Model model) {
        return ModelDto.builder()
                .id(model.getId())
                .name(model.getName())
                .year(model.getYear())
                .engine(model.getEngine())
                .brandName(model.getBrand().getName())
                .build();
    }

    public static List<ModelDto> toDto(List<Model> models) {
        return models.stream()
                .map(ModelMapper::toDto)
                .toList();
    }

    public static ModelSummaryDto toSummaryDto(Model model) {
        return ModelSummaryDto.builder()
                .id(model.getId())
                .name(model.getName())
                .year(model.getYear())
                .brandName(model.getBrand().getName())
                .build();
    }

    public static List<ModelSummaryDto> toSummaryDto(List<Model> models) {
        return models.stream()
                .map(ModelMapper::toSummaryDto)
                .toList();
    }

    public static Model toEntity(CreateModelCommand command) {
        return Model.builder()
                .id(UUID.randomUUID())
                .name(command.getName())
                .year(command.getYear())
                .engine(command.getEngine())
                .build();
    }

    public static void updateEntity(UpdateModelCommand command, Model model) {
        model.setName(command.getName());
        model.setYear(command.getYear());
        model.setEngine(command.getEngine());
    }
}
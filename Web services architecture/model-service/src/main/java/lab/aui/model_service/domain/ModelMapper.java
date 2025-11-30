package lab.aui.model_service.domain;

import lab.aui.model_service.domain.command.CreateModelCommand;
import lab.aui.model_service.domain.dto.ModelDto;
import lombok.experimental.UtilityClass;

import java.util.List;
import java.util.UUID;

@UtilityClass
class ModelMapper {
    static ModelDto toDto(Model model) {
        return ModelDto.builder()
                .id(model.getId())
                .name(model.getName())
                .year(model.getYear())
                .engine(model.getEngine())
                .brandName(model.getBrand().getName())
                .brandId(model.getBrand().getId())
                .build();
    }

    static List<ModelDto> toDto(List<Model> models) {
        return models.stream()
                .map(ModelMapper::toDto)
                .toList();
    }

    static Model toEntity(CreateModelCommand command) {
        return Model.builder()
                .id(UUID.randomUUID())
                .name(command.getName())
                .year(command.getYear())
                .engine(command.getEngine())
                .build();
    }
}

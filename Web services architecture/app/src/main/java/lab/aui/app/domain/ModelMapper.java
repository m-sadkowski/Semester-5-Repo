package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateModelCommand;
import lab.aui.app.domain.dto.ModelDto;
import lombok.experimental.UtilityClass;

import java.util.List;

@UtilityClass
class ModelMapper {
    static ModelDto toDto(Model model) {
        return ModelDto.builder()
                .id(model.getId())
                .name(model.getName())
                .year(model.getYear())
                .engine(model.getEngine())
                .brandName(model.getBrand().getName())
                .build();
    }

    static List<ModelDto> toDto(List<Model> models) {
        return models.stream()
                .map(ModelMapper::toDto)
                .toList();
    }

    static Model toEntity(CreateModelCommand command) {
        return Model.builder()
                .id(command.getId())
                .name(command.getName())
                .year(command.getYear())
                .engine(command.getEngine())
                .build();
    }
}

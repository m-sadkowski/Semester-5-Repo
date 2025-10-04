package lab.aui.app;

import lombok.experimental.UtilityClass;

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
}

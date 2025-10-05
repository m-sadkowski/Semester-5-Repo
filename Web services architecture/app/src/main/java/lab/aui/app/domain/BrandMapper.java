package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateBrandCommand;
import lab.aui.app.domain.dto.BrandDto;
import lombok.experimental.UtilityClass;

import java.util.List;

@UtilityClass
public class BrandMapper {
    static BrandDto toDto(Brand brand) {
        return BrandDto.builder()
                .id(brand.getId())
                .name(brand.getName())
                .country(brand.getCountry())
                .models(ModelMapper.toDto(brand.getModels()))
                .build();
    }

    static List<BrandDto> toDto(List<Brand> models) {
        return models.stream()
                .map(BrandMapper::toDto)
                .toList();
    }

    static Brand toEntity(CreateBrandCommand command) {
        return Brand.builder()
                .id(command.getId())
                .name(command.getName())
                .country(command.getCountry())
                .build();
    }
}

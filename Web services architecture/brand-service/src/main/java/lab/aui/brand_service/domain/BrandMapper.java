package lab.aui.brand_service.domain;

import lab.aui.brand_service.command.CreateBrandCommand;
import lab.aui.brand_service.dto.BrandDto;
import lombok.experimental.UtilityClass;

import java.util.List;
import java.util.UUID;

@UtilityClass
class BrandMapper {
    static BrandDto toDto(Brand brand) {
        return BrandDto.builder()
                .id(brand.getId())
                .name(brand.getName())
                .country(brand.getCountry())
                .build();
    }

    static List<BrandDto> toDto(List<Brand> models) {
        return models.stream()
                .map(BrandMapper::toDto)
                .toList();
    }

    static Brand toEntity(CreateBrandCommand command) {
        return Brand.builder()
                .id(UUID.randomUUID())
                .name(command.getName())
                .country(command.getCountry())
                .build();
    }
}

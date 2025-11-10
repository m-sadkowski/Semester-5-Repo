package lab.aui.app.domain;

import lab.aui.app.domain.command.CreateBrandCommand;
import lab.aui.app.domain.command.UpdateBrandCommand;
import lab.aui.app.domain.dto.BrandDto;
import lab.aui.app.domain.dto.BrandSummaryDto;
import lombok.experimental.UtilityClass;

import java.util.List;
import java.util.UUID;

@UtilityClass
public class BrandMapper {
    public static BrandDto toDto(Brand brand) {
        return BrandDto.builder()
                .id(brand.getId())
                .name(brand.getName())
                .country(brand.getCountry())
                .models(ModelMapper.toDto(brand.getModels()))
                .build();
    }

    public static List<BrandDto> toDto(List<Brand> models) {
        return models.stream()
                .map(BrandMapper::toDto)
                .toList();
    }

    public static BrandSummaryDto toSummaryDto(Brand brand) {
        return BrandSummaryDto.builder()
                .id(brand.getId())
                .name(brand.getName())
                .country(brand.getCountry())
                .build();
    }

    public static List<BrandSummaryDto> toSummaryDto(List<Brand> brands) {
        return brands.stream()
                .map(BrandMapper::toSummaryDto)
                .toList();
    }

    public static Brand toEntity(CreateBrandCommand command) {
        return Brand.builder()
                .id(UUID.randomUUID())
                .name(command.getName())
                .country(command.getCountry())
                .build();
    }

    public static void updateEntity(UpdateBrandCommand command, Brand brand) {
        brand.setName(command.getName());
        brand.setCountry(command.getCountry());
    }
}
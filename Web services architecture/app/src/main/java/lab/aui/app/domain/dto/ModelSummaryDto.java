package lab.aui.app.domain.dto;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
public class ModelSummaryDto {
    private UUID id;
    private String name;
    private int year;
    private String brandName;
}
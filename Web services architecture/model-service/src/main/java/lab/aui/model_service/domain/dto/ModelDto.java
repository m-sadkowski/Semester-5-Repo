package lab.aui.model_service.domain.dto;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
public class ModelDto implements Comparable<ModelDto> {
    private final UUID id;
    private final String name;
    private final int year;
    private final double engine;
    private final String brandName;
    private final UUID brandId;

    @Override
    public int compareTo(ModelDto other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return ("(ID: " + id + ") " + brandName + " " + name + " (" + year + "), " + engine);
    }
}

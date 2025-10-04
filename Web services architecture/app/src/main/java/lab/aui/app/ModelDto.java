package lab.aui.app;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
class ModelDto implements Comparable<ModelDto> {
    private final UUID id;
    private final String name;
    private final int year;
    private final double engine;
    private final String brandName;

    @Override
    public int compareTo(ModelDto other) {
        return this.id.compareTo(other.id);
    }
}

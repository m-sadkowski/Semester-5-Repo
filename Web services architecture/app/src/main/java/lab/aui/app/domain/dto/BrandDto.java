package lab.aui.app.domain.dto;

import lombok.Builder;
import lombok.Data;

import java.util.List;
import java.util.UUID;

@Data
@Builder
public class BrandDto implements Comparable<BrandDto> {
    private final UUID id;
    private final String name;
    private final String country;
    private final List<ModelDto> models;

    @Override
    public int compareTo(BrandDto other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return ("(ID: " + id + ") " + name + " (" + country + ")");
    }
}
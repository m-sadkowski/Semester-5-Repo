package lab.aui.app;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Setter
@Getter
@Builder
class Brand implements Comparable<Brand>, Serializable {
    private final UUID id;
    private final String name;
    private final String country;
    private List<Model> models;

    static Brand create(String name, String country) {
        return Brand.builder()
                .id(UUID.randomUUID())
                .name(name)
                .country(country)
                .models(List.of())
                .build();
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, country, models);
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Brand c)) { return false; }
        return this.id.equals(c.id);
    }

    @Override
    public int compareTo(Brand other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return "Brand: " + name + " (" + country + ")" + ", models: " + models;
    }
}

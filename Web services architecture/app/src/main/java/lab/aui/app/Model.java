package lab.aui.app;

import lombok.Builder;
import lombok.Getter;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Getter
@Builder
class Model implements Comparable<Model>, Serializable {
    private final UUID id;
    private final String name;
    private final int year;
    private final double engine;
    private final Brand brand;

    static void create(String name, int year, double engine, Brand brand) {
        Model newModel = Model.builder()
                .id(UUID.randomUUID())
                .name(name)
                .year(year)
                .engine(engine)
                .brand(brand)
                .build();

        List<Model> newModels = new ArrayList<>(brand.getModels());
        newModels.add(newModel);
        brand.setModels(newModels);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, year, engine);
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Model p)) { return false; }
        return this.id.equals(p.id);
    }

    @Override
    public int compareTo(Model other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return name + " (" + year + ")";
    }
}

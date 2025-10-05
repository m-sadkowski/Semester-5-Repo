package lab.aui.app;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "models")
public class Model implements Comparable<Model>, Serializable {
    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;
    @Column(name = "name", nullable = false)
    private String name;
    @Column(name = "production_year", nullable = false)
    private int year;
    @Column(name = "engine_capacity", nullable = false)
    private double engine;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "brand", nullable = false)
    private Brand brand;

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
        return Objects.hash(id);
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

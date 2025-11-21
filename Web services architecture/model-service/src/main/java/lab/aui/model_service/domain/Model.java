package lab.aui.model_service.domain;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "models")
public class Model implements Comparable<Model>, Serializable {
    @Id
    @Column(name = "id", nullable = false)
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

    static Model create(String name, int year, double engine, Brand brand) {
        return Model.builder()
                .id(UUID.randomUUID())
                .name(name)
                .year(year)
                .engine(engine)
                .brand(brand)
                .build();
    }

    @Override
    public int hashCode() { return Objects.hash(id); }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Model p)) return false;
        return this.id.equals(p.id);
    }

    @Override
    public int compareTo(Model other) { return this.id.compareTo(other.id); }

    @Override
    public String toString() { return name + " (" + year + ")"; }
}
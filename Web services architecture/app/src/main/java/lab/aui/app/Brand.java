package lab.aui.app;

import jakarta.persistence.*;
import lombok.Setter;
import lombok.Getter;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.io.Serializable;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "brands")
public class Brand implements Comparable<Brand>, Serializable {
    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;
    @Column(name = "name", nullable = false)
    private String name;
    @Column(name = "country", nullable = false)
    private String country;
    @OneToMany(mappedBy = "brand", fetch = FetchType.LAZY, cascade = CascadeType.ALL)
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
        return Objects.hash(id);
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

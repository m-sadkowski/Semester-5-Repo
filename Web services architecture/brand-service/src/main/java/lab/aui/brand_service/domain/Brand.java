package lab.aui.brand_service.domain;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;
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
    @Column(name = "id", nullable = false)
    private UUID id;
    @Column(name = "name", nullable = false, unique = true)
    private String name;
    @Column(name = "country", nullable = false)
    private String country;

    static Brand create(String name, String country) {
        return Brand.builder()
                .id(UUID.randomUUID())
                .name(name)
                .country(country)
                .build();
    }

    static Brand create(UUID id, String name, String country) {
        return Brand.builder()
                .id(id)
                .name(name)
                .country(country)
                .build();
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Brand c)) {
            return false;
        }
        return this.id.equals(c.id);
    }

    @Override
    public int compareTo(Brand other) {
        return this.id.compareTo(other.id);
    }

    @Override
    public String toString() {
        return "Brand: " + name + " (" + country + ")";
    }
}
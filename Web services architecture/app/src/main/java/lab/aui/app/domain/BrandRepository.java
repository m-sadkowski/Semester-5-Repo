package lab.aui.app.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

interface BrandRepository extends JpaRepository<Brand, UUID> {
    @Query("SELECT b FROM Brand b LEFT JOIN FETCH b.models")
    List<Brand> findAllWithModels();

    @Query("SELECT b FROM Brand b LEFT JOIN FETCH b.models WHERE b.name = :name")
    Optional<Brand> findByName(String name);

    @Query("SELECT b FROM Brand b LEFT JOIN FETCH b.models WHERE b.country = :country")
    List<Brand> findAllByCountry(String country);
}

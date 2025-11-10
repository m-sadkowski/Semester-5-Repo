package lab.aui.app.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.UUID;

interface ModelRepository extends JpaRepository<Model, UUID> {
    @Query("SELECT m FROM Model m LEFT JOIN FETCH m.brand")
    List<Model> findAllWithBrand();

    @Query("SELECT m FROM Model m LEFT JOIN FETCH m.brand WHERE m.name = :name")
    List<Model> findAllByName(String name);

    @Query("SELECT m FROM Model m LEFT JOIN FETCH m.brand WHERE m.year = :year")
    List<Model> findAllByYear(int year);

    @Query("SELECT m FROM Model m LEFT JOIN FETCH m.brand WHERE m.engine = :engine")
    List<Model> findAllByEngine(double engine);

    @Query("SELECT m FROM Model m LEFT JOIN FETCH m.brand WHERE m.brand.id = :brandId")
    List<Model> findAllByBrandId(UUID brandId);
}
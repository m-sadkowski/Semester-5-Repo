package lab.aui.app;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface ModelRepository extends JpaRepository<Model, UUID> {
    Optional<Model> findByName(String name);
    Optional<Model> findByYear(int year);
    Optional<Model> findByEngine(double engine);
    Optional<Model> findByBrand(Brand brand);
}
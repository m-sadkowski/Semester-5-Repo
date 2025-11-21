package lab.aui.brand_service.domain;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

interface BrandRepository extends JpaRepository<Brand, UUID> {
    Optional<Brand> findByName(String name);

    List<Brand> findAllByCountry(String country);
}

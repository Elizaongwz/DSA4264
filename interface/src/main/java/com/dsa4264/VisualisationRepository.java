package com.dsa4264;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface VisualisationRepository extends JpaRepository<Bus, Integer> {
    Optional<Bus> findById(Integer Id);
}


package com.dsa4264;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TrainLineRepository extends JpaRepository<TrainLine, Long> {
}
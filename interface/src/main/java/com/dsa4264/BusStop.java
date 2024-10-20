package com.dsa4264;


import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.util.List;

@Entity
@Table(name = "bus_stops")
public class BusStop {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  
  private String name;

  private Point location;

  @ManyToOne(targetEntity = BusRoute.class)
  @JoinColumn(name = "bus_route_id")
  private BusRoute busRoute;
  
  // getters and setters
}

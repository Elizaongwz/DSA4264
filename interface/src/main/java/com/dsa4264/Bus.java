package com.dsa4264;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

@Entity
public class Bus {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String busServiceNumber;
    private String routeGeoJson; // Store GeoJSON format

    // Getters and Setters
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getBusServiceNumber() {
        return busServiceNumber;
    }

    public void setBusServiceNumber(String busServiceNumber) {
        this.busServiceNumber = busServiceNumber;
    }

    public String getRouteGeoJson() {
        return routeGeoJson;
    }

    public void setRouteGeoJson(String routeGeoJson) {
        this.routeGeoJson = routeGeoJson;
    }
}
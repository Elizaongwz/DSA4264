package com.dsa4264.BusModel;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

@Entity
public class Bus {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;

    private String busServiceNumber;
    private String routeInfo;

    public Integer getId() {
        return id;
    }

    public String getBusServiceNumber() {
        return busServiceNumber;
    }

    public void setBusServiceNumber(String busServiceNumber) {
        this.busServiceNumber = busServiceNumber;
    }

    public String getRouteInfo() {
        return routeInfo;
    }

    public void setRouteInfo(String routeInfo) {
        this.routeInfo = routeInfo;
    }
}

package com.dsa4264.BusModel;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class BusVisualisationService {

    private final String PYTHON_API_URL = "http://127.0.0.1:5000/api/";

    public String getBusRouteGeoJson(Integer busId) {
        RestTemplate restTemplate = new RestTemplate();
        String routeUrl = PYTHON_API_URL + "bus_routes/" + busId;
        return restTemplate.getForObject(routeUrl, String.class);
    }

    public String getTrainRoutesGeoJson() {
        RestTemplate restTemplate = new RestTemplate();
        String trainUrl = PYTHON_API_URL + "train_routes";
        return restTemplate.getForObject(trainUrl, String.class);
    }
}

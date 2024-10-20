package com.dsa4264;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

@Service
public class BusVisualisationService {

    private final String PYTHON_API_URL = "http://127.0.0.1:5000/api/";

    public List<String> getAllBusRoutes() {
        RestTemplate restTemplate = new RestTemplate();
        String[] busRoutes = restTemplate.getForObject(PYTHON_API_URL + "bus_routes", String[].class);
        return Arrays.asList(busRoutes);
    }

    public String plotBusRoutes(List<String> busRoutes) {
        RestTemplate restTemplate = new RestTemplate();
        UriComponentsBuilder uriBuilder = UriComponentsBuilder.fromHttpUrl(PYTHON_API_URL + "plot_routes")
                .queryParam("busRoutes", String.join(",", busRoutes)); // Join bus routes as a comma-separated string
        return restTemplate.postForObject(uriBuilder.toUriString(), null, String.class); // Handle response as String
    }


    @SuppressWarnings("unchecked")
    public Map<String, Double> calculateParallelScores(List<String> busRoutes) {
        RestTemplate restTemplate = new RestTemplate();
        String scoreUrl = PYTHON_API_URL + "parallel_score";
        return restTemplate.postForObject(scoreUrl, busRoutes, Map.class);
    }
}


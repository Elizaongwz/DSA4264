package com.dsa4264;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Arrays;
import java.util.HashMap;
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

    public String plotBusRoutes(String serviceNo) {
        RestTemplate restTemplate = new RestTemplate();
        // Prepare the request body
        Map<Object, Object> requestBody = new HashMap<>();
        requestBody.put("service_no", serviceNo);  // Assuming we are passing one bus route for now

        // Create HttpEntity to wrap the request body
        HttpEntity<Map<Object, Object>> requestEntity = new HttpEntity<>(requestBody);
    
        // Logging request info for debugging
        System.out.println("Sending request to Python API: " + PYTHON_API_URL);
        System.out.println("Request Body: " + requestBody);
    
        // Using exchange() to handle the String response (HTML from Python API)
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "/plot_routes",
            HttpMethod.POST,
            requestEntity,
            String.class
        );
        
        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();
        } else {
            throw new RuntimeException("Failed to get map from Python API:" + response.getStatusCode());
        }
    }
    


    @SuppressWarnings("unchecked")
    public Map<String, Double> calculateParallelScores(List<String> busRoutes) {
        RestTemplate restTemplate = new RestTemplate();
        String scoreUrl = PYTHON_API_URL + "parallel_score";
        return restTemplate.postForObject(scoreUrl, busRoutes, Map.class);
    }
}


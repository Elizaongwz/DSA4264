package com.dsa4264;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
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

     public Map<String, Object> plotBusRoutes(List<String> busRoutes) {
        RestTemplate restTemplate = new RestTemplate();
        UriComponentsBuilder uriBuilder = UriComponentsBuilder.fromHttpUrl(PYTHON_API_URL).path("plot_routes");

        // Prepare the request body
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("service_no", busRoutes.get(0));  // Assuming we are passing one bus route for now

        // Create HttpEntity to wrap the request body
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestBody);

        // Logging request info for debugging
        System.out.println("Sending request to Python API: " + uriBuilder.toUriString());
        System.out.println("Request Body: " + requestBody);

        // Using exchange() instead of postForEntity to handle ParameterizedTypeReference
        ResponseEntity<Map<String, Object>> response = null;
        try {
            response = restTemplate.exchange(
                    uriBuilder.toUriString(), 
                    HttpMethod.POST, 
                    requestEntity, 
                    new ParameterizedTypeReference<Map<String, Object>>() {}
            );
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Error during POST request to Python API: " + e.getMessage());
            throw e;
        }

        // Logging response for debugging
        System.out.println("Response received from Python API: " + response.getBody());

        // Return the response body
        return response.getBody();
    }

    


    @SuppressWarnings("unchecked")
    public Map<String, Double> calculateParallelScores(List<String> busRoutes) {
        RestTemplate restTemplate = new RestTemplate();
        String scoreUrl = PYTHON_API_URL + "parallel_score";
        return restTemplate.postForObject(scoreUrl, busRoutes, Map.class);
    }
}


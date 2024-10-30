package com.dsa4264;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service  // Marks this class as a Spring service, allowing for dependency injection
public class BusVisualisationService {

    // Base URL for Flask API that handles data and visualizations
    private final String PYTHON_API_URL = "http://127.0.0.1:5000/api/";

    // Fetches all available bus routes from the Flask API (GET request)
    public List<String> getAllBusRoutes() {
        RestTemplate restTemplate = new RestTemplate();  // Initialize RestTemplate to make HTTP requests
        // Send GET request to Flask API to get all bus routes
        String[] busRoutes = restTemplate.getForObject(PYTHON_API_URL + "bus_routes", String[].class);
        return Arrays.asList(busRoutes);  // Convert array of routes into a list
    }

    // Fetches all modified bus routes from the Flask API (GET request)
    public List<String> getAllModifiedRoutes() {
        RestTemplate restTemplate = new RestTemplate();
        // Send GET request to Flask API to get all modified bus routes
        String[] busRoutes = restTemplate.getForObject(PYTHON_API_URL + "modified_routes", String[].class);
        return Arrays.asList(busRoutes);  // Convert array of routes into a list
    }

    // Fetches all proposed bus routes from the Flask API (GET request)
    public List<String> getAllProposedRoutes() {
        RestTemplate restTemplate = new RestTemplate();
        // Send GET request to Flask API to get all proposed bus routes
        String[] busRoutes = restTemplate.getForObject(PYTHON_API_URL + "proposed_routes", String[].class);
        return Arrays.asList(busRoutes);  // Convert array of routes into a list
    }

    // Fetches MRT train lines from the Flask API (GET request)
    public String getTrainLines() {
        RestTemplate restTemplate = new RestTemplate();
        // Send GET request to Flask API to fetch train lines (GeoJSON)
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "train_lines",
            HttpMethod.GET,
            null,
            String.class
        );
        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();  // Return the GeoJSON data for train lines if successful
        } else {
            // Throw an error if the response is not OK
            throw new RuntimeException("Failed to get train lines from Python API: " + response.getStatusCode());
        }
    }

    // Plots a bus route on the map by calling the Flask API (POST request)
    public String plotBusRoutes(String serviceNo) {
        RestTemplate restTemplate = new RestTemplate();
        // Prepare the request body with the bus service number
        Map<Object, Object> requestBody = new HashMap<>();
        requestBody.put("service_no", serviceNo);

        // Wrap the request body in HttpEntity
        HttpEntity<Map<Object, Object>> requestEntity = new HttpEntity<>(requestBody);

        // Logging for debugging purposes
        System.out.println("Sending request to Python API: " + PYTHON_API_URL);
        System.out.println("Request Body: " + requestBody);

        // Send POST request to Flask API to plot the bus route (returns GeoJSON)
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "/plot_routes",
            HttpMethod.POST,
            requestEntity,
            String.class
        );
        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();  // Return GeoJSON data if successful
        } else {
            // Throw an error if the response is not OK
            throw new RuntimeException("Failed to get map from Python API:" + response.getStatusCode());
        }
    }

    // Plots a modified bus route by calling the Flask API (POST request)
    public String plotModifiedBusRoutes(String serviceNo) {
        RestTemplate restTemplate = new RestTemplate();
        // Prepare the request body with the bus service number
        Map<Object, Object> requestBody = new HashMap<>();
        requestBody.put("service_no", serviceNo);

        // Wrap the request body in HttpEntity
        HttpEntity<Map<Object, Object>> requestEntity = new HttpEntity<>(requestBody);

        // Logging for debugging purposes
        System.out.println("Sending request to Python API: " + PYTHON_API_URL);
        System.out.println("Request Body: " + requestBody);

        // Send POST request to Flask API to plot the modified bus route (returns GeoJSON)
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "/plot_modified_routes",
            HttpMethod.POST,
            requestEntity,
            String.class
        );
        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();  // Return GeoJSON data if successful
        } else {
            // Throw an error if the response is not OK
            throw new RuntimeException("Failed to get map from Python API:" + response.getStatusCode());
        }
    }

    // Plots a proposed bus route by calling the Flask API (POST request)
    public String plotProposedRoutes(String serviceName) {
        RestTemplate restTemplate = new RestTemplate();
        // Prepare the request body with the proposed bus service name
        Map<Object, Object> requestBody = new HashMap<>();
        requestBody.put("service_name", serviceName);

        // Wrap the request body in HttpEntity
        HttpEntity<Map<Object, Object>> requestEntity = new HttpEntity<>(requestBody);

        // Logging for debugging purposes
        System.out.println("Sending request to Python API: " + PYTHON_API_URL);
        System.out.println("Request Body: " + requestBody);

        // Send POST request to Flask API to plot the proposed bus route (returns GeoJSON)
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "/plot_proposed_routes",
            HttpMethod.POST,
            requestEntity,
            String.class
        );
        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();  // Return GeoJSON data if successful
        } else {
            // Throw an error if the response is not OK
            throw new RuntimeException("Failed to get map from Python API:" + response.getStatusCode());
        }
    }

    // Fetches the parallel score for a bus route by calling the Flask API (POST request)
    public String getParallelScore(String serviceNo) {
        RestTemplate restTemplate = new RestTemplate();

        // Prepare the request body with the bus service number
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("service_no", serviceNo);

        // Wrap the request body in HttpEntity
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestBody);

        // Send POST request to Flask API to fetch the parallel score
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "/parallel_score",
            HttpMethod.POST,
            requestEntity,
            String.class
        );

        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();  // Return the parallel score if successful
        } else {
            // Throw an error if the response is not OK
            throw new RuntimeException("Failed to get parallel score from Python API: " + response.getStatusCode());
        }
    }

    // Fetches the rank of a bus route by calling the Flask API (POST request)
    public String getRank(String serviceNo) {
        RestTemplate restTemplate = new RestTemplate();

        // Prepare the request body with the bus service number
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("service_no", serviceNo);

        // Wrap the request body in HttpEntity
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestBody);

        // Send POST request to Flask API to fetch the rank of the bus route
        ResponseEntity<String> response = restTemplate.exchange(
            PYTHON_API_URL + "/rank",
            HttpMethod.POST,
            requestEntity,
            String.class
        );

        if (response.getStatusCode() == HttpStatus.OK) {
            return response.getBody();  // Return the rank if successful
        } else {
            // Throw an error if the response is not OK
            throw new RuntimeException("Failed to get rank from Python API: " + response.getStatusCode());
        }
    }
}

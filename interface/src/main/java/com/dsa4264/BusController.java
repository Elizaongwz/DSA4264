package com.dsa4264;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@CrossOrigin(origins = "http://localhost:3000") // Enable CORS for requests coming from React frontend
@RestController // Spring REST controller
@RequestMapping("/api") // Base URL for all endpoints in this controller
public class BusController {

    private final BusVisualisationService busVisualisationService;

    // Constructor injection for BusVisualisationService
    public BusController(BusVisualisationService busVisualisationService) {
        this.busVisualisationService = busVisualisationService;
    }

    // Endpoint to get all bus routes
    @GetMapping("/bus_routes")
    public ResponseEntity<List<String>> getAllBusRoutes() {
        try {
            List<String> busRoutes = busVisualisationService.getAllBusRoutes();
            return ResponseEntity.ok(busRoutes); // Return bus routes with 200 status
        }
        catch (Exception e) {
            // log error and return 500 (Internal Server Error) response if something goes wrong
            System.err.println("Error fetching bus routes: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
    // Endpoint to get all modified routes
    @GetMapping("/modified_routes")
    public ResponseEntity<List<String>> getAllModifiedRoutes() {
        try {
            List<String> busRoutes = busVisualisationService.getAllModifiedRoutes(); // Fetch modified routes
            return ResponseEntity.ok(busRoutes); // Return modified routes with HTTP status 200 (OK)
        }
        catch (Exception e) {
            // log error and return 500 (Internal Server Error) response if something goes wrong
            System.err.println("Error fetching bus routes: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    // Endpoint to get all proposed routes
    @GetMapping("/proposed_routes")
    public ResponseEntity<List<String>> getAllProposedRoutes() {
        try {
            List<String> busRoutes = busVisualisationService.getAllProposedRoutes(); // Fetch proposed routes
            return ResponseEntity.ok(busRoutes); // Return modified routes with HTTP status 200 (OK)
        }
        catch (Exception e) {
            // log error and return 500 (Internal Server Error) response if something goes wrong
            System.err.println("Error fetching bus routes: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    // Endpoint to get train lines (as GeoJSON)
    @GetMapping("/train_lines")
    public ResponseEntity<String> getTrainLines() {
        try {
            String trainLines = busVisualisationService.getTrainLines();  // GeoJSON data for train lines
            if (trainLines == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: Train lines not found."); // Handle missing data
            }
            return ResponseEntity.ok(trainLines);  // Return the GeoJSON data when status 200
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage()); // Handle errors and log as 500 status code
        }
    }
    
    // Endpoint to plot bus routes (returns GeoJSON data for the selected bus route)
    @PostMapping("/plot_routes")
    public ResponseEntity<String> plotBusRoutes(@RequestBody Map<String, String> busRouteRequest){
        // Extract "service_no" from the request body
        String serviceNo = busRouteRequest.get("service_no"); 

        if (serviceNo == null || serviceNo.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: 'service_no' is required."); // Handle invalid request
        }

        // Call the service to get the bus route visualization (HTML map)
        try {
            String geoJsonData = busVisualisationService.plotBusRoutes(serviceNo);  // Assuming this method returns GeoJSON
            if (geoJsonData == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: Bus route not found.");
            }
            return ResponseEntity.ok(geoJsonData);  // Return the GeoJSON data
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }
     // Endpoint to plot modified bus routes (returns GeoJSON data)
    @PostMapping("/plot_modified_routes")
    public ResponseEntity<String> plotModifiedBusRoutes(@RequestBody Map<String, String> busRouteRequest){
        // Extract "service_no" from the request body
        String serviceNo = busRouteRequest.get("service_no");

        if (serviceNo == null || serviceNo.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: 'service_no' is required.");
        }

        // Call the service to get the bus route visualization (HTML map)
        try {
            String geoJsonData = busVisualisationService.plotModifiedBusRoutes(serviceNo);  // method returns GeoJSON
            if (geoJsonData == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: Bus route not found.");
            }
            return ResponseEntity.ok(geoJsonData);  // Return the GeoJSON data
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }
    // Endpoint to plot proposed bus routes (returns GeoJSON data)
    @PostMapping("/plot_proposed_routes")
    public ResponseEntity<String> plotProposedRoutes(@RequestBody Map<String, String> busRouteRequest){
        // Extract "service_no" from the request body
        String serviceName = busRouteRequest.get("service_name");

        if (serviceName == null || serviceName.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: 'service_name' is required.");
        }

        // Call the service to get the bus route visualization (HTML map)
        try {
            // Extract "service_name" from the request body
            String geoJsonData = busVisualisationService.plotProposedRoutes(serviceName);  // method returns GeoJSON
            if (geoJsonData == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Error: Bus route not found.");
            }
            return ResponseEntity.ok(geoJsonData);  // Return the GeoJSON data
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }
    // Endpoint to calculate and return the parallel score for a bus route
    @PostMapping("/parallel_score")
    public ResponseEntity<String> parallelScore(@RequestBody Map<String, String> busRouteRequest) {
        // Extract bus service number
        String serviceNo = busRouteRequest.get("service_no");

        if (serviceNo == null || serviceNo.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: 'service_no' is required."); // Handle missing service
        }

        try {
            // Call the service to get the parallel score for the provided service number
            String score = busVisualisationService.getParallelScore(serviceNo);
            return ResponseEntity.ok(score);  // Return the score as a string
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage()); // log error as status 500
        }
    }

    // Endpoint to calculate and return the rank of the parallel score for a bus route
    @PostMapping("/rank")
    public ResponseEntity<String> Rank(@RequestBody Map<String, String> busRouteRequest) {
        // Extract bus service number
        String serviceNo = busRouteRequest.get("service_no");

        if (serviceNo == null || serviceNo.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: 'service_no' is required.");
        }

        try {
            // Call the service to get the parallel score for the provided service number
            String score = busVisualisationService.getRank(serviceNo);
            return ResponseEntity.ok(score);  // Return the score as a string
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage()); // log error as status 500
        }
    }

}

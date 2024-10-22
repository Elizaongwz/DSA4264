package com.dsa4264;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@CrossOrigin(origins = "http://localhost:3000")
@RestController
@RequestMapping("/api")
public class BusController {

    private final BusVisualisationService busVisualisationService;

    public BusController(BusVisualisationService busVisualisationService) {
        this.busVisualisationService = busVisualisationService;
    }
    @GetMapping("/bus_routes")
    public ResponseEntity<List<String>> getAllBusRoutes() {
        try {
            List<String> busRoutes = busVisualisationService.getAllBusRoutes();
            return ResponseEntity.ok(busRoutes);
        }
        catch (Exception e) {
            System.err.println("Error fetching bus routes: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    //return busVisualisationService.getAllBusRoutes();
    }
    

    @PostMapping("/plot_routes")
    public ResponseEntity<String> plotBusRoutes(@RequestBody Map<String, String> busRouteRequest){
        // Extract "service_no" from the request body
        String serviceNo = busRouteRequest.get("service_no");

        if (serviceNo == null || serviceNo.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error: 'service_no' is required.");
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



    @PostMapping("/parallel_score")
    public Map<String, Double> parallelScore(@RequestParam List<String> busRoutes) {
        // This method calculates and returns the parallel scores for the selected bus routes
        return busVisualisationService.calculateParallelScores(busRoutes);
    }
}

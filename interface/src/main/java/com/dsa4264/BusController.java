package com.dsa4264;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
    public Map<String, Object> plotRoutes(@RequestBody List<String> busRoutes) {
        if (busRoutes == null || busRoutes.isEmpty()) {
            System.err.println("No bus routes received!");
            Map<String, Object> errorMap = new HashMap<>();
        errorMap.put("error", "No bus routes received!");
        return errorMap;
        } else {
            System.out.println("Received bus routes: " + busRoutes);
        }
    
    // This method returns a stringified HTML of the map
        return busVisualisationService.plotBusRoutes(busRoutes);
    }


    @PostMapping("/parallel_score")
    public Map<String, Double> parallelScore(@RequestParam List<String> busRoutes) {
        // This method calculates and returns the parallel scores for the selected bus routes
        return busVisualisationService.calculateParallelScores(busRoutes);
    }
}

package com.dsa4264.BusModel;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class BusController {

    @Autowired
    private VisualisationRepository visualisationRepository;

    @GetMapping("/bus-services")
    public String getBusServices(Model model) {
        List<Bus> buses = visualisationRepository.findAll();
        model.addAttribute("buses", buses);
        return "busServices";  // Will render a dropdown menu in Thymeleaf
    }

    @GetMapping("/bus-route")
    public String getBusRoute(@RequestParam("id") Integer id, Model model) {
        Bus bus = visualisationRepository.findById(id).orElse(null);
        if (bus != null) {
            model.addAttribute("bus", bus);
            // Fetch and pass the route information to the frontend
            model.addAttribute("routeInfo", bus.getRouteInfo());
        }
        return "busRoute";
    }
}

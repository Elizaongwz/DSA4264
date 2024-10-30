# Technical Report

**Project: LTA Geospatial Analysis**  
**Members: Eliza, Fang Ting, Krystal, Lily**  
Last updated on 29 October, 2024

## Section 1: Context

*In this section, you should explain how this project came about. Retain all relevant details about the project’s history and context, especially if this is a continuation of a previous project.*

*If there are any slide decks or email threads that started before this project, you should include them as well.*

## Section 2: Scope

### 2.1 Problem

*In this subsection, you should explain what is the key business problem that you are trying to solve through your data science project. You should aim to answer the following questions:*

* *What is the problem that the business unit faces? Be specific about who faces the problem, how frequently it occurs, and how it affects their ability to meet their desired goals.*
* *What is the significance or impact of this problem? Provide tangible metrics that demonstrate the cost of not addressing this problem.*
* *Why is data science / machine learning the appropriate solution to the problem?*


### 2.2 Success Criteria

Firstly, success would be achieved when our project identifies at least 2-3 bus routes that have significant overlap with MRT lines that can be modified. By targeting these parallel bus services, Land Transport Authority (LTA) can reduce operational costs and reallocate funds toward routes aligned with commuter needs. This improves LTA’s resource utilisation, ensuring that the funds are invested to maximise the value of the public transport system.

Another key measure of success is an increase in public satisfaction. By considering public sentiments when optimising route planning, bus services are catered to meet real commuter needs, leading to greater satisfaction and convenience and thus commuter experiences can be improved. An improved, demand-driven public network reflects LTA’s commitment to connecting people and places effectively, ensuring a positive perception of Singapore’s public transport system.

Lastly, our project’s success will be measured by the development of an adaptable, data-driven framework that LTA can apply to assess future MRT line expansions. This enables LTA to quickly evaluate the impact of new MRT lines on existing bus services, enabling faster, data-driven decisions for route planning and resource allocation. This allows LTA to meet the evolving commuter needs, ensuring a more efficient system that continues to be aligned with their vision of a people-centred transport system.


### 2.3 Assumptions

*In this subsection, you should set out the key assumptions for this data science project that, if changed, will affect the problem statement, success criteria, or feasibility. You do not need to detail out every single assumption if the expected impact is not significant.*

*For example, if we are building an automated fraud detection model, one important assumption may be whether there is enough manpower to review each individual decision before proceeding with it.*

## Section 3: Methodology

### 3.1 Technical Assumptions

*In this subsection, you should set out the assumptions that are directly related to your model development process. Some general categories include:*
* *How to define certain terms as variables*
* *What features are available / not available*
* *What kind of computational resources are available to you (ie on-premise vs cloud, GPU vs CPU, RAM availability)*
* *What the key hypotheses of interest are*
* *What the data quality is like (especially if incomplete / unreliable)*

### 3.2 Data

After retrieving raw data on the bus routes through API calls, the datasets obtained were Bus_routes_df, Bus_stops_df, bus_services_df. 

Our first step was to filter for trunk services from bus_services_df, and join ServiceNo to Bus_routes_df to create a new dataframe ‘trunkroutes’. Next, we cleaned the trunk routes by combining both directions of a bus service into a single continuous route. If the last stop of the first direction matched the first stop of the second direction, we removed the duplicate bus stop and updated the stop sequence of the second direction to make a single route. If the last stop of the first direction did not match the first stop of direction two, we update the stop sequence of the second direction immediately as there are no duplicate stops. Following this, we dropped the directions column to ensure a simplified representation of each bus service route.

After cleaning the trunk routes, we created new features for each bus stop in the dataset. Our first feature is the average_passenger_volume, calculated for each bus stop. This is essential in identifying bus stops with high or low demands. We obtained the tap-in and tap-out data for each stop, summing the values across July, August, and September for both weekdays and weekends. The final average passenger volume for each bus stop was calculated as the mean of these monthly values.

Another feature was an indicator for whether a bus stop was an MRT station or not. A bus stop was defined as an MRT bus stop if its description contained ‘Stn’ or ‘Int’, but did not contain words like ‘Police’, ‘Fire’, ‘Railway’, which would indicate non-MRT bus stops.

Additionally, we defined which MRT line(s) each MRT bus stop belonged to. To do this, we created a mapping between MRT lines and their stations, including variations and short forms of station names to account for different naming conventions in the raw data. Using the find_mrt_line function, we checked each MRT bus stop’s name against the mapped MRT lines. If the bus stop name contained the station name from any MRT line, it would return the respective MRT line(s) associated with that bus stop.


### 3.3 Experimental Design

*In this subsection, you should clearly explain the key steps of your model development process, such as:*
* *Algorithms: Which ML algorithms did you choose to experiment with, and why?*
* *Evaluation: Which evaluation metric did you optimise and assess the model on? Why is this the most appropriate?*
* *Training: How did you arrive at the final set of hyperparameters? How did you manage imbalanced data or regularisation?*

## Section 4: Findings

### 4.1 Results

*In this subsection, you should report the results from your experiments in a summary table, keeping only the most relevant results for your experiment (ie your best model, and two or three other options which you explored). You should also briefly explain the summary table and highlight key results.*

*Interpretability methods like LIME or SHAP should also be reported here, using the appropriate tables or charts.*

### 4.2 Discussion

*In this subsection, you should discuss what the results mean for the business user – specifically how the technical metrics translate into business value and costs, and whether this has sufficiently addressed the business problem.*

*You should also discuss or highlight other important issues like interpretability, fairness, and deployability.*

### 4.3 Recommendations

To handle the top 10 most parallel bus routes, we propose a methodology that evaluates the necessity of the bus stops along those routes. This approach aims to identify redundant segments along these routes, freeing up resources for better resource allocation.

1. Define Thresholds for Bus Stop Retention
We implemented two threshold criteria based on average passenger volumes:
- Inner Threshold: This threshold is applied to bus stops between two MRT stations on the same line. Stops below this threshold are likely redundant due to MRT connectivity. This threshold is calculated using the create_inner_threshold function, which aggregates passenger volumes for all distince in-between stops across Singapore and derives a value based on a specified quantile.
- Outer Threshold: For stops located outside the initial and final MRT stations on a route, evaluating their utility as feeder points. This threshold is calculated using the create_outer_threshold function, which aggregates passenger volumes for all stops on each route individually.

2. Process Bus Routes to Keep or Remove Bus Stops
Our process_bus_routes function uses these thresholds to label each stop as "keep" or "remove" based on its passenger volume. Specifically:
- For stops between MRT stations on the same line, the inner threshold is applied. If the average volume of the in-between stops is higher than the threshold, stops are kept. Else, it is removed
- For stops outside MRT boundaries, the outer threshold is applied. If the average volume of each stop is higher than the threshold, stops are kept. Else, it is removed

3. Next Steps for Implementation
We applied this method for the top 10 most parallel bus services identified using our parallelism scores. This produced a modified dataset (new_top_10_bus_data) where each stop is classified for retention or removal. Additionally, we produced top_10_buses_new_routes_only, focusing solely on routes where modifications were recommended.

We recommend deploying this methodology as an assessment tool integrated with real-time passenger data, enabling LTA to regularly evaluate the relevance of bus stops in relation to MRT lines. This will allow LTA to respond to public demand effectively, while cutting operational costs and increasing public satisfaction.

Furthermore, ensuring high data quality, particularly for passenger volumes, is crucial to avoid improper stop removals. Incorporating real-time or predictive data on passenger flow would further enhance accuracy, allowing LTA to refine resource allocation based on evolving commuter needs.

This method could be significantly enhanced with access to passenger volume data specific to each bus service. By capturing the unique passenger load for each bus and the individual stops they service, we could achieve a more precise assessment of each route’s utility. This would allow LTA to fine-tune their decisions, ensuring that routes are modified based not only on bus stop volumes but also on the demand of different bus services.

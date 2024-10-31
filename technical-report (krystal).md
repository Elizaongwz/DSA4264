# Technical Report

## Section 3: Methodology

### 3.1 Technical Assumptions
#### Assumption 1: 
Publicly accessible data limitations prevented us from obtaining exact ridership data for specific bus services. Instead, LTA DataMall provides "Passenger Volume by Bus Stop," which indicates passenger volumes at a given bus stop at specific hours of a weekday or weekend in each month. Additionally, DataMall only allows for calls on Passenger Volume by Bus Stop for the past three months, restricting our passenger volume data to July, August, and September of 2024. 

The available data records only tap-ins and tap-outs, without distinguishing between passengers ending their journey and those transferring to another bus service. Therefore, the aggregate number of tap-ins likely overestimates the actual number of commuting journeys, and similarly, tap-outs likely overestimate the count of passengers with final destinations near the respective bus stop. 
<img width="857" alt="Screenshot 2024-10-31 at 1 32 31 PM" src="https://github.com/user-attachments/assets/247dae2a-1403-4ea0-b8f3-53e1164ca686">

We assume that passenger volume at a given bus stop reasonably reflects the ridership of bus services that serve it. We acknowledge the limitation in this assumption, as each bus stop typically serves multiple bus services and ridership may be overstated when popular services contribute disproportionately to volume. 

Consequently, our evaluation of bus routes did not solely rely on ridership data when considering whether a route should be kept, modifed or removed all together. Our prioritisation of trunk bus routes follows a three-tiered approach, detailed in Section 3.3.

#### Assumption 2:
Our project also assumed a specific criteria to define when a section of a bus route qualifies as “parallel” to an MRT line in the second tier of calculating parallel scores. We defined a bus route segment as parallel if it falls within a 1km buffer zone around the MRT track and contains at least 8 consecutive bus stops within this buffer. Such a segment would be flagged as parallel and we would record which MRT line it corresponds to. 

We acknowledge that setting a threshold of 8 consecutive stops may vary in impact depending on the route length of each bus service; longer routes are more likely to meet this criterion, while shorter routes are less likely to do so. However, the aim of this parallel identification is to account for the extent and nature of MRT parallelism across bus routes, with a penalty applied to routes that align with multiple MRT lines. This approach helps differentiate longer bus routes, which are inherently more likely to intersect with multiple MRT lines, from shorter routes that may align with only one or no MRT lines.

#### Assumption 3:
In the third tier of calculating parallel scores, we assumed that buses that cover more than __% of the bus stops in a bus service would be classified as having a similar route, making that bus service more common. Under this assumption, services with common routes could be reasonably considered for modification, as commuters would have alternative options along these shared paths. The threshold of __% was selected based on our own experimentation with the dataset and concluded that this threshold best reflected similarity between bus routes. We recognise that this threshold may impose a limitation on shorter routes, as these inherently cover fewer stops and are less likely to meet the threshold to be classified as “similar.” 

However, the intent of this threshold is to highlight bus services with significant overlap, whose modification would be less likely to disrupt commuters due to alternative options. Although shorter routes fall outside this threshold, their exclusion is acceptable, as these routes generally serve more localised areas and are less likely to act as substitutes for other bus services.

### 3.3 Experimental Design
#### Parallel Scoring 
To aid LTA in identifying which trunk services can be kept, modified or removed, we derived a Parallel Scoring Method to score and rank current trunk services in the order of priority to be evaluated. Our approach utilises a three-tiered method to not only identify trunk services that are most parallel to the MRT, but also to factor in potentual commuter feedback from  modifying services.
Our approach is as follows:
<img width="490" alt="Screenshot 2024-10-31 at 2 28 39 PM" src="https://github.com/user-attachments/assets/c6b41296-c5c8-4cc5-b982-08d892f5a5a9">

##### Tier 1:
For the first tier of the Parallel Scoring Method, we calculate the "parallelism" of each bus route relative to the MRT network. This metric evaluates how closely each bus route aligns spatially and directionally with MRT lines.

First, we load and group the MRT line data from the shapefile by MRT_LINE. A LineString is created for each MRT line by sorting the station points by sequence (STN_SEQUEN) and connecting their centroids. These individual LineStrings are then combined into a single MultiLineString (mrt_multiline), representing the entire MRT system.

We then defined the geospatial functions that will be used to calculate how near and how parallel a bus route is to the MRT System.
The haversine function calculates the geographic distance between two points, which is critical in determining proximity between bus and MRT segments.
<img width="977" alt="Screenshot 2024-10-31 at 2 47 46 PM" src="https://github.com/user-attachments/assets/60ca5fda-9b43-4d3a-9c06-e30bcd966af6">

The calculate_bearing function computes the bearing (directional angle) between two points, allowing us to measure alignment between bus and MRT line segments.
<img width="919" alt="Screenshot 2024-10-31 at 2 48 10 PM" src="https://github.com/user-attachments/assets/5d99e8a7-c647-47f5-b1ab-cd32b8a9083f">

For each bus route, the calculate_route_parallelism function iterates over its segments.
For each segment: We find the nearest MRT segment using the minimum haversine distance and the bearing difference is computed between the bus segment and the nearest MRT segment, adjusting for cases where the difference exceeds 180 degrees.
<img width="913" alt="Screenshot 2024-10-31 at 2 42 08 PM" src="https://github.com/user-attachments/assets/b591e5a3-029d-436e-b5d9-4d979657346b">

Each segment receives a parallelism score inversely related to its distance from the MRT and bearing difference, this score is then weighted by segment length to moderate the effect of very long segments and derive the total parallelism score for a route.
The total parallelism score for a route is then normalised by the square root of its length, ensuring that longer routes don’t automatically receive inflated scores.
<img width="941" alt="Screenshot 2024-10-31 at 2 43 29 PM" src="https://github.com/user-attachments/assets/066ccf03-2855-40b4-9389-d745bcbf4291">

For each trunk bus service, the calculate_route_parallelism is applied, yielding a normalised parallelism score that reflects the route’s degree of alignment with MRT lines. These scores are then sorted in descending order, providing a ranked list of bus services based on their MRT parallelism, which supports prioritising bus services for evaluation.

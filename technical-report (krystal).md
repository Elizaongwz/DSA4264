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


### Assumption 3:
In the third tier of calculating parallel scores, we assumed that buses that cover more than __% of the bus stops in a bus service would be classified as having a similar route, making that bus service more common. Under this assumption, services with common routes could be reasonably considered for modification, as commuters would have alternative options along these shared paths. The threshold of __% was selected based on our own experimentation with the dataset and concluded that this threshold best reflected similarity between bus routes. We recognise that this threshold may impose a limitation on shorter routes, as these inherently cover fewer stops and are less likely to meet the threshold to be classified as “similar.” 

However, the intent of this threshold is to highlight bus services with significant overlap, whose modification would be less likely to disrupt commuters due to alternative options. Although shorter routes fall outside this threshold, their exclusion is acceptable, as these routes generally serve more localised areas and are less likely to act as substitutes for other bus services.

### 3.3 Experimental Design
#### Parallel Scoring 
To aid LTA in identifying which trunk services can be kept, modified or removed, we derived a Parallel Scoring Method to score and rank current trunk services in the order of priority to be evaluated. Our approach utilises a three-tiered method to not only identify trunk services that are most parallel to the MRT, but also to factor in potentual commuter feedback from  modifying services.
Our approach is as follows:

<img width="490" alt="Screenshot 2024-10-31 at 2 28 39 PM" src="https://github.com/user-attachments/assets/c6b41296-c5c8-4cc5-b982-08d892f5a5a9">



# Technical Report

## Section 3: Methodology

### 3.1 Technical Assumptions
*In this subsection, you should set out the assumptions that are directly related to your model development process. Some general categories include:*
* *How to define certain terms as variables*
* *What features are available / not available*
* *What kind of computational resources are available to you (ie on-premise vs cloud, GPU vs CPU, RAM availability)*
* *What the key hypotheses of interest are*
* *What the data quality is like (especially if incomplete / unreliable)*
#### Assumption 1: 
Publicly accessible data limitations prevented us from obtaining exact ridership data for specific bus services. Instead, LTA DataMall provides "Passenger Volume by Bus Stop," which indicates passenger volumes at a given bus stop at specific hours of a weekday or weekend in each month. Additionally, DataMall only allows for calls on Passenger Volume by Bus Stop for the past three months, restricting our passenger volume data to July, August, and September of 2024. 

The available data records only tap-ins and tap-outs, without distinguishing between passengers ending their journey and those transferring to another bus service. Therefore, the aggregate number of tap-ins likely overestimates the actual number of commuting journeys, and similarly, tap-outs likely overestimate the count of passengers with final destinations near the respective bus stop. 
<img width="857" alt="Screenshot 2024-10-31 at 1 32 31 PM" src="https://github.com/user-attachments/assets/247dae2a-1403-4ea0-b8f3-53e1164ca686">

Our primary assumption is that passenger volume at a given bus stop reasonably reflects the ridership of bus services that serve it. We acknowledge the limitation in this assumption, as each bus stop typically serves multiple bus services and ridership may be overstated when popular services contribute disproportionately to volume. 

Consequently, our evaluation of bus routes did not solely rely on ridership data when considering whether a route should be kept, modifed or removed all together. Our prioritisation of trunk bus routes follows a three-tiered approach, detailed in Section 3.3.

#### Assumption 2:
Our project also assumed a specific criteria to define when a section of a bus route qualifies as “parallel” to an MRT line in the second tier of calculating parallel scores. We defined a bus route segment as parallel if it falls within a 1km buffer zone around the MRT track and contains at least 8 consecutive bus stops within this buffer. Such a segment would be flagged as parallel and we would record which MRT line it corresponds to. 

We acknowledge that setting a threshold of 8 consecutive stops may vary in impact depending on the route length of each bus service; longer routes are more likely to meet this criterion, while shorter routes are less likely to do so. However, the aim of this parallel identification is to account for the extent and nature of MRT parallelism across bus routes, with a penalty applied to routes that align with multiple MRT lines. This approach helps differentiate longer bus routes, which are inherently more likely to intersect with multiple MRT lines, from shorter routes that may align with only one or no MRT lines.


### 3.3 Experimental Design


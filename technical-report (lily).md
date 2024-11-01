# Technical Report

## Section 4: Findings

### 4.1 Results

We found that routes with high parallelism scores tend to:
  1. Serve densely populated and high-demand corridors particularly in the corners of Eastern and North-Eastern regions where MRT stations are getting more accessible as well as Central to Northern regions       with a high volume of different bus services.
  2. Have parallelism scores that are generally lower in the Western region, with routes either running shorter distances or do not overlap with multiple MRT lines, leading to diluted parallelism scores.
  3. Exhibit longer total route distances, often mirroring the trajectory of MRT lines over extended stretches without significant deviations.
  4. Operate with frequent service intervals, likely responding to high ridership demand along these parallel paths.

On the opposite end, trunk routes with scores below 0.2 are often feeder routes or those with unique trajectories, serving specific areas without MRT overlap. These results indicate that a smaller proportion of trunk bus services are tailored to provide access to areas that MRT lines do not directly serve but help to bridge connectivity gaps in the network.

![Screenshot 2024-11-01 at 1 43 39 AM](https://github.com/user-attachments/assets/1a111357-e8d3-4b08-a994-f698f3bb5d16)

With our definition of parallel routes, our tri-part parallelism score model identified bus routes 966, 63, and 31 as the most parallel to MRT lines, achieving the highest relative parallelism scores of 1.0, 0.98, and 0.93, respectively. These routes exhibit a strong alignment in direction and proximity with specific MRT lines, particularly maintaining consistent bearings and minimal deviations from the routes taken by these rail lines. Additionally, they are primarily aligned with only one or two different MRT lines, which reduces route complexity and makes them highly comparable to specific MRT services. They exhibit a high degree of overlap in bus stops with other services, making them easily replaceable with many available alternative bus services that could be taken.

These findings were integrated with GIS mapping tools for visualizing transit redundancies or gaps in underserved areas. Our interactive SHAP visualizations and parallelism score maps created during this project allow transportation authorities to make data-driven decisions to optimize route configurations further.

#### Bus Route 966:
<img width="1214" alt="Screenshot 2024-11-01 at 9 01 05 PM" src="https://github.com/user-attachments/assets/f0c0a9af-e97b-4360-ba28-053eda57f0bc">

#### Bus Route 63:
<img width="1218" alt="Screenshot 2024-11-01 at 9 03 27 PM" src="https://github.com/user-attachments/assets/09316cfc-f9ad-4b39-9be8-360be722c058">

#### Bus Route 31:
<img width="1187" alt="Screenshot 2024-11-01 at 9 04 24 PM" src="https://github.com/user-attachments/assets/a3ddbc70-b5b1-46ab-8c0d-8e9aad67161c">

Out of over 400 evaluated routes, only a small fraction (approximately 5%) achieved a parallelism score above 0.8, underscoring that true MRT-bus parallelism is relatively rare across the network. The majority of routes showed scores below 0.5, suggesting that most bus routes operate in corridors that are less directly served by MRT lines. This distribution hints at complementary rather than competitive positioning of most bus routes relative to MRT services. The clear identification of high-scoring routes provides transit authorities with a targeted set of routes for further study and potential adjustments.
![parallel_score_distribution](https://github.com/user-attachments/assets/8b013374-889b-4f10-afe3-32de7e08698e)

### 4.2 Discussion
#### 4.2.2 Significance of key features of the model
##### Step 1 

##### Step 2

##### Step 3

#### 4.2.3 Potential Biases in the Model
Several potential biases may emerge from employing the three-step approach in calculating parallelism scores.

##### Bias 1: Bearing Similarity
There could potentially be an overemphasis with directional consistency. The emphasis on bearing similarity may disadvantage routes that do not strictly align directionally with MRT lines due to road network constraints or urban layout. In dense urban areas or complex suburban layouts, road infrastructure often requires bus routes to take winding or indirect paths to serve neighborhoods, shopping centers, and other key destinations. These routes may still operate within the same transit corridor as an MRT line but appear less parallel because of necessary turns or adjustments to serve local demand. Routes that are more winding and take frequent turns to access residential or commercial areas receive lower scores, even if they effectively serve the same transit corridors as MRT lines. 

##### Bias 2: Multi-Line Consistency 
Routes that facilitate transfers between MRT lines or provide crosstown connectivity may be over-scored, despite their essential role in improving network flexibility. Stations with high MRT line densities may appear to have high parallelism scores indicating parallelism to limited MRT lines yet serve broader connectivity needs. For instance, Outram Park MRT station serves as a connection between 3 different MRT lines: Thomson-East Coast Line, North-East Line and East-West Line. A bus that travels parallel to the East-West Line receives a higher parallelism score without taking into account stations such as Outram Park that can increase assesibility to other MRT lines, and should be scored lower.

##### Bias 3: Bus Stop Overlap
Routes passing through high-traffic stops near MRT stations or central transit areas may receive inflated parallelism scores due to frequent stop overlap. This bias is particularly pronounced in densely populated urban centers, where high stop overlap can give an inaccurate representation of a route’s functional redundancy with MRT services; their parallelism score can be inflated depending on the length of the entire route. Routes that are much shorter and go through multiple popular bus stops would be overscored yet primarily serve densely populated areas not covered by MRT, rather than assessing their unique transit contributions. This results in overvaluation of long-distance routes that partially overlap with MRT lines, even if a large segment of the route aligns and are parallel with MRT service areas.

##### Bias 4: Lack of Demand-Sensitive Scoring 
The current scoring process does not incorporate ridership data or information about actual passenger demand, which could lead to inflated parallelism scores for routes that follow MRT lines yet still experience high utilization by commuters. Without considering demand, the model may inadvertently overvalue routes that appear redundant on the basis of route alignment but, in practice, fulfill a distinct role in the transit network due to high passenger usage.

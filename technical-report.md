# Technical Report

**Project: {insert project name}**  
**Members: {insert project members}**  
Last updated on {last updated date}

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

*In this subsection, you should explain how you will measure or assess success for your data science project. You need to specify at least 2 business and/or operational goals that will be met if this project is successful. Business goals directly relate to the business’s objectives, such as reduced fraud rates or improved customer satisfaction. Operational goals relate to the system’s needs, such as better reliability, faster operations, etc.*

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

*In this subsection, you should provide a clear and detailed explanation of how your data is collected, processed, and used. Some specific parts you should explain are:*
* *Collection: What datasets did you use and how are they collected?*
* *Cleaning: How did you clean the data? How did you treat outliers or missing values?*
* *Features: What feature engineering did you do? Was anything dropped?*
* *Splitting: How did you split the data between training and test sets?*

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

*In this subsection, you should highlight your recommendations for what to do next. For most projects, what to do next is either to deploy the model into production or to close off this project and move on to something else. Reasoning about this involves understanding the business value, and the potential IT costs of deploying and integrating the model.*

*Other things you can recommend would typically relate to data quality and availability, or other areas of experimentation that you did not have time or resources to do this time round.*
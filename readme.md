# Leveraging Collective Intelligence for Bug Triaging in a Knowledge Graph-based System

## Problem Statement
In software development, problem triage is a difficult process that requires efficient assignment of bugs to the right team members for resolution. Traditional methods are often time-consuming and error-prone, resulting in ineffective and incorrect sorting.

## Significance of the problem
The individuals responsible for assigning bug solutions to developers, known as triagers, are experiencing a heavy workload due to the high volume of bug reports submitted to the bug repository. Various techniques, including machine learning algorithms and social media metrics, have been suggested to determine the appropriate developer to address a bug report, with the aim of reducing the workload of triagers.

### Empirical Study
According to Eclipse project reports, it often takes 40 days for an issue to be assigned to the first dev, and another 100 days or more for the bug to be assigned to the second dev. Similarly, a Mozilla project takes an average of 180 days for an initial assignment and another 250 days if the initial programmer is unable to resolve the issue. These figures show that the considerable work required to resolve the errors is due to the lack of effective, automated strategies for matching and reducing discards.

## Brief Description of the Solution Approach
The basis of our work starts with using a graph-based approach by creating a more visual notation of bugs and devs. We want to divide all the devs according to the type of bugs that they resolved.  That is we form a community of devs based on their expertise in a particular type of node, the trust developed due to solving bugs in the least amount of time, decay time, the severity of bugs, and the priority of bug resolved. We then recommend the best community to resolve the bug based on the component of the bug, along with the top 5 devs in that community that are most likely to solve it earliest.

## Building the KG  using dataset
![image13](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/b6c6562c-4e8a-46b2-9f1a-7ebff2779d06)

## Building KG using Bug_Resolution_Performance_Index and expertise score
![image31](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/0381e4b9-a30d-4884-b251-a805015d939a)

## Cypher Queries Answered 
### Calculating the expertise score of devs based on bugs solved and components worked on.	
![image20](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/df711f07-dbf2-49a6-baf4-9f4f3681b197)

### Calculating Bug_Resolution_Performance_Index of devs based on solving time.
![image4](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/045b16ac-350c-42c9-908f-7d35e2668c5e)

### Calculating the decay factor of devs based on average solving time and days since the bug was resolved.
![image42](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/81d81dc0-6bdd-4282-830c-ddca5e44f3cc)

## Calculating Credibility Score using different weights and storing in CSV file
Formula for Credibility Score:
![image19](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/043079d6-5ecb-4628-aedd-052b6078715c)

Where:
a is the weight assigned to the Bug Resolution Performance Index
b is the assigned weight of the expertise score 
c is the assigned weight of the decay factor
Bug_Resolution_Performance_Index is a measure of how well the dev has resolved bugs in the past
expertise_score is a measure of the dev's expertise in the component
decay_factor is a measure of how recent the dev has worked on the component

## Validation
### Accuracy
![image28](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/96808509-4ae2-4cfe-a1b3-5a1154721c91)
Result:
Case1:  when a=0.25, b=0.5, c=0.25
Case 2: when a=0.2, b=0.6, c=0.2
Case 3:when a=0.3, b=0.4, c=0.3
Case 4: when a=0.3,b=0.3,c=0.4
#### Accuracy Table
![image35](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/fd14877d-ee85-4804-bbc9-bf2db0559a30)

## Visualizing Graph of Accuracy
![image39](https://github.com/Mystic-Trooper/bug-triaging-2/assets/71957235/f2cd2b1e-f8b1-458c-ad55-328b383f9b64)
The link between a project's correctness and the number of devs working on it is seen in the graph. The correctness of the project is shown by the y-axis, while various cases or situations are represented by the x-axis.

The graph has three lines, each of which represents the project's accuracy for a different number of devs. The accuracy for five devs is shown by the blue line, for ten devs by the orange line, and for fifteen devs by the green line.

The graph shows that when the number of devs rises, the project's accuracy tends to rise as well. For instance, in scenario 1, 5 devs' accuracy is around 0.69, whereas 15 devs' accuracy is approximately 0.83. However, in other circumstances, as in scenario 3, the accuracy declines as the number of devs rises.

In general, this graph indicates that more devs working on a project can result in more accuracy, but there may be additional variables at work that might influence the link between the number of devs and the accuracy of the project.

# Building Graph-Based Dataset Recommendation System

## Project Overview
#### Background 
Exploring and finding existent research datasets and the relational network among themselves, between datasets and entities of interest such as research fields, paper titles, authors, and research methods are *shown to be inefficient* and the lack an integrated online platform that improves this process. This capstone project connects datasets with various entities in the academic research entities such as the publication papers that were used, the authors, the research field involved, as well as the subject terms given to the dataset. This heterogenous knowledge graph is built in order to improve user experience by building a dataset recommendation system based on the network. We use offline evaluation to assess the performance of our system. Two of the model outputs from the Rich Context Competition, a competition held by Coleridge Initiative to develop automatic extraction of dataset mentions, methodology, and reserach field from publication papers. Our improved network by adding additional subject terms entity shows better connectivity based on a similarity matrix that prioritizes the shortest path between two datasets. And a second updated network replacing research fields with author entity shows even better connectivity. As we apply different connections of nodes and weighted edges in our network and define different similarity matrices, we expect to produce a network model with the best performance and build our recommendation system on it. 

#### Problem Statement
* Great data go undiscovered and are undervalued
* Time and resources are wasted redoing empirical work
* No existing recommendation system for datasets

#### Our Goal
* Build a dataset recommendation system to improve research efficiency.

#### Our Approach
* Build a heterogenous knowledge graph network. 
* Exploit information to develop a more well connected network.
* Use link prediction to measure connectivity between nodes. 

## DEMO
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/RbY7AwgOlRc/0.jpg)](http://www.youtube.com/watch?v=RbY7AwgOlRc)

<video src="demo_diabetes.mov" width="320" height="200" controls preload></video>

# Rich Context Capstone
#### Center for Urban Science & Progress, New York University 2019
### Recommendation system of datasets for the ICPSR dataset archive.
Exploring and finding existent research datasets and the relational network among themselves, between datasets and entities of interest such as research fields, paper titles, authors, and research methods are *shown to be inefficient* and the lack an integrated online platform that improves this process. This capstone project connects datasets with various entities in the academic research entities such as the publication papers that were used, the authors, the research field involved, as well as the subject terms given to the dataset. This heterogenous knowledge graph is built in order to improve user experience by building a dataset recommendation system based on the network. We use offline evaluation to assess the performance of our system. Two of the model outputs from the Rich Context Competition, a competition held by Coleridge Initiative to develop automatic extraction of dataset mentions, methodology, and reserach field from publication papers. Our improved network by adding additional subject terms entity shows better connectivity based on a similarity matrix that prioritizes the shortest path between two datasets. And a second updated network replacing research fields with author entity shows even better connectivity. As we apply different connections of nodes and weighted edges in our network and define different similarity matrices, we expect to produce a network model with the best performance and build our recommendation system on it. 

# Getting Started
### Setting up Environment
After cloning the repository, install the prerequisites:
`pip install -r requirements.txt`

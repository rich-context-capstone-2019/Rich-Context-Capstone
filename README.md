# Rich Context Capstone
#### Center for Urban Science & Progress, New York University 2019
### Recommendation system of datasets for the ICPSR dataset archive.
Exploring research datasets and their relational network between one and the others, and between datasets and entities of interest, such as research fields, paper titles, authors, and citation counts, are currently inefficient and lack an integrated online platform that improves this process. This capstone project connects datasets with various entities in the papers that use them and with other related papers. It improves user experience by building a dataset recommendation system based on a graph model. We create this system based on model outputs from the Rich Context Competition which showed weak mean relationship scores between datasets, publications, and research fields. We developed a novel evaluation metric to assess the performance of our system based on our what our definition of a good dataset recommendation system. Our previous network version adding keywords entity shows better connectivity based on a similarity matrix that prioritizes the shortest path between two datasets. And our latest knowledge network remapping fields of study entity and adding author entity shows even better connectivity. After we apply different connections of nodes and weighted edges in our network and define different similarity matrices, we produce a network model with the best performance and build our recommendation system on it. This recommendation system can be very useful when integrated with an interactive search engine and lead researches in all domains.

# Getting Started
### Setting up Environment
After cloning the repository, install the prerequisites:
`pip install -r requirements.txt`

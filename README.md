# Post Frequency Tracker with CountMinSketch

This project allows you to fetch posts from the Bluesky API, process them to track the frequency of specific words using a **CountMinSketch** algorithm, and query the frequency of a given word. The CountMinSketch is a probabilistic data structure that allows for efficient frequency estimation in large datasets.

## Installation

To run this project, you need Python 3.7+ installed on your system. Follow these steps to get started:

1. Clone the repository:
   git clone https://github.com/audreyper/bluesky-cms.git


2. Navigate to the project directory:

cd repository-name

3. Install dependencies:

pip3 install -r requirements.txt

4. Run the script:

python3 bluesky-cms.py


## Configurations

The search query (e.g., query = "outage") can be modified to retrieve posts related to different topics. The script then applies the CountMinSketch algorithm to track word frequencies within the posts returned from the query. To query the frequency of any specific word, simply adjust the word_to_query variable.

### Environment Variable

This project requires the API URL to be set as an environment variable. 
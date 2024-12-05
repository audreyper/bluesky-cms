import json
import requests
import hashlib
import os

# Define CountMinSketch class for processing
class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        # Create a table of zeros
        self.table = [[0] * width for _ in range(depth)]

    def hash_function(self, item, i):
        # Compute the hash value and return an index in the table.
        # Hash the item and get an index in the range of width
        return int(hashlib.md5((str(item) + str(i)).encode()).hexdigest(), 16) % self.width

    def add(self, item):
        # Increment counters for the given item.
        for i in range(self.depth):
            index = self.hash_function(item, i)
            self.table[i][index] += 1

    def query(self, item):
        # Query for the frequency of the item.
        result = min(self.table[i][self.hash_function(item, i)] for i in range(self.depth))
        return result

# Function to search posts
def search_posts(query):
    try:
        # Build the request URL
        url = os.getenv("BLUESKY_API_URL")

        if not url:
            raise ValueError("API URL is missing. Please set the BLUESKY_API_URL environment variable.")
        
        # Send the search request
        response = requests.get(
            url,
            params={
                "q": query,  
                "sort": "latest",  
                "limit": 50,  
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Error fetching posts: {response.text}")

        # Parse the response as JSON
        posts_data = response.json()
        return posts_data
    except Exception as e:
        raise Exception(f"Error searching posts: {str(e)}")

# Main function to handle processing posts and tracking words
def main():
    try:
        # Define the search query when fetching from the bluesky api
        query = "outage"

        # Initialize CountMinSketch with width and depth
        cms = CountMinSketch(width=1000, depth=5)

        # Fetch posts based on the query
        post_data = search_posts(query)

        # Extract words and update CountMinSketch
        for post in post_data.get('posts', []):  
            record = post.get('record', {})
            content = record.get('text', "")

            words = content.split()  # Split content into words
      
            # Update CountMinSketch with the words
            for word in words:
                cms.add(word.lower())  # Convert words to lowercase for consistent tracking

        # Query the frequency of a specific word after fetching posts based on a certain query
        word_to_query = "power"
        frequency = cms.query(word_to_query.lower())
        print(f"Estimated frequency of '{word_to_query}' from posts that contain '{query}': {frequency}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()


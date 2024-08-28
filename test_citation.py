from scholarly import scholarly
import re
import os
from urllib.parse import urlparse

def get_scholar_profile_url(author_name):
    try:
        # Search for the author
        search_query = scholarly.search_author(author_name)
        # Get the first result (most relevant)
        author = next(search_query)
        
        # Retrieve the author's data
        author = scholarly.fill(author)
        
        # Get the scholar id
        scholar_id = author['scholar_id']
        
        # Construct the Google Scholar profile URL
        profile_url = f"https://scholar.google.com/citations?user={scholar_id}"
        
        return profile_url
    except StopIteration:
        return f"No Google Scholar profile found for {author_name}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_citation_count_from_url(profile_url):
    try:
        # Extract the user ID from the URL
        user_id_match = re.search(r'user=([^&]+)', profile_url)
        if not user_id_match:
            return "Invalid Google Scholar profile URL"
        
        user_id = user_id_match.group(1)
        
        # Retrieve the author's data using the user ID
        author = scholarly.search_author_id(user_id)
        author = scholarly.fill(author)
        
        # Get the total citations
        total_citations = author['citedby']
        
        return total_citations
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_citation_count_from_search(author_search):
    profile_url = get_scholar_profile_url(author_search)
    citations = get_citation_count_from_url(profile_url)
    return citations 


def cv_filename_to_name(filename):
    # Remove the file extension
    name_without_extension = os.path.splitext(filename)[0]
    
    # Split the name by underscores or spaces
    parts = re.split(r'[/]', name_without_extension)
    parts = parts[-1]
    parts = re.split(r'[_]', parts)
    # Remove any year or date that might be at the end
    parts = [part for part in parts if not part.isdigit()]
    
    # Capitalize each part and join them with a space
    name = ' '.join(part.capitalize() for part in parts)
    
    return name


# Example usage
if __name__ == "__main__":
    author_search = "Jakša Cvitanic"
    citations = get_citation_count_from_search(author_search)
    try: 
        float(citations)
        print(f"Total citations for {author_search}: {citations}")
    except:
        print(f"No Google Scholar profile found for {author_search}")

import os
import time
import requests

import json

from mistralai import Mistral

########################################### Google Search Function ###########################################

# #############################
# # Search Function with lynx #
# #############################
def search_google(query):
    formatted_query = f"{query} submission date for this year. Only from real and original site."
    formatted_query = formatted_query.replace(" ", "+")
    
    # Run lynx to fetch Google search results
    cmd = f'lynx -dump "http://www.google.com/search?q={formatted_query}" > search_results.txt'
    os.system(cmd)
    
    # Extract context around mentions of submission-related terms
    with open("search_results.txt", "r") as f:
        content = f.read()
    
    # only consider the first 3500 characters
    content = content[:3500]
    print(content)
    
    # Find all occurrences of relevant terms and get surrounding context
    results = []
    content_lower = content.lower()
    search_terms = ["submission deadline"]
    
    for search_term in search_terms:
        pos = 0
        while True:
            pos = content_lower.find(search_term, pos)
            if pos == -1:
                break
            
            # Get 50 characters before and after the occurrence
            num_chars_extension = 350
            start = max(0, pos - num_chars_extension)
            end = min(len(content), pos + len(search_term) + num_chars_extension)
            context = content[start:end]
            results.append(context)
            pos += len(search_term)
    
    # Take only the first 3 results to avoid overwhelming
    # results = results[0:2]

    # Join all contexts with separators
    final_content = "\n---\n".join(results) if results else "No relevant submission information found."
    
    # Save search
    with open("search.txt", "w") as f:
        f.write(final_content)
    
    # Clean up
    os.remove("search_results.txt")

# ###############################
# # Search Function with Google #
# ###############################
# # # Your Google Custom Search API key and Search Engine ID (replace with your actual values)
# # API_KEY = "AIzaSyCRkJq_4_3dGcF1l0HPpDv_jBn0GCM5RN0"
# # SEARCH_ENGINE_ID = "b10331df8102b41bf"  # Replace with your Custom Search Engine ID

# # # Function to perform a Google search using the Custom Search JSON API
# # def search_google(query):
# #     formatted_query = f"{query} submission date for this year. Only from real and original site."
# #     formatted_query = formatted_query.replace(" ", "+")

# #     # Google Custom Search API endpoint
# #     url = f"https://www.googleapis.com/customsearch/v1?q={formatted_query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"

# #     # Send a request to the Google API
# #     response = requests.get(url)
    
# #     if response.status_code == 200:
# #         search_results = response.json()
# #         contexts = []

# #         # Extract search result titles and snippets
# #         for item in search_results.get('items', []):
# #             snippet = item.get('snippet', '')
# #             link = item.get('link', '')
            
# #             # Check for relevant terms in the snippet
# #             if "submit" in snippet.lower() or "submission" in snippet.lower() or "submitted" in snippet.lower():
# #                 contexts.append(f"Context: {snippet}\nLink: {link}\n")

# #         # Return extracted contexts or a default message if none are found
# #         return "\n---\n".join(contexts) if contexts else "No relevant submission information found."
    
# #     else:
# #         return f"Error: Unable to fetch results, status code: {response.status_code}"

# ########################################### Google Search Function ###########################################

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
from mistralai import Mistral

########################################### DuckDuckGo Search Function ###########################################

# def search_google(query):
#     """
#     Search for conference submission dates using DuckDuckGo via Selenium.
#     DuckDuckGo is less likely to show CAPTCHA challenges than Google.
#     Extracts and returns context around mentions of submission-related terms.
#     """
#     # Format the query to specifically look for submission dates
#     formatted_query = f"{query} submission date deadline"
    
#     # Set up Chrome options for headless browsing
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     # Add a user agent that looks like a regular browser
#     user_agents = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
#     ]
#     options.add_argument(f"user-agent={random.choice(user_agents)}")
    
#     # Initialize the Chrome driver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
#     try:
#         # Use DuckDuckGo instead of Google to avoid CAPTCHA
#         driver.get("https://duckduckgo.com/")
        
#         # Allow time for the page to load
#         time.sleep(2)
        
#         # Find the search box and enter query
#         try:
#             search_box = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.ID, "searchbox_input"))
#             )
#             search_box.clear()
#             search_box.send_keys(formatted_query)
#             search_box.send_keys(Keys.RETURN)
            
#             # Wait for results to load
#             time.sleep(3)
            
#         except Exception as e:
#             print(f"Error interacting with DuckDuckGo search: {e}")
#             # Direct URL approach as fallback
#             driver.get(f"https://duckduckgo.com/?q={formatted_query.replace(' ', '+')}")
#             time.sleep(3)
        
#         # Get the page source
#         content = driver.page_source
        
#         # Extract the text content from the HTML
#         soup = BeautifulSoup(content, 'html.parser')
        
#         # Try to focus on the main search results
#         results_area = soup.find('div', {'id': 'links'}) or soup.find('div', {'class': 'results'})
#         text_content = results_area.get_text() if results_area else soup.get_text()
        
#         # Find all occurrences of relevant terms and get surrounding context
#         results = []
#         text_content_lower = text_content.lower()
#         search_terms = ["submission deadline"]
        
#         for search_term in search_terms:
#             pos = 0
#             while True:
#                 pos = text_content_lower.find(search_term, pos)
#                 if pos == -1:
#                     break
                
#                 # Get extended context around the occurrence
#                 num_chars_extension = 300
#                 start = max(0, pos - num_chars_extension)
#                 end = min(len(text_content), pos + len(search_term) + num_chars_extension)
#                 context = text_content[start:end]
#                 results.append(context)
#                 pos += len(search_term)
        
#         # Take only the first 3 results to avoid overwhelming
#         results = results[0:2]
#         final_content = "\n---\n".join(results) if results else "No relevant submission information found."
        
#         # Save search results to file
#         with open("search.txt", "w") as f:
#             f.write(final_content)

#         print('#############################################')
            
#         return final_content
        
#     finally:
#         # Clean up
#         driver.close()
#         driver.quit()

#############################
# Print Num Confs Functions #
#############################
def print_conference_names():
    """Print all conference names from the loaded JSON data"""
    conferences = conference_json["conferences"]
    print(f"List of all conferences ({len(conferences)}):")
    print()

############################
# LLM CALL TO EXTRACT DATE #
############################
def extract_date_from_text(text, conf_name):
    api_key = "WqZbYQALu5PqyOVHd1g87np5s7rfaD60"
    model   = "mistral-small-latest"
    client  = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role":  "user",
                "content": f"""Based on the following search results for a conference, extract ONLY the paper submission deadline date.
                There will be multiple dates in the search results, but you need to extract the paper submission deadline date.

                Conference: {conf_name}
                Search Results: {text}
                
                Format your response as ONLY the date in YYYY-MM-DD format. If you cannot find a specific date, respond with 'Unknown'.
                Do not include any explanations, notes, or additional text in your response. Just the date or 'Unknown'.""",
            },
        ]
    )
    return chat_response.choices[0].message.content

###########################
# Update JSON with dates  #
###########################
def update_json_with_dates(dates_collected):
    for conference in conference_json["conferences"]:
        conference_name = conference["name"]
        if conference_name in dates_collected:
            conference["submission_date"] = dates_collected[conference_name]
    with open("/home/localssk23/conf_track/conferences.json", "w") as file:
        json.dump(conference_json, file, indent=4)
    print("JSON file updated successfully")

# Main execution function
def main():
    # Read the JSON file
    global conference_json
    with open("/home/localssk23/conf_track/conferences.json", "r") as file:
        conference_json = json.load(file)
    print('JSON file read successfully')
    print()

    # Print all conference names
    # print_conference_names()

    # Get a list of all conference names
    conference_names = [conference["name"] for conference in conference_json["conferences"]]
    
    # Uncomment to limit number of conferences for testing
    conference_names = conference_names[:1]
    
    dates_collected = {}

    # for conf_name in conference_names:
    #     try:
    #         search_results = search_google(conf_name)
    #         print(f"\nSearching for: {conf_name}")
    #         print("Search Results (Preview):")
    #         print(search_results[:300] + "..." if len(search_results) > 300 else search_results)
            
    #         llm_extracted_date = extract_date_from_text(search_results, conf_name)
    #         print(f"Extracted date from LLM: {llm_extracted_date}")
    #         dates_collected[conf_name] = llm_extracted_date
    #     except Exception as e:
    #         print(f"Error processing {conf_name}: {str(e)}")
    #         dates_collected[conf_name] = "Error"
        
    #     # Add a pause between requests to avoid rate limiting
    #     print("Waiting 3 seconds before next request...")
    #     time.sleep(3)

    print(conference_names)

    for conf_name in conference_names:

        search_results = search_google(conf_name)
        print(f"\nSearching for: {conf_name}")
        print("Search Results (Preview):")
        # print(search_results[:300] + "..." if len(search_results) > 300 else search_results)
        print(search_results)
        
        # Add a pause between requests to avoid rate limiting
        print("Waiting 3 seconds before next request...")
        time.sleep(3)
        print()

    # Update the JSON file with the extracted dates
    # update_json_with_dates(dates_collected)

    for conf_name, date in dates_collected.items():
        print(f"{conf_name}: {date}")
if __name__ == "__main__":
    main()
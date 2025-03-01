import sys
import os

def search_google(query):
    formatted_query = f"{query} submission date for this year. Only from real and original site."
    formatted_query = formatted_query.replace(" ", "+")
    
    # Run lynx to fetch Google search results
    #? https://www.reddit.com/r/commandline/comments/y4cv18/googling_in_the_terminal_presenting_googlesh/
    cmd = f'lynx -dump "http://www.google.com/search?q={formatted_query}" > search_results.txt'
    os.system(cmd)
    
    # Extract the first 1000 characters
    with open("search_results.txt", "r") as f:
        content = f.read(2500)
    
    # Save search
    with open("search.txt", "w") as f:
        f.write(content)
    
    # Clean up
    os.remove("search_results.txt")
    
    # Print results
    print(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
    else:
        search_term = input("Enter the conference name: ")
    
    search_google(search_term)

# exmaple of how to run the code
# python search.py "International Conference on Machine Learning"
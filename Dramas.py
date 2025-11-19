# Install imdbpy if not already installed
# pip install imdbpy
try:
    from imdb import IMDb
except ModuleNotFoundError:
    import sys
    print("IMDbPY package 'imdb' not found. Install it with: pip install imdbpy")
    sys.exit(1)

# -------------------------
# FUNCTIONS
# -------------------------

def get_top_tv_shows(n=50):
    """
    Fetch top n TV shows from IMDb using IMDbPY
    Returns a list of dictionaries with metadata
    """
    rr = IMDb()
    top_shows = rr.get_top50_tv()  # IMDbPY provides top 50 TV shows
    
    tv_data = []
    for show in top_shows[:n]:
        tv_data.append({
            "Title": show.get('title', 'N/A'),
            "Year": show.get('year', 'N/A'),
            "Rating": show.get('rating', 'N/A'),
            "Genres": ", ".join(show.get('genres', [])) if show.get('genres') else 'N/A',
            "URL": f"https://www.imdb.com/title/tt{show.movieID}/"
        })
    return tv_data

def display_list(data):
    """Display numbered list of TV shows"""
    for i, item in enumerate(data, start=1):
        print(f"{i}. {item['Title']} ({item['Year']}) - Rating: {item['Rating']}")

def create_smaller_lists(data):
    """
    Let the user create smaller lists from the main list
    Returns a dictionary of lists
    """
    groups = {}

    while True:
        group_name = input("\nEnter a new list name (or type END to finish): ")
        if group_name.lower() == "end":
            break

        groups[group_name] = []
        display_list(data)

        print(f"\nSelect item numbers for '{group_name}' (comma separated):")
        selections = input("Enter numbers: ")

        try:
            chosen = [int(num.strip()) for num in selections.split(",")]
            for index in chosen:
                if 1 <= index <= len(data):
                    groups[group_name].append(data[index - 1])
                else:
                    print(f"Ignored invalid index: {index}")
        except:
            print("Invalid input. Skipping this group.")
    
    return groups

def save_lists_to_files(main_list, groups):
    """Save main list and smaller lists to text files"""
    
    # Save main list
    with open("top_tv_shows.txt", "w", encoding="utf-8") as f:
        for tv in main_list:
            for k, v in tv.items():
                f.write(f"{k}: {v}\n")
            f.write("-" * 50 + "\n")

    # Save smaller groups
    for group_name, items in groups.items():
        filename = f"{group_name.replace(' ', '_').lower()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for tv in items:
                for k, v in tv.items():
                    f.write(f"{k}: {v}\n")
                f.write("-" * 50 + "\n")

    print("\nAll lists saved successfully!")

# -------------------------
# MAIN PROGRAM
# -------------------------

print("=== IMDb TV Show Metadata Collector ===")
tv_list = get_top_tv_shows(n=50)

print(f"\nFetched {len(tv_list)} TV shows.\n")
display_list(tv_list)

# Let user create smaller lists
groups = create_smaller_lists(tv_list)

# Save all lists to text files
save_lists_to_files(tv_list, groups)

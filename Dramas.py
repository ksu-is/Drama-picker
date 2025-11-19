from imdb import IMDb

# -------------------------
# FUNCTIONS
# -------------------------

def get_top_tv_shows(n=50):
    """
    Fetch top n TV shows from IMDb using IMDbPY
    Returns a list of dictionaries with metadata
    """
    ia = IMDb()
    top_shows = ia.get_top50_tv()  # IMDbPY provides top 50 TV shows

    tv_data = []
    for idx, show in enumerate(top_shows[:n], start=1):
        tv_data.append({
            "Number": idx,
            "Title": show.get('title', 'N/A'),
            "Year": show.get('year', 'N/A'),
            "Rating": show.get('rating', 'N/A'),
            "Genres": ", ".join(show.get('genres', [])) if show.get('genres') else 'N/A',
            "URL": f"https://www.imdb.com/title/tt{show.movieID}/"
        })
    return tv_data

def display_list(data):
    """Display numbered list of TV shows"""
    for item in data:
        print(f"{item['Number']}. {item['Title']} ({item['Year']}) - Rating: {item['Rating']}")

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
                for item in data:
                    if item['Number'] == index:
                        groups[group_name].append(item)
        except:
            print("Invalid input. Skipping this group.")

    return groups

def save_lists_to_files(main_list, groups, filename_prefix="imdb_tv"):
    """Save main list and smaller lists to text files"""
    main_filename = f"{filename_prefix}_main.txt"
    with open(main_filename, "w", encoding="utf-8") as f:
        for item in main_list:
            for key, value in item.items():
                f.write(f"{key}: {value}\n")
            f.write("-" * 50 + "\n")
    print(f"Main list saved to {main_filename}")

    for group_name, items in groups.items():
        filename = f"{filename_prefix}_{group_name.replace(' ', '_').lower()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for item in items:
                for key, value in item.items():
                    f.write(f"{key}: {value}\n")
                f.write("-" * 50 + "\n")
        print(f"Group '{group_name}' saved to {filename}")

# -------------------------
# MAIN PROGRAM
# -------------------------
def main():
    print("Fetching top IMDb TV shows...")
    tv_list = get_top_tv_shows(n=50)
    print(f"\nFetched {len(tv_list)} TV shows.\n")
    display_list(tv_list)

    # Create smaller lists
    groups = create_smaller_lists(tv_list)

    # Save all lists
    save_lists_to_files(tv_list, groups, filename_prefix="imdb_tv")

if __name__ == "__main__":
    main()

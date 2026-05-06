"""
Concepts We Are Practicing:
- Functions
- Loops and Menu-Driven Programs
- Lists and Data Filtering
- Dictionaries
- Counter (from collections)

Modules and Libraries:
- API Requests (requests)
- Text Processing (re - regular expressions)
"""

"""
Author: Your Name
GitHub Link: https://github.com/KedoKedo
Project: Book Analyzer (CS I Project)
Extra credit: I have fixed the bug in line 45-200: I have added so many lines I no longer know what bugs were in the original code and/or created by me, 
    Notable mentions: the fetching of books needed to be changed for the different errors you can get while "connecting" to Gutenberg for easier troubleshooting on the user
              I implemeted a new feature:  if choice == '6', new feature View Library: this allows you to veiw all bokks and associated URLs in current pool
               will be executed
"""

import requests
import re
from collections import Counter


# -----------------------------
# INITIAL DATA
# -----------------------------

my_library = {
    "mobydick": {
        "title": "Moby Dick",
        "url": "https://www.gutenberg.org/files/2701/2701-0.txt"
    }
}


# -----------------------------
# STOP WORDS
# -----------------------------
with open("EN-Stopwords.txt", "r") as f:
    STOP_WORDS = set(line.strip() for line in f)

# -----------------------------
# FETCH BOOK
# -----------------------------
def fetch_book(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.ConnectionError:
        print("Network Error: Gutenberg Down")

    except requests.exceptions.Timeout:
        print("Request timed out")

    except requests.exceptions.InvalidURL:
        print("Invalid URL")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(raw_text):
    text = raw_text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.split()

# -----------------------------
# ANALYZE TEXT
# -----------------------------
def analyze_text(words):
    filtered_words = [
        w for w in words
        if w not in STOP_WORDS and len(w) > 2
    ]

    return Counter(filtered_words).most_common(10)



# -----------------------------
# VISUALIZATION (BAR CHART)
# -----------------------------
def plot_results(stats, title):
    print("\n" + title)
    print("-" * len(title))

    if not stats:
        print("No data to display.")
        return

    max_count = stats[0][1]

    for word, count in stats:
        bar_length = int((count / max_count) * 50)
        bar = "█" * bar_length
        print(f"{word}: {bar} ({count})")

# -----------------------------
# MENU SYSTEM
# -----------------------------
def main():
    while True:
        print("\n--- LIBRARY MANAGER ---")
        print(f"Current Books: {[v['title'] for v in my_library.values()]}")
        print("1. Add New Book")
        print("2. Remove Book")
        print("3. Update Book URL")
        print("4. Analyze a Book")
        print("5. Exit")
        print("6. View Library")

        choice = input("\nSelect (1-6): ")

        #----------------------------------
        # ADD BOOK
        #-------------------------------------

        if choice == '1':
            name = input("Enter Book Title: ").strip()
            url = input("Enter Gutenberg .txt URL: ").strip()

            key = name.lower()

            if not name or not url:
                print("Error: Book title and URL cannot be empty.")
                continue

            if key in my_library:
                print("Error: That book already exists in your library.")
                continue

            my_library[key] = {"title": name, "url": url}
            print(f"'{name}' added.")

        # -------------------------
        # REMOVE BOOK
        # -------------------------

        elif choice == '2':
            key = input("Enter title to remove: ").strip().lower()

            if key in my_library:
                print(f"'{my_library[key]['title']}' removed.")
                del my_library[key]
            else:
                print("Error: Book not found.")

            
            
        # -------------------------
        # UPDATE BOOK
        # -------------------------
        elif choice == '3':
            key = input("Enter the book title to update: ").strip().lower()

            if key in my_library:
                print(f"Current URL: {my_library[key]['url']}")
                new_url = input("Enter new URL: ").strip()

                if new_url:
                    my_library[key]["url"] = new_url
                    print(f"'{my_library[key]['title']}' updated successfully.")
                else:
                    print("Invalid URL. Update cancelled.")
            else:
                print("Book not found.")

        # -------------------------
        # ANALYZE BOOK
        # -------------------------
        elif choice == '4':
            key = input("Which book to analyze? ").strip().lower()

            if key in my_library:
                url = my_library[key]["url"]
                title = my_library[key]["title"]

                print(f"Fetching and analyzing '{title}'...")

                raw_text = fetch_book(url)

                if raw_text:
                    words = clean_text(raw_text)
                    stats = analyze_text(words)
                    plot_results(stats, title)
                else:
                    print("Error: Failed to fetch book.")
            else:
                print("Error: Book not found.")

        # -------------------------
        # EXIT
        # -------------------------
        elif choice == '5':
            print("Goodbye!")
            break

        # -------------------------
        # VIEW LIBRARY
        # -------------------------
        elif choice == '6':
            if not my_library:
                print("Library is empty.")
            else:
                print("\n--- CURRENT LIBRARY ---")
                for data in my_library.values():
                    print(f"{data['title']} -> {data['url']}")


if __name__ == "__main__":
    main()
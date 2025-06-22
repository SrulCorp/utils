from bs4 import BeautifulSoup
import sys

def main():
    print("Paste your HTML snippet (press Ctrl+D to finish on Linux/macOS or Ctrl+Z then Enter on Windows):")

    # Read multiline HTML input from stdin
    html_input = sys.stdin.read()

    # Parse the HTML
    soup = BeautifulSoup(html_input, 'html.parser')

    # Find all <a> tags and extract href attributes
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

    # Output the links array
    print("\nFound links:")
    print(links)

    # Wait for keypress before exiting
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

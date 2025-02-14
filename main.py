from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    elsevier_api_key = os.getenv("ELSEVIER_API_KEY")
    print(elsevier_api_key)

if __name__ == "__main__":
    main()
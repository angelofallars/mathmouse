import os
from dotenv import load_dotenv
from botclass import QuizBot


def main():
    # Get token from .env file in same directory
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    # Run the client
    client = QuizBot()
    client.run(TOKEN)


if __name__ == '__main__':
    main()

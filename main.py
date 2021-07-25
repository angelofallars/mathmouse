import os
from dotenv import load_dotenv
from botclass import MathQuiz


def main():
    # Get token
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    # Run the client
    client = MathQuiz()
    client.run(TOKEN)


if __name__ == '__main__':
    main()

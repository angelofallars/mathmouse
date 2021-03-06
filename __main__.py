"""
The MIT License (MIT)
Copyright (c) 2015-present Rapptz
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import os
from dotenv import load_dotenv
from botclass import QuizBot


def main():
    # Check if running on heroku
    is_prod = os.environ.get('IS_HEROKU')

    # Running on Heroku
    if is_prod:
        TOKEN = os.environ.get('TOKEN')

    # Running on dev
    else:
        # Get token from .env file in same directory
        load_dotenv()
        TOKEN = os.environ.get('TOKEN')

    # Return if no token
    if not TOKEN:
        from sys import exit
        exit(101)


    # Run the client
    client = QuizBot()
    client.run(TOKEN)


if __name__ == '__main__':
    main()

# Testing login to https://www.puzzles-mobile.com/api/login

import os
import requests

from dotenv import load_dotenv

load_dotenv()

# Need to move these to a "secrets" file so they are not committed to the repo.

payload = {
    'email': os.environ['PUZZLE_EMAIL'],
    'password': os.environ['PUZZLE_PASSWORD']
}

LOGIN_URL = 'https://www.puzzles-mobile.com/api/login'
PUZZLE_URL = 'https://www.puzzle-minesweeper.com/minesweeper-5x5-easy/'

with requests.Session() as session:
    login_response = session.post(LOGIN_URL, data=payload)

    print(login_response.cookies['api_token'])
    api_token = login_response.cookies['api_token']
    session.cookies.set('api_token', api_token, domain='www.puzzle-minesweeper.com', path='/')

    puzzle_response = session.get(PUZZLE_URL)
    print(puzzle_response.request.headers.get("Cookie"))
    # if login_response.ok:
    #     dashboard = session.get(protected_url)
    #     print(dashboard.cookies.get_dict())
        
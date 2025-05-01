# bot-detector
This program launches a site that analyzes specified users on the social media platform Reddit, stores their data in a database, and provides a structured analysis of the collected information. The main codebase is written in Python, the backend utilizes Django, and the frontend is built with JavaScript and HTML.
Key metrics analyzed include:
1.  A user’s posts and comments metadata.
2. The user’s trophy count and karma score.
3. The polarity and emotional tone of all posts and comments.
4. The likelihood of a user being a bot, evaluated through multiple behavioral and activity-based factors.
Core components:
reddit_request.py:
Requests user data via Reddit’s API using provided usernames and subreddit associations. The retrieved data is later structured and analyzed.
semantics.py:
Analyzes the emotional tone and sentiment of post and comment text gathered by reddit_request.py.
bot_rank.py:
Estimates the probability (as a percentage) of a user being a bot based on their activity patterns and post history.
utils.py (includes prepare_data_analysis_page()):
Prepares and formats analyzed data for display on the frontend.
Architecture:
1. The user enters a Reddit username into the input field.
2. The input is sent from the frontend to Django’s views.py.
3. The system checks if the user’s data already exists in the database. If found, it retrieves the cached data; otherwise, it fetches fresh data via Reddit’s API.
4. The data is processed through bot probability estimation (bot_rank.py), semantic analysis (semantics.py), and formatting utilities (utils.py), then returned to the frontend.
5. The user is redirected to a results page displaying the analyzed metrics.

To run the project:
1. Clone the repository and install Python dependencies (Django, PRAW, text analysis libraries) via pip install -r requirements.txt.
2. Go into testproject in the console
3. Start the Django server with python manage.py runserver.
4. Navigate to http://127.0.0.1:8000 in your browser, enter a Reddit username in the input field, and submit.
       
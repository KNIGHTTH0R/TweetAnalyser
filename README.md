# TweetAnalyser
Final Year Project in Social Media Analytics and Monitoring.

### Important Note
IMPORTANT NOTE. Live collection of tweets is not possible with the current state of the project, as it would require to leave my
private Twitter keys in the code, which is strongly advised against by Twitter. On requrest I can
demonstate that the functionality is working, or other persons private keys can be used.
To use your own keys, navigate to live-tweets and insert them into twitter_credentials.py file.

### Note
This project was created on Ubuntu.
It would also be easiest to run in on Ubuntu.

## Requirements
- Python 3
- pip (Python package manager)
- venv (Python virtual environment)

## Running the program on Ubuntu
1. Make sure everything listed in requirements is installed.
2. Clone the repository, and navigate to it.
3. Run `python -m venv venv` to create a virtual environment.
4. Run `. venv/bin/activate` to activate the virtual environment.
5. Run `pip install -r requirements.txt` to install dependencies.
6. Run `python main_script.py` to run the main program.

The program will analyse a single set of 300 tweets.
To change the file to be analysed, open main_script.py, and change
the number of the loaded file in the main function. If 'load_tweets_backup' is used for
loading files and it throws an error 'load_tweets' must be used. This is due to some tweet files
using single quotation marks in JSON, where double quotation marks is the standard, I had to adopt
the loading of the file to support that.

For any questions, feel free to contact me.

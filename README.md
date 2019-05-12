# TweetAnalyser
Final Year Project in Social Media Analytics and Monitoring.

## Abstract
Looking for a Needle in a Haystack.

Information Extraction related to Twitter posts can greatly benefit the society in cases of crisis situations, potentially providing detailed live information about any given event. However, many obstacles must be overcome to get to that stage, as when working with such tasks we are dealing with highly unstructured information in form of natural language which has sentiment attached to it, and communication style adopted to Social Media is often used. Furthermore, it turns out that vast majority of incoming information is irrelevant (spam, ads, words used in wrong context). We will be looking at how all the listed challenges can be overcome using Artificial Intelligence, by creating a system for filtering and extracting information. The system will be tested on a collection of winter data, with analysis of results and discussion of further work. While testing the system on such data set, I would like to note that it is designed in such a way so that with least amount of effort it can be adopted to work with any data sets.

### Important Note
Live collection of tweets is not possible with the current state of the project, as it would require me to leave my
private Twitter keys in the code, which is strongly advised against by Twitter. On requrest I can
demonstate that the functionality is working, or other persons private keys can be used.
To use your own keys, navigate to live-tweets and insert them into `twitter_credentials.py` file.

### Note
As this is an interesting and important project for me, in future I will either rewrite it with better architecture and experiment with other ways of getting similar of better results, or clean up this existing version.

## Getting Started
This project was created on Linux OS, it would also be easiest to run it in the same environment.

### Prerequsities
- `Python 3`
- `pip` (Python package manager)
- `venv` (Python virtual environment)
- Twitter Developer keys are needed if tweet collection functionality is to be used, they can be obtained by registering on https://developer.twitter.com/ and creating an app.

### Installation
1. Make sure everything listed in requirements is installed.
2. Clone the repository using `git clone`, and navigate to it.

### Running the program on Ubuntu
1. Run `python -m venv venv` to create a virtual environment.
2. Run `. venv/bin/activate` to activate the virtual environment.
3. Run `pip install -r requirements.txt` to install dependencies.
4. Run `python main_script.py` to run the main program.

By default the program will analyse a single set of 300 tweets.
To change the file to be analysed, open `main_script.py`, and change
the number of the loaded file in the main function. If `load_tweets_backup` is used for
loading files and it throws an error `load_tweets` must be used. <br />
This is due to some tweet files
using single quotation marks in JSON, where double quotation marks is the standard, I had to adopt
the loading of the file to support that.

### Contact me
For any questions, feel free to contact me.

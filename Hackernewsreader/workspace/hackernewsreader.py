from flask import Flask
from flask_ask import Ask, statement, question, session
from hackernews import HackerNews
import requests
import time
import unidecode
import os

app = Flask(__name__)
ask = Ask(app, "/hackernews_reader")
hn = HackerNews()

def get_posts():
    top_story_ids = hn.top_stories(limit=10)
    for story in top_story_ids:
        stories = hn.get_item(story)
    return stories
    #top_iter = hn.get_top_stories(limit=10) # get top 10 stories
    #top_iter = '... '.join([i for i in top_iter])
    #return top_iter
    
@app.route('/')
def homepage():
    return "Ay this ish working"
    
@ask.launch
def start_skill():
    welcome_message = 'Hi there, would you like to hear the top ten news stories from Hacker News?'
    return question(welcome_message)
    
@ask.intent("YesIntent")
def share_posts():
    posts = get_posts()
    posts_msg = 'The current world news headlines are {}'.format(posts)
    return statement(posts_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Well why did you call me then ... Bye'
    return statement(bye_text)


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
    app.run()
    app.run(debug=True)
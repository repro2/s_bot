import praw
import pdb
import re
import os


source_dir = r""
post_file_path = os.path.join(source_dir, "posts_replied_to.txt")
comment_file_path = os.path.join(source_dir, "comments_replied_to.txt")

if not os.path.isfile(post_file_path):
    posts_replied_to = []
else:
    with open(post_file_path, "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile(comment_file_path):
    comments_replied_to = []
else:
    with open(comment_file_path, "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

def redditConnect():
    reddit = praw.Reddit(
        client_id = "",
        client_secret = "",
        user_agent = "Analysis_Sbot 0.1",
        username = "analysis_sbot",
        password = "",
    )

    print(reddit.read_only)
    return reddit

def replyToSubmission(submission, posts_replied_to):
    if submission.id not in posts_replied_to:
        if re.search("Hello!", submission.title, re.IGNORECASE):
            submission.reply("Hi!")
            print("Bot replying to: ", submission.title)
            posts_replied_to.append(submission.id)

def replyToComment(comment, comments_replied_to):
    if comment.id not in comments_replied_to:
        if re.search("Hi!", comment.body, re.IGNORECASE):
            comment.reply("Hello!")
            print("Bot replying to comment: ", comment.id)
            comments_replied_to.append(comment.id)

def printCommentsFromSubmission(submission, comments_replied_to):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        print("Comment ID: ", comment.id)
        print("Comment Body: ", comment.body)
        print("---------------------------------\n")
        
        replyToComment(comment, comments_replied_to)

    with open(comment_file_path, "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

def printPostFromSubreddit(redditCon, subreddit):
    for submission in redditCon.subreddit(subreddit).hot(limit=10):
        print("Title: ", submission.title)
        print("Text: ", submission.selftext)
        print("Score: ", submission.score)
        print("---------------------------------\n")

        replyToSubmission(submission, posts_replied_to)
        printCommentsFromSubmission(submission, comments_replied_to)
        
    with open(post_file_path, "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
    
    with open(comment_file_path, "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

def postToReddit(redditCon, subreddit, title, url):
    redditCon.validate_on_submit = 1
    subreddit = redditCon.subreddit(subreddit)
    subreddit.submit(title, url = url)
    print("Post Submitted")

if __name__ == '__main__':
    # redditConnect()
    printPostFromSubreddit(redditConnect(), 'Analysis_SentimentBot')






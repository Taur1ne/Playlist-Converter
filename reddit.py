import praw
from config import Config


def main():
    c = Config()
    reddit = praw.Reddit(
            user_agent='Playlist Converter (by /u/PlaylistConverter)',
            client_id=c.reddit_client_id,
            client_secret=c.reddit_secret,
            username=c.reddit_username,
            password=c.reddit_password)
    
    subreddit = reddit.subreddit('AskReddit')
    for item in reddit.inbox.all(limit=None):
        print(repr(item))


if __name__ == '__main__':
    main()
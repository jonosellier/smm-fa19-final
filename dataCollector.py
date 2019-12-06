from textblob import TextBlob
import praw
import datetime
import sys

dt = datetime.datetime.today()

reddit = praw.Reddit(client_id='CLIENT ID HERE', client_secret='SECRET HERE', password='', user_agent='USERAGENT', username='')

def get_avg_post_sentiment_dfs(parent_comment, net_sentiment, total_comments):
    #print(net_sentiment,total_comments)
    if len(parent_comment.replies) < 1:
        return [net_sentiment, total_comments]
    for comment in parent_comment.replies:
        if hasattr(comment.author, "name") and hasattr(parent_comment.author, "name"):
            tb = TextBlob(comment.body)
            sent = tb.sentiment.polarity
            net_sentiment+=sent
            total_comments+=1
            res = get_avg_post_sentiment_dfs(comment, net_sentiment, total_comments)
            net_sentiment = res[0]
            total_comments = res[1]
    return [net_sentiment, total_comments]

def get_avg_sentiment(post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None) #gets rid of "show more comments" links
    net = 0
    count = 0
    for top_level_comment in submission.comments:
        resp = get_avg_post_sentiment_dfs(top_level_comment, 0, 0)
        net += resp[0]
        count += resp[1]
    if count > 0:
        return net/count
    else:
        return 0

def get_fp_post_sentiments():
    post_dict = dict()
    i = 1
    toolbar_width = 40
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))
    f = open("collected_data_raw.csv", 'a')
    for submission in reddit.subreddit('all').top('day', limit=1000):
        if i%(1000/toolbar_width) == 0:
            sys.stdout.write("-")
            sys.stdout.flush()
        res = get_avg_sentiment(submission.id)
        if submission.subreddit.display_name not in post_dict:
            post_dict[submission.subreddit.display_name] = {"net_sentiment": res, "post_count":1}
        else:
            post_dict[submission.subreddit.display_name]["net_sentiment"]+=res
            post_dict[submission.subreddit.display_name]["post_count"]+=1 #second+ time we saw this subreddit
        i+=1
        if submission.over_18:
            f.write(submission.id+","+str(res)+","+submission.subreddit.display_name+",FALSE\n")
        else:
            f.write(submission.id+","+str(res)+","+submission.subreddit.display_name+",TRUE\n")
    sys.stdout.write("\n")
    f.close()
    return post_dict

def dict_to_csv(d, collection_id):
    f = open("collected_data.csv", 'a')
    for sub in d.keys():
        f.write(str(collection_id)+","+sub+","+str(d[sub]["net_sentiment"])+","+str(d[sub]["post_count"])+"\n")
    f.close()
    return

def combine_results():
    f = open("collected_data.csv")
    g = open("combined_data.csv", 'w')
    g.write("subreddit,net_sentiment,post_count\n")
    next(f)
    lines = f.readlines()
    d = dict()
    for line in lines:
        contents = line.split(",")
        if contents[1] not in d:
            d[contents[1]]={"net_sent": float(contents[2]), "count": int(contents[3])}
        else:
            d[contents[1]]["net_sent"]+=float(contents[2])
            d[contents[1]]["count"]+=float(contents[3])
    for sub in d.keys():
        g.write(sub+","+str(d[sub]["net_sent"])+","+str(d[sub]["count"])+"\n")

d = dict()
print("Starting code run")
d = get_fp_post_sentiments()
print("Done\n\nWriting to file...")
dict_to_csv(d, dt.day)
print("Done\n\nCombining results by subreddit...")
combine_results()
print("Done\n")

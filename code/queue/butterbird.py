import twitter
import time
import sys

consumer_key=""
consumer_sec=""
access_key=""
access_sec=""

api = twitter.Api(
        consumer_secret=consumer_sec,
        consumer_key=consumer_key,
        access_token_key=access_key,
        access_token_secret=access_sec)

api.VerifyCredentials()

last_id = int(sys.argv[1])
check_interval = int(sys.argv[2])

while True:
    # Make sure it's between 8 am and 10 pm.
    cur_hour = time.localtime().tm_hour
    if not (cur_hour >= 8 and cur_hour <= 22):
        print "It's too late to tweet!"
        time.sleep(60*30)
        continue
    # Sleep if we're near our rate limit.
    if api.GetRateLimitStatus()["remaining_hits"] < 10:
        print "Rate limiting..."
        time.sleep(600)
        continue
    # Check the buffer stream for new tweets, and post the oldest new tweet.
    print "Checking..."
    untweeted = api.GetUserTimeline(screen_name="beala_queue", since_id=last_id)
    if len(untweeted) > 0:
        to_post = untweeted[-1]
        api.PostUpdate(to_post.text)
        last_id = to_post.id
        print "New tweet: " + to_post.text
        print "id: " + str(last_id)
        # Save last tweet id to file in case the script gets killed.
        with open(".last_tweet_id", 'w') as id_file:
            id_file.write(str(last_id))
    # Sleep between checks/posts.
    time.sleep(check_interval)

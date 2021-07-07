from pdf2image import convert_from_path
import tweepy
def main(startDate):
	pages = convert_from_path('/_betList/BetList_' + str(startDate) + '.pdf', 500)
	i = 0
	for page in pages:
		name = "images/" + startDate + "_" + str(i) + ".jpg"
		page.save(name, 'JPEG')
		i += 1	
	twitter_auth_keys = { 
        "consumer_key"        : "d5pEaeD9g6BRTg4YgrBBXE01T",
        "consumer_secret"     : "6TgcN2g76wMKFUiwJ0DqIGkIyLE4Q3HPi444V6WKMXy9Q0WCQ3",
        "access_token"        : "1298604826662703110-lttUgVWlr11rjLjjgmnp25kObYxOQ3",
        "access_token_secret" : "rDamrR4pqRZEOVAxr7KAUCq0Rh2HbMoJVPWiWfjEenYOf"
    }	
	
	auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
	auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
	api = tweepy.API(auth)
	
	#Upload Images
	images = []
	image_id = []
	for x in range(i):
		media = api.media_upload("images/" + startDate + "_" + str(x) + ".jpg")
		images.append(media)
		image_id.append(media.media_id)
	
	#Add Text
	tweet = startDate + " BetList"
	post_result = api.update_status(status=tweet, media_ids=image_id)
	
	
	
if __name__ == "__main__":
	main()
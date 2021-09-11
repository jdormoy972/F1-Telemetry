import tweepy
import os
import re

API_KEY = ''
API_SECCRET_KEY = ''
BearerTOKEN = ''
Access_Token = ''
Access_Token_Secret = ''


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(API_KEY, API_SECCRET_KEY)
auth.set_access_token(Access_Token, Access_Token_Secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Creates the user object. The me() method returns the user whose authentication keys were used.
user = api.me()
 
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))
 
# Sample method, used to update a status
# api.update_status('Hello Form RBI Lab!')

# load image
directory = 'Plot_Out/Quali/'
for filename in os.listdir(directory):
	if filename.endswith(".png"):
		img = re.sub('.png',"!", filename)
		status = "Check out the speed telemetry of %s \n\n#HungarianGP #F1 #Formula1"%img

		print(status)

		# Send the tweet.
		api.update_with_media(directory+filename, status)

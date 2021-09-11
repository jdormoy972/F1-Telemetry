import tweepy
import os
import re

API_KEY = 'BGXSbJ63ExpvFAzrFirMddeO2'
API_SECCRET_KEY = '0ID07kP4R00RVafg154WVKK7FfroS6r5Q78PqSAnPYD40Kec1G'
BearerTOKEN = 'AAAAAAAAAAAAAAAAAAAAAEDxSAEAAAAAkj2k94SlRd38%2BJQxs8QTwtGcyLk%3DEZ9En9QB04OP8po8DL569ygSMlbk3FcQpRt0F1KXZSXrVGCMdr'
Access_Token = '1416046508630319104-RaXStfTVft09emeMc6EdQcmaIJpgvW'
Access_Token_Secret = '6qCc1Cr4AzABi4Xg8mrt752lr0a2istFWtNecCBNPhGA6'


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
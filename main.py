# ---------------------INSTA BOT------------------------

import requests #to use requests (get,post,update,delete)
import urllib   #to download a particular post
from textblob import TextBlob  #to delete negative comments using m/c learning
from textblob.sentiments import NaiveBayesAnalyzer

Base_URL = "https://api.instagram.com/v1/"
Access_token = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494" #access token of own user

# --------------FUNCTION TO DISPLAY OWN DETAILS--------------------

def self_info():

    request_url = (Base_URL + 'users/self/?access_token=%s') %(Access_token)
    print 'GET request URL : %s' %request_url
    user_info = requests.get(request_url).json()  #get request sent to instagram will get a response which is by json converted into python dictionary and stored in user_info

    if user_info['meta']['code'] == 200:    #200 is one of the status code 200 means the request is successfully made and response also successful

        if 'data' in user_info:

            user_name = user_info["data"]["username"]
            name = user_info["data"]["full_name"].capitalize()
            posts = user_info["data"]["counts"]["media"]
            following = user_info["data"]["counts"]["follows"]
            followers = user_info["data"]["counts"]["followed_by"]

            print "\n1.USER NAME:%s\n2.FULL NAME:%s\n3.NO. OF POSTS:%d\n4.FOLLOWING:%d\n5.FOLLOWERS:%d" %(user_name,name,posts,following,followers)  #from that user_info we are printing details if status code is 200

        else:

            print "User not Exist!"

    else:

        print "Response unsucessfull!"

# -------------------FUNCTION TO GET USER ID-----------------------------

def get_user_id(insta_username):

    request_url = (Base_URL + 'users/search?q=%s&access_token=%s') % (insta_username, Access_token) #by using users/search API this function will search for the particular user name
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'

# --------------------FUNCTION TO PRINT USER DETAILS-------------------------

def get_user_info(insta_username):

    user_id = get_user_id(insta_username) #from that user id we'll fetch data of that ID

    if user_id == None:
        print 'User does not exist!'

    request_url = (Base_URL + 'users/%s?access_token=%s') % (user_id, Access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()        #That searched user info stored in user_info

    if user_info['meta']['code'] == 200:
        if 'data' in user_info:
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'

    else:
        print 'Status code other than 200 received!'

# -----------------FUNCTION TO DOWNLOAD RECENT POST OF USER--------------------

def get_user_post(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'

    request_url = (Base_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, Access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name) #to download that image we use urllib
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'

    else:
        print 'Status code other than 200 received!'

# --------------FUNCTION TO DOWNLOAD RECENT POST OF OWN USER------------------

def get_own_post():

  request_url = (Base_URL + 'users/self/media/recent/?access_token=%s') % (Access_token)
  print 'GET request url : %s' % (request_url)
  own_media = requests.get(request_url).json()

  if own_media['meta']['code'] == 200:
      if len(own_media['data']) > 0:
          image_name = own_media['data'][0]['id'] + '.jpeg'
          image_url = own_media['data'][0]['images']['standard_resolution']['url']
          urllib.urlretrieve(image_url, image_name)
          print 'Your image has been downloaded!'
      else:
          print 'Post does not exist!'

  else:
     print 'Status code other than 200 received!'


# ---------------------FUNCTION TO GET POST ID--------------

def get_post_id(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'

    request_url = (Base_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, Access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            return user_media['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
        return None

# ---------------------FUNCTION TO LIKE A POST-----------------------

def like_a_post(insta_username):

    media_id = get_post_id(insta_username)
    request_url = (Base_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": Access_token}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json() #post method send reques to like the post

    if post_a_like['meta']['code'] == 200: #if meta code is 200 that like is successfull
		print 'Like was successful!'
    else:
        print "Unsuccesful like"

# --------------FUNCTION TO POST A COMMENT---------------------------

def post_a_comment(insta_username):

    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": Access_token, "text" : comment_text}
    request_url = (Base_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()  #same function as like

    if make_comment['meta']['code'] == 200:
        print 'comment was successful!'
    else:
        print 'Your comment was unsuccessful. Try again!'

#  -----------FUNCTION TO DELETE NEGATIVE COMMENT----------------------

def delete_negative_comment(insta_username):

	media_id = get_post_id(insta_username)
	request_url = (Base_URL + 'media/%s/comments/?access_token=%s') % (media_id, Access_token)
	print 'GET request url : %s' % (request_url)
	comment_info = requests.get(request_url).json()

	if comment_info['meta']['code'] == 200:
		if len(comment_info['data']) > 0:
			for comment in comment_info['data']:
				comment_text = comment['text']
				blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())  #it will analyse the comment and separate negative and positive words

				if blob.sentiment.p_neg > blob.sentiment.p_pos: #if negative percentage is more that particular comment will be deleted
					comment_id = comment['id']
					delete_url = (Base_URL + 'media/%s/comments/%s/?access_token=%s') % (
						media_id, comment_id, Access_token)
					print 'DELETE request url : %s' % (delete_url)

					delete_info = requests.delete(delete_url).json()

					if delete_info['meta']['code'] == 200:
						print 'Comment successfully deleted!'
					else:
						print 'Could not delete the comment'

		else:
			print 'No comments found'
	else:
		print 'Status code other than 200 received!'

# ------------MAIN FUNCTION----------------

def start_bot():
    while True:

        print '\n'
        print '***** Welcome to instaBot! ******\n'
        print '\t\t***MENU***'
        print "1.Get your own details."
        print "2.Get details of a user by username."
        print "3.Get your own recent post."
        print "4.Get the recent post of a user by username."
        print "5.Like recent post of a user."
        print "6.Post a comment."
        print "7.Delete negative comment for a user."
        print "8.Exit"
        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()
        elif choice == "2":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "5":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "6":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "7":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "8":
            exit()
        else:
            print "Wrong Choice!"


start_bot()
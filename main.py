import requests
import urllib

Base_URL = "https://api.instagram.com/v1/"
Access_token = "4870715640.a48e759.874aba351e5147eca8a9d36b9688f494"

def self_info():
    request_url = (Base_URL + 'users/self/?access_token=%s') %(Access_token)
    print 'GET request URL : %s' %request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if 'data' in user_info:

            user_name = user_info["data"]["username"]
            name = user_info["data"]["full_name"].capitalize()
            posts = user_info["data"]["counts"]["media"]
            following = user_info["data"]["counts"]["follows"]
            followers = user_info["data"]["counts"]["followed_by"]

            print "\n1.USER NAME:%s\n2.FULL NAME:%s\n3.NO. OF POSTS:%d\n4.FOLLOWING:%d\n5.FOLLOWERS:%d" %(user_name,name,posts,following,followers)

        else:

            print "User not Exist!"

    else:

        print "Response unsucessfull!"

def get_user_id(insta_username):

    request_url = (Base_URL + 'users/search?q=%s&access_token=%s') % (insta_username, Access_token)

    print 'GET request url : %s' % (request_url)

    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


def get_user_info(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (Base_URL + 'users/%s?access_token=%s') % (user_id, Access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

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

def get_user_post(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (Base_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, Access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

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
        elif choice == "8":
            exit()
        else:
            print "Wrong Choice!"


start_bot()
import requests

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


def get_own_post():

    request_url = (Base_URL + 'users/self/media/recent/?access_token=%s') %Access_token
    print 'GET request URL : %s' %(request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:

        if len(own_media['data']) > 0 :
            return own_media['data'][0]['id']
        else:
            print 'Post not Exist'

    else:
        print 'Status codeother than 200 recieved!'


self_info()
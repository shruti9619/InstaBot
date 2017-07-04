import requests
import urllib
import csv
from tagdataplot import plotter

# my key
APP_ACCESS_TOKEN = "5683010082.f0c5981.7724a99b4e794e4a8d4976af727fe38d"
BASE_URL = "https://api.instagram.com/v1/"
MENU_LIST = ["Fetch personal information.","Fetch info of a user.", "Fetch your most recent post",
             "Fetch most recent posts of a user", "Fetch my most recent posts liked", "Like most recent post of a user",
             "Fetch list of comments on a user's recent post", "Post comment on a user's post" , "Fetch number of posts on a hashtag",
             "Quit"]


# method to download files
def download_method(r):
    if r['meta']['code'] == 200:
        if len(r['data']):
            for i in range(0,len(r['data'])):
                name = r['data'][i]['id'] + '.png'
                print 'ID: '+ name
                url = ['data'][i]['images']['standard_resolution']['url']
                print 'Image Details: ' + url
                urllib.urlretrieve(url, 'images/' + name)
                print '\n'
        else:
            print '\n No data or media found!'
    else:
        print "Response couldn't be fetched!"


# method to access self info
def fetch_self_info():
    req_url = BASE_URL+'users/self/?access_token=%s' % APP_ACCESS_TOKEN
    try:
        r = requests.get(req_url).json()
        if r['meta']['code'] == 200:
            if len(r['data']):
                print 'Username: %s' % (r['data']['username'])
                print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
                print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
                print 'No. of posts: %s' % (r['data']['counts']['media'])
            else:
                print 'There is no data for this user!'
    except:
        print "Url request exception occurred!"


# method to fetch username from the api
def fetch_uid(username):
    uid = None
    req_url = BASE_URL + 'users/search?q=%s&access_token=%s' % (username,APP_ACCESS_TOKEN)
    try:
        user_info=requests.get(req_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                return user_info['data'][0]['id']
        else:
            print "Status code not 200!"
    except:
        print "Url request exception occurred!"
    return uid


# method to fetch user details using the uid
def fetch_other_user(uid):
    # print uid for easiness's sake
    print uid
    if uid is None:
        print 'Username could not be fetched! \n\n'
    else:
        req_url=BASE_URL+'users/%s?access_token=%s' % (uid, APP_ACCESS_TOKEN)
        try:
            r=requests.get(req_url).json()
            if r['meta']['code'] == 200:
                if len(r['data']):
                    print 'Username: %s' % (r['data']['username'])
                    print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
                    print 'No. of people he/she is following: %s' % (r['data']['counts']['follows'])
                    print 'No. of posts: %s' % (r['data']['counts']['media'])
                else:
                    print 'There is no data for this user!'
            else:
                print 'Status code other than 200 received!'
        except:
            print "exception occurred!"


# method to fetch self posts
def fetch_self_posts(num_posts):
    req_url = BASE_URL+"users/self/media/recent/?access_token=%s&count=%s" % (APP_ACCESS_TOKEN, str(num_posts))
    r = requests.get(req_url).json()
    download_method(r)


# method to fetch others posts
def fetch_other_posts(user_name, num_posts):
    uid = fetch_uid(user_name)
    if uid is not None:
        req_url = BASE_URL + "users/%s/media/recent/?access_token=%s&count=%s" % (uid, APP_ACCESS_TOKEN, str(num_posts))

        user_media = requests.get(req_url).json()
        download_method(user_media)
    else:
        print "User doesn't exist!"

# method to fetch most recent post liked by self
def fetch_most_recent_liked_self(num_posts):
    req_url = BASE_URL + "users/self/media/liked?access_token=%s&count=%s" % (APP_ACCESS_TOKEN, str(num_posts))

    r = requests.get(req_url).json()
    download_method(r)


def fetch_most_recent_media_id(uid):
    req_url = BASE_URL + "users/%s/media/recent/?access_token=%s&count=3" % (uid, APP_ACCESS_TOKEN)

    user_media = requests.get(req_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print "Failed to fetch post!"
    else:
         print "Failed to fetch post!"
    return None


# method to like the most recent post of a user
def like_user_post(user_name):
    uid=fetch_uid(user_name)
    if uid is None:
        print "User doesn't exist!"
        return
    else:
        media_id=fetch_most_recent_media_id(uid)

        if media_id is not None:
            req_url=BASE_URL + "media/%s/likes" % str(media_id)
            token_payload = {"access_token": APP_ACCESS_TOKEN}
            r=requests.post(req_url, token_payload).json()

            if r['meta']['code'] != 200:
                print "Failed to like the post! 11"
            else:
                print "Keep liking more!"
        else:
            print "Failed to like the post!22"
    return


# method to fetch comments on the latest post of a user by username
def fetch_user_recent_post_comments(user_name):
    uid = fetch_uid(user_name)
    if uid is not None:
        media_id = fetch_most_recent_media_id(uid)
        if media_id is not None:
            req_url = BASE_URL + "media/%s/comments?access_token=%s" % (str(media_id), APP_ACCESS_TOKEN)
            r=requests.get(req_url).json()
            if r['meta']['code'] == 200:
                if len(r['data']):
                    print "The comments are :- \n"
                    for i in range(0,len(r['data'])):
                        print r['data'][i]['from']['full_name'] + ": " + r['data'][i]['text']
                else:
                    print "No comments yet! Be the first one to comment!"
            else:
                print "Data inaccessible!"
        else:
            print "Posts not found!"
    else:
        print "User doesn't exist!"


# method to add to comment in the most recent user post
def post_comment_most_recent(user_name):
    uid = fetch_uid(user_name)

    if uid is not None:
        media_id = fetch_most_recent_media_id(uid)

        if media_id is not None:
            req_url = BASE_URL + "media/%s/comments" % media_id
            print "Please not that the comment should not exceed 300 characters, should not be in ALL capitals, " \
                  "should not contain more than 4 hashtags and one URL link."
            comment_msg = raw_input("Your comment: ")
            comment_payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_msg}
            r = requests.post(req_url,comment_payload).json()

            if r['meta']['code'] == 200:
                print "Comment posted successfully!"
            else:
                print "Failed to post comment. Try again!"

        else:
            print "Posts not found!"
    else:
        print "User doesn't exist!"


#  method to collect tag data from images and plot
def tag_collect(tag_name):
    req_url=BASE_URL+'tags/%s?access_token=%s'% (tag_name,APP_ACCESS_TOKEN)
    r = requests.get(req_url).json()
    if r['meta']['code'] == 200:
        if len(r['data']):
            print 'Number of images with the tag %s: %d ' % (tag_name, r['data']['media_count'])
            f = open("collection.csv",'ab')
            writer = csv.writer(f)
            writer.writerow([tag_name, r['data']['media_count']])
            f.close()

# method to show menu and take input
def show_menu():

    print "Welcome to InstaBot! \n What are you upto today? Let's pick from the menu"

    while True:

        for i in range(0,len(MENU_LIST)):
            print '%d. %s' % (i+1, MENU_LIST[i])

        try:
            menu_choice = int(raw_input())
        except:
            print 'Something went wrong with your answer! \n Try again! '
        if menu_choice == 1:
            fetch_self_info()

        elif menu_choice == 2:
            u_name = raw_input("Enter the username to fetch details ")
            fetch_other_user(fetch_uid(u_name))

        elif menu_choice == 3:
            num_of_posts = raw_input("Enter the number of posts that you would like to fetch ")
            fetch_self_posts(num_of_posts)

        elif menu_choice == 4:
            user_name = raw_input("Enter the name of user that you would like to fetch ")
            num_of_posts = raw_input("Enter the number of posts that you would like to fetch ")
            fetch_other_posts(user_name, num_of_posts)

        elif menu_choice == 5:
            num_of_posts = raw_input("Enter the number of posts that you would like to fetch ")
            fetch_most_recent_liked_self(num_of_posts)

        elif menu_choice == 6:
            user_name = raw_input("Enter the name of user ")
            like_user_post(user_name)

        elif menu_choice == 7:
            user_name = raw_input("Enter the name of user ")
            fetch_user_recent_post_comments(user_name)

        elif menu_choice == 8:
            user_name = raw_input("Enter the name of user ")
            post_comment_most_recent(user_name)

        elif menu_choice == 9:
            tag_name = raw_input("Enter a tag to search ")
            tag_collect(tag_name)

        else:
            print 'Quitting...'
            exit(0)
        print '\n\n'


show_menu()



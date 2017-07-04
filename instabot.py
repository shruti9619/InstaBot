import requests

#my key
APP_ACCESS_TOKEN = "5683010082.f0c5981.7724a99b4e794e4a8d4976af727fe38d"
BASE_URL = "https://api.instagram.com/v1/"
MENU_LIST = ["Fetch personal information.","Fetch info of a user.", "Quit"]


# method to access self info
def fetch_self_info():
    req_url = BASE_URL+'users/self/?access_token=%s' % APP_ACCESS_TOKEN
    try:
        r = requests.get(req_url)
        print r.json()
    except:
        print "Url request exception occurred!"


# method to fetch username from the api
def fetch_uid(username):
    uid = 0
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
    if uid == 0:
        print 'Username could not be fetched!'
    req_url=BASE_URL+'users/%s?access_token=%s' % (uid, APP_ACCESS_TOKEN)
    try:
        r=requests.get(req_url).json()
        if r['meta']['code'] == 200:
            if len(r['data']):
                print 'Username: %s' % (r['data']['username'])
                print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
                print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
                print 'No. of posts: %s' % (r['data']['counts']['media'])
            else:
                print 'There is no data for this user!'
        else:
            print 'Status code other than 200 received!'
    except:
        print "exception occurred!"


# method to show menu and take input
def show_menu():

    print "Welcome to InstaBot! \n What are you upto today? Let's pick from the menu"
    while True:

        for i in range(0,len(MENU_LIST)):
            print '%d. %s' % (i+1, MENU_LIST[i])

        menu_choice = int(raw_input())
        if menu_choice == 1:
            fetch_self_info()
        if menu_choice == 2:
            u_name = raw_input("Enter the username to fetch details.")
            fetch_other_user(fetch_uid(u_name))
        else:
            exit(0)


show_menu()

import requests

APP_ACCESS_TOKEN="5683010082.f0c5981.7724a99b4e794e4a8d4976af727fe38d" #my key
BASE_URL="https://api.instagram.com/v1/"


def self_info():
    req_url=BASE_URL+'users/self/?access_token=%s'%(APP_ACCESS_TOKEN)
    r=requests.get(req_url)
    print r.json()



self_info()

def fetch_uid(username):
    uid=1
    req_url = BASE_URL + 'users/search?q=%s&access_token=%s' % (username,APP_ACCESS_TOKEN)
    user_info=requests.get(req_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
    else:
        print "Status code not 200!"
    return uid

def other_user(uid):
    print uid
    req_url=BASE_URL+'users/%s?access_token=%s'%(uid,APP_ACCESS_TOKEN)
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


#no sandbox invites successful yet hence my own name for the search
other_user(fetch_uid("shrutiiyyer"))
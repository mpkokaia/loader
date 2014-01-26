from urllib import urlopen
import json
def users_get(usr_id):
    access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url="https://api.vk.com/method/users.get?v=5.5&user_ids="
    fields="&fields=sex,bdate,city,country,photo_200_orig,online,online_mobile,lists,domain,has_mobile,contacts,connections,site,education,universities,schools,can_post,can_see_all_posts,can_see_audio,can_write_private_message,status,last_seen,relation,relatives,counters"
    data = urlopen(url+str(usr_id)+fields+access_token)
    obj=json.load(data)
    if obj['response'][0]['first_name']==u'DELETED':
        return False
    return obj['response'][0]   

def users_getSubscriptions(usr_id):
    access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url="https://api.vk.com/method/users.getSubscriptions?user_id="
    fields="&extended=1&count=100&v=5.7&fields=city,country,place,description,members_count,counters,start_date,end_date,can_post,can_see_all_posts,activity,status,contacts,links,fixed_post,verified,site,can_create_topic"
    data = urlopen(url+str(usr_id)+fields+access_token)
    obj=json.load(data)     
    if obj['response']['count']==0:
        return False
    return obj['response']   

def wall_get(usr_id):
    access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url="https://api.vk.com/method/wall.get?owner_id="
    fields="&count=100"
    data = urlopen(url+str(usr_id)+fields+access_token)
    obj=json.load(data)      
    if 'error' in obj:
        return False
    return obj['response']

def groups_get(usr_id):
    access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url="https://api.vk.com/method/groups.get?user_id="
    fields="&v=5.7&fields=city,country,place,description,wiki_page,members_count,counters,start_date,end_date,can_post,can_see_all_posts,activity,status,contacts,links,fixed_post,verified,site,can_create_topic&extended=1"
    data = urlopen(url+str(usr_id)+fields+access_token)
    obj=json.load(data)   
    if u'error' in obj:
        return False   
    return obj['response']

def friends_get(usr_id):
    access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url="https://api.vk.com/method/friends.get?user_id="
    fields="&fields=nickname,domain,sex,bdate,city,country,timezone,has_mobile,contacts,education,online,relation,last_seen,status,can_write_private_message,can_see_all_posts,can_post,universities"
    data = urlopen(url+str(usr_id)+fields+access_token)
    obj=json.load(data) 
    if u'error' in obj:
        return False 
    return obj['response']

def photos_getAlbums(usr_id):
    access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url="https://api.vk.com/method/photos.getAlbums?user_id="
    data = urlopen(url+str(usr_id)+access_token)
    obj=json.load(data) 
    return obj

def create_record(db,usr_id):
    record={}
    record['vkid']=usr_id
    record['users_get']=users_get(usr_id)
    record['users_getSubscriptions']=users_getSubscriptions(usr_id)    
    record['wall_get']=wall_get(usr_id)
    record['groups_get']=groups_get(usr_id)
    record['friends_get']=friends_get(usr_id)
    record['photos_getAlbums']=photos_getAlbums(usr_id)
    db.users.save(record)   
 
offset=0
access_token="&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
url="https://api.vk.com/method/users.search?v=5.5&university=477&fields=nickname,screen_name,sex,bdate,city,country,timezone,has_mobile,contacts,education,relation,last_seen,status,can_write_private_message,can_see_all_posts,can_post,universities&offset="
from pymongo import Connection
connection = Connection()
db = connection.masht

for i in range(0,100,20):
    data = urlopen(url+str(offset)+access_token)
    obj=json.load(data)
    for i in range(20):
        usr_id=obj['response']['items'][i]['id']
        create_record(db,usr_id)
    offset+=i



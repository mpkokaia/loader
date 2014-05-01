from urllib import urlopen
import json


def users_get(usr_id):
    access_token = "&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url = "https://api.vk.com/method/users.get?v=5.5&user_ids="
    fields = "&fields=sex,education,universities,schools,personal,connections,interests"
    data = urlopen(url + str(usr_id) + fields + access_token)
    obj = json.load(data)
    if obj['response'][0]['first_name'] == u'DELETED':
        return False
    return obj['response'][0]


def friends_get(usr_id):
    access_token = "&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
    url = "https://api.vk.com/method/friends.get?user_id="
    fields = "&fields=nickname,education,universities"
    data = urlopen(url + str(usr_id) + fields + access_token)
    obj = json.load(data)
    if u'error' in obj:
        return False
    return obj['response']


def create_record(db, usr_id):
    record = {}
    try:
        record['vkid'] = usr_id
        user = users_get(usr_id)
        if user == False:
            return True
        record['users_get'] = user
        record['friends_get'] = friends_get(usr_id)
    except IOError:
        import sys

        sys.exit()
    db.students.save(record)
    return True


access_token = "&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
url = "https://api.vk.com/method/users.search?v=5.5&university=477&offset="
from pymongo import Connection

connection = Connection()
db = connection.urfu

access_token = "&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
url = "https://api.vk.com/method/users.search?v=5.5&university=477"
foffset = "&offset="
university_year = "&university_year="
fsex = "&sex="
year = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
sex = [1, 2]
offset = 0
for s in sex:
    for y in year:
        offset = 0
        for i in range(0, 1000, 20):
            try:
                data = urlopen(url + university_year + str(y) + fsex + str(s) + foffset + str(offset) + access_token)
            except IOError:
                import sys

                sys.exit()
            obj = json.load(data)
            for item in obj['response']['items']:
                usr_id = item['id']
                create_record(db, usr_id)
            offset = i

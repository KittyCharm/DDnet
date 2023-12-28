import requests
#import json

#获取玩家id，返回玩家数据
def get_player_data_from_ddnet(player_name):
    url = 'https://ddnet.org/players/?json2=' + player_name
    response = requests.get(url)
    player_data=''
    if response.status_code == 200:
        player_data=response.json()
        #with open('data1.json', 'w', encoding='utf-8') as file:
            #json.dump(player_data, file, ensure_ascii=False, indent=2)
    return player_data

'''
def get_map_data():
    url='https://ddnet.org/releases/maps.json'
    response = requests.get(url)
    map_data=''
    if response.status_code == 200:
        map_data=response.json()
    return map_data
'''
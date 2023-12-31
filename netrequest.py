import requests
import json
from urllib.parse import quote


# 获取玩家id，返回玩家数据
def get_player_data_from_ddnet(player_name):
    url = 'https://ddnet.org/players/?json2=' + player_name
    response = requests.get(url)
    player_data = ''
    if response.status_code == 200:
        player_data = response.json()
        # with open('data1.json', 'w', encoding='utf-8') as file:
        # json.dump(player_data, file, ensure_ascii=False, indent=2)
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


def get_map_ranking_information(map_name):
    map_name_1 = quote(map_name, safe=':/?=')
    url = 'https://ddnet.org/maps/?json=' + map_name_1 + '&country=CHN'
    response = requests.get(url)
    map_ranking_information = ''
    if response.status_code == 200:
        map_ranking_information = response.json()
        # with open('data3.json', 'w', encoding='utf-8') as file:
        # json.dump(map_ranking_information, file, ensure_ascii=False, indent=2)

    return map_ranking_information

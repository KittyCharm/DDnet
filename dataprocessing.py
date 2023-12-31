# import json
from datetime import datetime, timezone, timedelta
from netrequest import get_player_data_from_ddnet, get_map_ranking_information
import calendar

# 获取json文件名，返回格式化后的数据
'''
def getflie(filename):
    with open(filename, 'r') as file:
        json_content = file.read()
        data = json.loads(json_content)
    return data
'''


# 获取玩家数据，返回过去一年游玩时长
def get_played_hours_last_year(player_data):
    annual_total_duration = player_data['hours_played_past_365_days']
    return annual_total_duration


# 获取玩家数据,返回游玩时间最长的日期和时长
def get_longest_time_for_playing(player_data):
    ltime = 0
    lday = []
    for adaily in player_data['activity']:
        # 年份限制
        if adaily['date'][:4] != '2023':
            continue
        if ltime < adaily['hours_played']:
            ltime = adaily['hours_played']
            lday.clear()
            lday.append(adaily['date'])

        elif ltime == adaily['hours_played']:
            lday.append(adaily['date'])
    return {'date': lday, 'hours': ltime}


# 获取玩家数据，返回最晚过图的图名和时间
def get_latest_time_for_passing_map(player_data):
    smap = ''
    sdate = ''
    stime = timedelta(hours=24)
    for types_key, types_value in player_data['types'].items():
        for maps_key, maps_value in types_value["maps"].items():
            timestamp = maps_value.get('first_finish')
            if timestamp != None:
                local_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
                # 年份限制
                if local_time.year != 2023:
                    continue
                # formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
                five_am = local_time.replace(hour=5, minute=0, second=0, microsecond=0)
                if local_time > five_am:
                    time_difference = timedelta(hours=24) - (local_time - five_am)
                else:
                    time_difference = five_am - local_time
                if time_difference < stime:
                    stime = time_difference
                    sdate = local_time
                    smap = maps_key
    return {'map': smap, 'time': sdate}


# 获取玩家数据，返回过的分数最高的图及分数
def get_map_with_highest_score(player_data):
    highest_score = 0
    map_with_highest_score = []
    for types_key, types_value in player_data['types'].items():
        for maps_key, maps_value in types_value["maps"].items():
            timestamp = maps_value.get('first_finish')
            if timestamp != None:
                # 年份限制
                if datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(
                        timezone(timedelta(hours=8))).year != 2023:
                    continue
                if highest_score < maps_value['points']:
                    highest_score = maps_value['points']
                    map_with_highest_score.clear()
                    map_with_highest_score.append(maps_key)
                elif highest_score == maps_value['points']:
                    map_with_highest_score.append(maps_key)
    return {'map': map_with_highest_score, 'score': highest_score}


# 获取玩家数据，返回过的次数最多的图及次数
def get_map_with_most_completion_times(player_data):
    most_completion_times = 0
    map_with_most_completion_times = []
    for types_key, types_value in player_data['types'].items():
        for maps_key, maps_value in types_value["maps"].items():
            finishes_times = maps_value.get('finishes')
            if finishes_times != None:
                if most_completion_times < finishes_times:
                    most_completion_times = finishes_times
                    map_with_most_completion_times.clear()
                    map_with_most_completion_times.append(maps_key)
                elif map_with_most_completion_times == finishes_times:
                    map_with_most_completion_times.append(maps_key)
    return {'map': map_with_most_completion_times, 'times': most_completion_times}


# -------------------分割线，注意调整后面的方法顺序---------------------------------


# 获取玩家数据，返回首次过的图及时间
def get_first_passing_map_information(player_data):
    timestamp = player_data['first_finish']['timestamp']
    local_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    map = player_data['first_finish']['map']
    return {'map': map, 'time': local_time}


# 获取玩家数据，返回全勤年--月
def get_full_attendance(player_data):
    current_year = int(player_data['activity'][0]['date'][:4])
    current_month = int(player_data['activity'][0]['date'][5:7])
    day_counting = 0
    monthly_playing_days = []
    for activity in player_data['activity']:
        year = int(activity['date'][:4])
        month = int(activity['date'][5:7])
        # day=int(activity['data'][8:])
        if current_year < year or current_month < month:
            monthly_playing_days.append([current_year, current_month, day_counting])
            current_year = year
            current_month = month
            day_counting = 0
        day_counting += 1
    full_attendence = []
    for i in monthly_playing_days:
        if i[1] in [1, 3, 5, 7, 8, 10, 12] and i[2] == 31:
            full_attendence.append(i[:2])
        if i[1] in [4, 6, 9, 11] and i[2] == 30:
            full_attendence.append(i[:2])
        if i[1] == 2 and ((calendar.isleap(i[0]) and i[2] == 29) or (not calendar.isleap(i[0]) and i[2] == 28)):
            full_attendence.append(i[:2])
    full_attendence_2023 = []
    # 取2023部分
    for i in full_attendence:
        if i[0] == 2023:
            full_attendence_2023.append(i)
    return full_attendence_2023


# 获取玩家数据，返回最喜欢的搭档及合作次数
def get_favorite_partner(play_data):
    favorite_partners = play_data.get('favorite_partners')
    if favorite_partners != None:
        favorite_partner = favorite_partners[0]['name']
        favorite_partner_times = favorite_partners[0]['finishes']
        return {'name': favorite_partner, 'times': favorite_partner_times}
    else:
        return ''


# 获取玩家数据，返回过去一年获得的分数
def get_scores_obtained_past_year(player_data):
    total_points = 0
    for types_key, types_value in player_data['types'].items():
        for maps_key, maps_value in types_value["maps"].items():
            timestamp = maps_value.get('first_finish')
            if timestamp != None:
                local_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
                if local_time.year == 2023:
                    total_points = total_points + maps_value['points']
    return total_points


# --------------------------------------------------------------------------------
def get_best_ranking(player_name):
    player_data = get_player_data_from_ddnet(player_name)
    candidate_maps = {}
    for types_key, types_value in player_data['types'].items():
        for maps_key, maps_value in types_value["maps"].items():
            if maps_value.get('rank') != None:
                candidate_maps[maps_key] = maps_value

    best_ranking_20 = sorted(candidate_maps.items(), key=lambda x: x[1]["rank"])[:20]
    best_ranking_20_result = [[name, {'rank': info['rank'], 'team_rank': info.get('team_rank'), 'time': info['time']}]
                              for name, info in best_ranking_20]
    count = 0

    for best_key, best_value in best_ranking_20:
        # print(best_key)
        map_ranking_information = get_map_ranking_information(best_key)
        for i in map_ranking_information['ranks']:
            if player_name == i['player']:
                best_ranking_20_result[count][1]['rank_CHN'] = i['rank']
                break
        if map_ranking_information['team_ranks'] != []:
            for i in map_ranking_information['team_ranks']:
                for j in i['players']:
                    if player_name == j:
                        best_ranking_20_result[count][1]['team_rank_CHN'] = i[
                            'rank']  # str(i['rank'])+f'{i['players']}'
                        break
        best_ranking_20_result[count][1]['type'] = map_ranking_information['type']
        best_ranking_20_result[count][1]['difficulty'] = map_ranking_information['difficulty']
        best_ranking_20_result[count][1]['points'] = map_ranking_information['points']
        count += 1

    return best_ranking_20_result


def number_to_circle_symbol(number):
    if 1 <= number <= 20:
        unicode_code_point = 0x245F + number  # U+245F is ①, U+2460 is ①, U+2461 is ②, and so on
        return chr(unicode_code_point)
    else:
        return "Number out of range"
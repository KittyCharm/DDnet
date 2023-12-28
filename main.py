from dataprocessing import *
from netrequest import get_player_data_from_ddnet
from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def welcome_interface():
    return ''


@app.route('/<player_name>/')
def obtain_annual_summary(player_name):
    # player_data = getflie('data.json')
    player_data = get_player_data_from_ddnet(player_name)
    if player_data != '':
        # 输出过去一年游玩时间
        played_time = get_played_hours_last_year(player_data)
        # print(f'过去一年你一共玩了{played_time}小时')

        # 输出游玩时间最长的日期及游玩时间
        longest_time_day = get_longest_time_for_playing(player_data)
        longest_time_date = longest_time_day['date']
        longest_time = longest_time_day['hours']
        # print(f"你在{longest_time_date}玩的时间最长，一天玩了{longest_time}小时。")

        # 输出最晚过图时间和图名
        lasted_passing_map_information = get_latest_time_for_passing_map(player_data)
        lasted_palaying_time = lasted_passing_map_information['time'].strftime('%Y-%m-%d %H:%M:%S')
        lasted_palaying_map = lasted_passing_map_information['map']
        # print(f'最晚在{lasted_palaying_time}过图，过的图是{lasted_palaying_map}')

        # 输出过的最高分的图及分数
        map_with_highest_score_information = get_map_with_highest_score(player_data)
        map_with_highest_score = map_with_highest_score_information['map']
        highest_score = map_with_highest_score_information['score']
        # print(f'过的最高分的图是{map_with_highest_score},有{highest_score}分')

        # 输出通过次数最多的图级次数
        map_with_most_completion_times_information = get_map_with_most_completion_times(player_data)
        map_with_most_completion_times = map_with_most_completion_times_information['map']
        most_completion_times = map_with_most_completion_times_information['times']
        # print(f'通过次数最多的图是{map_with_most_completion_times},共通过了{most_completion_times}次')

        # 首次过的图及时间
        first_passing_map_information = get_first_passing_map_information(player_data)
        first_passing_map = first_passing_map_information['map']
        first_passing_map_time = first_passing_map_information['time'].strftime('%Y-%m-%d %H:%M:%S')

        # 全勤月
        full_attendance = [item[1] for item in get_full_attendance(player_data)]

        # 最喜欢的搭档及合作次数
        favorite_partner_information = get_favorite_partner(player_data)
        favorite_partner = favorite_partner_information['name']
        favorite_partner_times = [favorite_partner_information['times']]

        # 过去一年获得的分数
        scores_obtained_past_year = get_scores_obtained_past_year(player_data)

        annual_summary_start=[f'在{first_passing_map_time}，你成功地通关了地图{first_passing_map}，这标志着{player_name}的ddnet游戏生涯正式启动。',f'{player_name}，你在{first_passing_map_time}完成了地图{first_passing_map}，从此步入了ddnet游戏的世界。',f'从{first_passing_map_time}那一刻开始，当你首次攻克地图{first_passing_map}，{player_name}的ddnet之旅正式开启。',f'{player_name}，你在{first_passing_map_time}迎来了你的第一次挑战的成功，你通过了{first_passing_map}地图，这也是你ddnet游戏之旅的起点。',f'自{first_passing_map_time}你成功通过{first_passing_map}的那一刻起，{player_name}的ddnet游戏历程就此展开。',f'{first_passing_map_time}，你初次尝到了闯过{first_passing_map}的喜悦，那一刻，{player_name}的ddnet之旅正式开拓。',f'{player_name}，你的ddnet游戏生涯始于{first_passing_map_time}，在那个时刻，你首次通过了{first_passing_map}地图。',f'{player_name}，你在{first_passing_map_time}对地图{first_passing_map}的首次成功挑战，标志着你的ddnet游戏历程的开启。',f'在{first_passing_map_time}，{player_name}你首次通过了{first_passing_map}地图，这一事件是你ddnet游戏生涯的起源。',f'{player_name}，在{first_passing_map_time}那一刻，你首次攻克了{first_passing_map}地图，同样也开启了你在ddnet游戏中的新篇章。']
        annual_summary_main=[f'在过去的一年中，你总共投入了 {played_time} 小时在游戏中。在这期间，你在 {longest_time_date} 的那一天游玩时间最长，高达 {longest_time} 小时。记得你在 {lasted_palaying_time} 通关了 {lasted_palaying_map} 这张地图，哪个时刻真是令人难忘。\n你的技术也有了显著的提升，你在 {map_with_highest_score} 地图上取得了最高分，达到了惊人的 {highest_score} 分，这甚至可能是所有玩家中的最高分之一。在 {full_attendance} 这几个月里，你毫无遗漏地每天都进行了游戏，说明你对此游戏的热爱和坚持。\n在过去的一年里，你一共获得了 {scores_obtained_past_year} 分，这是你努力付出的结果。让我们期待新的一年，你将创造更多的记录并享受游戏带来的乐趣！',f'回顾过去一年的游戏历程，你有 {played_time} 小时在这个虚拟世界里度过。记得在 {longest_time_date} 那天，你的投入时间达到了峰值，一整天你玩了长达 {longest_time} 小时。你最晚在 {lasted_palaying_time} 完成了 {lasted_palaying_map} 地图的挑战，那一刻的成就感必定无与伦比。\n你的技术突飞猛进，其中在 {map_with_highest_score} 的地图上你获得了最高分，打出了令人惊叹的 {highest_score} 分。在 {full_attendance} 这些月份，你的出勤率达到了百分之百，每一天都沉浸在游戏的乐趣中。\n一年的累计下来，你共得到了 {scores_obtained_past_year} 分，这是你持续努力的象征。期待在新的一年，你能持续享受游戏，创造更多的辉煌成绩！',f'过去一年，你的游戏时间累计达到了 {played_time} 小时，充分展现了你对游戏的热爱和投入。值得一提的是，在 {longest_time_date} 这一天，你玩了整整 {longest_time} 小时，游戏时间创下了新高。\n你在 {lasted_palaying_time} 通过了 {lasted_palaying_map} 地图，这无疑是一个重要的里程碑。同时，你也在 {map_with_highest_score} 地图上打破了个人纪录，拿到了惊人的 {highest_score} 分，这一成就无疑彰显了你在游戏中的技艺。\n更加令人印象深刻的是，在 {full_attendance} 这些月份里，你没有间断过一天游戏，每日坚持使你所获得的总分在过去一年累积到了 {scores_obtained_past_year} 分。\n在接下来的一年中，期待你能在游戏的道路上取得更多成就，继续享受其中的乐趣并取得更出色的表现！']

        annual_summary=random.choice(annual_summary_start)+'\n'+random.choice(annual_summary_main)

        return annual_summary

        '''
        return f'过去一年你一共玩了{played_time}小时。' \
               f'你在{longest_time_date}玩的时间最长，一天玩了{longest_time}小时。' \
               f'最晚在{lasted_palaying_time}过图，过的图是{lasted_palaying_map}。' \
               f'过的最高分的图是{map_with_highest_score},有{highest_score}分。' \
               f'通过次数最多的图是{map_with_most_completion_times},共通过了{most_completion_times}次。' \
               f'你在{first_passing_map_time}通过了{first_passing_map}，开启了你的ddnet之旅。' \
               f'你在{full_attendance}这几个月每天玩。' \
               f'你最喜欢的搭档是{favorite_partner},你们一共合作了{favorite_partner_times}次。' \
               f'你在过去一年一共获得了{scores_obtained_past_year}分。'
        
        return f'{first_passing_map_time}，你首次通过了地图{first_passing_map}，你的ddnet游戏之旅就此展开！\n' \
               f'这过去的一年里中，你投入到游戏的时间累计达到了{played_time}小时。对于你而言，最为难忘的一天应该是{longest_time_date}，那一天你一口气玩了整整{longest_time}小时。你还记得那个深夜吗？是在{lasted_palaying_time}，你成功闯过了{lasted_palaying_map}，那个瞬间无比激动人心。\n' \
               f'在你的历程中，曾创造了最高分记录的地图是{map_with_highest_score}，你在那儿拿下了令人瞩目的{highest_score}分。而你挑战频率最高的地图则是{map_with_most_completion_times}，你已经成功通关了它{most_completion_times}次。\n' \
               f'在{full_attendance}的那些月份里，你每一天都坚持在游戏中度过，你的精神实属可佳。又或者，我们要谈论你的团队伙伴{favorite_partner}，你们共同完成了{favorite_partner_times}次任务，这种默契的配合令人印象深刻。\n' \
               f'至于你的总成绩，今年你赢得了总计{scores_obtained_past_year}分。这是你这一年游戏的成就与经历，你的每一个决策和努力都塑造了今天的你。'
        '''
    else:
        return '网络请求出错'


if __name__ == '__main__':
    app.run(debug=True)
'''
    player_data = get_player_data_from_ddnet('飞翔的翅膀')
    testing=get_scores_obtained_past_year(player_data)
    print(testing)
'''

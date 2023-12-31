from dataprocessing import *
from netrequest import get_player_data_from_ddnet, get_map_ranking_information
from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def welcome_interface():
    return '欢迎使用DDnet年度总结'


@app.route('/<player_name>/')
def obtain_annual_summary(player_name):
    # player_data = getflie('data.json')
    player_data = get_player_data_from_ddnet(player_name)
    player_name = ' [' + player_name + '] '
    if player_data != '' and player_data != {}:
        # 输出过去一年游玩时间
        played_time = get_played_hours_last_year(player_data)
        # print(f'过去一年你一共玩了{played_time}小时')

        # 输出游玩时间最长的日期及游玩时间
        longest_time_day = get_longest_time_for_playing(player_data)
        longest_time_date = random.choice(longest_time_day['date'])
        longest_time = longest_time_day['hours']
        # print(f"你在{longest_time_date}玩的时间最长，一天玩了{longest_time}小时。")

        # 输出最晚过图时间和图名
        lasted_passing_map_information = get_latest_time_for_passing_map(player_data)
        if lasted_passing_map_information['map'] == '':
            return f'{player_name},看起来你在过去的一年一张图都没有过呢！'
        lasted_palaying_time = lasted_passing_map_information['time'].strftime('%Y-%m-%d %H:%M:%S')
        lasted_palaying_map = '[' + lasted_passing_map_information['map'] + ']'
        lasted_palaying_time_date = lasted_palaying_time[:10]
        lasted_palaying_time_time = lasted_palaying_time[11:]
        # print(f'最晚在{lasted_palaying_time}过图，过的图是{lasted_palaying_map}')

        # 输出过的最高分的图及分数
        map_with_highest_score_information = get_map_with_highest_score(player_data)
        map_with_highest_score = '[' + random.choice(map_with_highest_score_information['map']) + ']'
        highest_score = map_with_highest_score_information['score']
        # print(f'过的最高分的图是{map_with_highest_score},有{highest_score}分')

        # 输出通过次数最多的图级次数
        map_with_most_completion_times_information = get_map_with_most_completion_times(player_data)
        map_with_most_completion_times = '[' + random.choice(map_with_most_completion_times_information['map']) + ']'
        most_completion_times = map_with_most_completion_times_information['times']
        # print(f'通过次数最多的图是{map_with_most_completion_times},共通过了{most_completion_times}次')

        # 首次过的图及时间
        first_passing_map_information = get_first_passing_map_information(player_data)
        first_passing_map = '[' + first_passing_map_information['map'] + ']'
        first_passing_map_time = first_passing_map_information['time'].strftime('%Y-%m-%d %H:%M:%S')

        # 全勤月
        full_attendance = [item[1] for item in get_full_attendance(player_data)]
        number_of_months = len(full_attendance)

        # 最喜欢的搭档及合作次数
        favorite_partner_information = get_favorite_partner(player_data)
        if favorite_partner_information != '':
            favorite_partner = ' [' + favorite_partner_information['name'] + '] '
            favorite_partner_times = favorite_partner_information['times']

        # 过去一年获得的分数
        scores_obtained_past_year = get_scores_obtained_past_year(player_data)

        annual_summary_start = [
            f'在{first_passing_map_time}，你成功地通关了{first_passing_map}，这标志着{player_name}的ddnet游戏生涯正式启动。',
            f'{player_name}，你在{first_passing_map_time}完成了{first_passing_map}，从此步入了ddnet游戏的世界。',
            f'从{first_passing_map_time}你首次攻克{first_passing_map}这一刻开始，{player_name}的ddnet之旅正式开启。',
            f'{player_name}，你在{first_passing_map_time}迎来了你的第一次过图的成功，你通过了{first_passing_map}，这也是你ddnet游戏之旅的起点。',
            f'自{first_passing_map_time}你成功通过{first_passing_map}的那一刻起，{player_name}的ddnet游戏历程就此展开。',
            f'{first_passing_map_time}，你初次尝到了闯过{first_passing_map}的喜悦，那一刻，{player_name}的ddnet之旅正式开拓。',
            f'{player_name}，你的ddnet游戏生涯始于{first_passing_map_time}，在那个时刻，你首次通过了{first_passing_map}。',
            f'{player_name}，你在{first_passing_map_time}对{first_passing_map}的成功挑战，标志着你的ddnet游戏历程的开启。',
            f'在{first_passing_map_time}，{player_name}，你首次通过了{first_passing_map}地图，这是你ddnet游戏生涯的起源。',
            f'{player_name}，在{first_passing_map_time}那一刻，你首次攻克了{first_passing_map}，同样也开启了你在ddnet游戏中的新篇章。']
        annual_summary_main_1 = [
            f'在过去的一年中，你共投入了{played_time}小时的时间来享受这款游戏。其中，你一天中最长的游戏时间出现在{longest_time_date}，那一天你玩了惊人的{longest_time}小时。你曾在{lasted_palaying_time_date}深夜{lasted_palaying_time_time}成功通关{lasted_palaying_map}，足以证明你的坚持和热爱。你所获得的最高分数是在{map_with_highest_score}，你斩获了令人瞠目的{highest_score}分。',
            f'在过去的一年里，你有{played_time}小时花在了这款游戏上。你的热情和投入在{longest_time_date}达到了顶峰，那一天你投入了整整{longest_time}小时。透过你在{lasted_palaying_time_date}深夜{lasted_palaying_time_time}通关{lasted_palaying_map}的例子，可以看到你对游戏的执着和热爱。\n你在{map_with_highest_score}获得了单张地图的最高分数，{highest_score}分，这是你技巧和努力的明证。',
            f'在过去的一年中，你为这款游戏贡献了总计{played_time}小时的时间。记得是{longest_time_date}，你创下了单日最长游玩时间，达到了整整{longest_time}小时。还有那个深夜，在{lasted_palaying_time}，你成功通关了{lasted_palaying_map}，展现了你对游戏的热忱和毅力。\n你的技巧和努力在{map_with_highest_score}得到了充分的体现，你在这张地图上取得了骄人的{highest_score}分。']
        if lasted_passing_map_information['time'] < lasted_passing_map_information['time'].replace(hour=5, minute=0,
                                                                                                   second=0,
                                                                                                   microsecond=0):
            annual_summary_main_1.append(
                f'你在过去的一年里，为这款游戏投入了{played_time}小时。其中，你在{longest_time_date}那天创下了个人单日最长游戏时间记录，玩了长达{longest_time}小时。更令人印象深刻的是，你在{lasted_palaying_time_date}凌晨{lasted_palaying_time_time}成功地通关了{lasted_palaying_map}，这无疑证明了你对游戏的热爱和毅力。\n你的技能和决心都在{map_with_highest_score}得到了明显的体现，你赢得了高达{highest_score}分。')
            annual_summary_main_1.append(
                f'在上一年度，你投入了总计{played_time}小时在这款游戏中。令人印象深刻的是，在{longest_time_date}那天，你玩了整整{longest_time}小时，这是你的最长游戏时间记录。更难得的是，你在{lasted_palaying_time_date}凌晨{lasted_palaying_time_time}成功通过了{lasted_palaying_map}，展示了你对游戏的热诚和不屈不挠的精神。\n你的技艺和毅力在{map_with_highest_score}充分体现，你在那里获得了高达{highest_score}分。')
        annual_summary_main_2 = [
            f'在{full_attendance}这{number_of_months}个月里，你表现出了无比的投入，每天都会抽出时间来玩游戏。',
            f'在{full_attendance}这{number_of_months}个月里，你无一天缺席，每日都在游戏中度过。',
            f'在{full_attendance}这{number_of_months}个月，你的坚持更是令人钦佩，每天都在线进行游戏。',
            f'在{full_attendance}这{number_of_months}个月，你每天都会登陆游戏，你的坚持和热情让人感到敬佩。',
            f'值得称赞的是，在{full_attendance}的这{number_of_months}个月里，你每天都坚持玩游戏，显示出你的专注和坚持。']
        annual_summary_main_3 = [
            f'过去的一年，你一共累积了{scores_obtained_past_year}分，这个成绩足以证明你的努力和技巧。',
            f'过去的一年，你已经累计得到了{scores_obtained_past_year}分，这是你付出了时间、精力和技巧换来的成果。',
            f'过去一年，你累计了{scores_obtained_past_year}分，这无疑证明了你的能力和付出。',
            f'过去一年，你累计了{scores_obtained_past_year}分，这无疑证明了你的能力和付出。',
            f'整个过去的一年，你总共获得了{scores_obtained_past_year}分，这充分表明了你的技巧和付出。']
        annual_summary_main_4 = [
            f'在你的游戏历程中，{map_with_most_completion_times}是你最常通过的，总共成功通关了{most_completion_times}次，反映出你对这张地图的热爱和精通。',
            f'在你的游戏历程中，{map_with_most_completion_times}无疑是你最喜欢的，因为你在这里取得了{most_completion_times}次的成功通关，标志着你对这张地图的技巧和深度理解。',
            f'在你的游戏旅程中，{map_with_most_completion_times}是你通关次数最多的，达到了惊人的{most_completion_times}次，体现了你对这张地图的熟练掌握和喜好。',
            f'在你精彩的游戏历程中，{map_with_most_completion_times}无疑是你最擅长的，因为你已经成功地完成了{most_completion_times}次，这个记录展示出你对这张地图深入的理解和卓越的技巧。',
            f'在你的游戏历程中，{map_with_most_completion_times}是你最常挑战并成功通关的，共计通过{most_completion_times}次。这充分证明了你对该地图的熟练掌握和喜爱。']
        annual_summary_main_5 = [
            f'同时，{favorite_partner}成为了你最频繁合作的搭档，你们一起过图{favorite_partner_times}次，这展示了你们间深厚的默契和友谊。',
            f'同时，在所有的游戏伙伴中，你与{favorite_partner}的合作最为紧密，共同过图{favorite_partner_times}次，体现了你们之间的强烈默契和深刻友谊。',
            f'在所有的队友中，你最倾向于与{favorite_partner}一起合作，你们已经共同完成了{favorite_partner_times}次挑战，展现了你们之间紧密的配合和深厚的友情。',
            f'另外，你与{favorite_partner}建立了稳固的伙伴关系，{favorite_partner_times}次的合作，证明了你们之间的默契和友谊。',
            f'与此同时，你与搭档{favorite_partner}的合作频率非常高，一共进行了{favorite_partner_times}次合作，反映出了你们之间深厚的默契和友情。']
        annual_summary_main_5_nopartner = [
            '另外，看起来你是一个独行侠，暂时还没有找到你的游戏伙伴哦！但别担心，就像一个真正的超级英雄一样，你完全有能力自己完成任务！']
        annual_summary_end = [
            '回顾过去一年，你的表现无疑是卓越的。在新的一年中，愿你继续享受游戏的乐趣，保持对挑战的热情，并与你的搭档共同创造更多的精彩。让我们期待未来的一年，祝你游戏愉快！',
            '一年的游戏历程已经落幕，你在这期间付出的努力和取得的成就都值得赞扬。在新的一年里，愿你继续探索，享受每一次的游戏体验，并与伙伴共同攀登更高的巅峰。期待你在接下来的日子里创造更多美好的回忆，祝游戏顺利！',
            '在过去的一年里，你的表现异常出色，并取得了许多令人难以忘怀的成就。在新的一年里，希望你能保持这种热情，继续与队友一起创造更多精彩的时刻。期待你在未来的游戏旅程中实现更多的胜利和乐趣，祝你游戏愉快！',
            # '随着一年的结束，你取得了许多令人瞩目的成就。在新的一年中，让我们期待你继续以这种热情和决心面对挑战，享受游戏的乐趣，并与伙伴共同开创更多的辉煌。愿你的游戏之路越走越宽广，祝游戏顺利！',
            '经过一年的精彩表现，你的努力和进步都得到了充分的体现。在新的一年中，期待你能再创佳绩。无论是独闯或与伙伴并肩作战，愿你都能享受每一次的游戏历程。祝新的一年里游戏愉快，成就满满！',
            '在过去一年的游戏历程中，你的成绩和努力有目共睹。新的一年里，希望你继续保持这种热情，无论是挑战新地图还是与伙伴共同作战，都能享受其中的乐趣。期待你在未来的岁月中创造更多亮眼的成绩，祝你游戏愉快！',
            '过去的一年，你在游戏中展现了不凡的实力和坚韧的毅力。新的一年已经开启，期待你继续享受每一个挑战，与队友并肩作战，创造更多精彩的瞬间。无论何时，都要记住，游戏的真谛在于快乐。祝你在新的一年里游戏顺利，收获满满！',
            # '一年的游戏旅程已经落下帷幕，你在这个过程中取得的成就和付出的努力都值得我们为你骄傲。新的一年里，让我们期待你继续以满腔热情面对每一个挑战，创造更多美好的回忆，并与你的伙伴一起走向新的高峰。祝愿你在接下来的一年中游戏愉快，尽享乐趣！',
            '回顾过去的一年，你在游戏中的表现绝对令人钦佩。新的一年已经开始，希望你持续你的热情和才华，再创辉煌。无论是独自挑战还是与伙伴并肩作战，祝你都能享受其中的每一刻，取得更多的胜利。期待新的一年，你将有更多精彩的表现，祝游戏愉快！',
            '过去的一年，你在游戏中取得了许多值得庆祝的成就。新的一年，让我们期待你继续挑战自我，享受每一场游戏，并与伙伴共同前进。愿你的游戏之旅充满欢笑和胜利，期待你在未来创造更多的精彩瞬间。祝你在新的一年里游戏顺利，快乐无穷！']

        # 年度总结初版
        annual_summary = random.choice(annual_summary_start) + '\n' + random.choice(
            annual_summary_main_1)

        # 判断是否有全勤月，决定是否添加全勤信息
        if number_of_months != 0:
            annual_summary = annual_summary + random.choice(annual_summary_main_2)

        annual_summary = annual_summary + random.choice(annual_summary_main_3) + '\n' + random.choice(
            annual_summary_main_4)

        # 判断是否有和搭档一起玩过游戏，决定返回信息
        if favorite_partner_information != '':
            annual_summary = annual_summary + random.choice(annual_summary_main_5)
        else:
            annual_summary = annual_summary + random.choice(annual_summary_main_5_nopartner)

        annual_summary = annual_summary + '\n' + random.choice(annual_summary_end)

        # ---------------------------------------------------------------------------------

        # 年度总结创新1版
        annual_summary_1 = f'自{first_passing_map_time}将{first_passing_map}初次攻下的那一刻起，喵~我们可爱的{player_name}在ddnet的冒险就正式启动啦！\n在过去的一年里，你用了{played_time}小时的宝贵时间来享受这款游戏，真是太投入啦！其中，你最长的一天游戏时间出现在{longest_time_date}，那天你玩了惊人的{longest_time}小时，简直是个打游戏的小怪兽呢！话说，你还记得在{lasted_palaying_time_date}深夜{lasted_palaying_time_time}你通关了{lasted_palaying_map}吗？这可是证明了你持之以恒的爱好和坚定不移的毅力哟！而你在{map_with_highest_score}获得的最高分数是惊人的{highest_score}分，这也足以证明你的技艺和实力了。'
        if number_of_months != 0:
            annual_summary_1 += f'喵~看到你在{full_attendance}这{number_of_months}个月中如此专注于游戏，真是让我感到钦佩！你每天都会抽出时间来享受游戏，真是个游戏狂魔呢！'
        annual_summary_1 += f'过去的一年，你累积了{scores_obtained_past_year}分，这个数字就是对你努力和技巧的最好证明。\n在你的游戏历程中，{map_with_most_completion_times}显然是你最常挑战并成功的地图，你过了{most_completion_times}次，这充分展示了你对它的热爱和精通。与此同时，{favorite_partner}成为了你最喜欢的合作伙伴，你们两个一起过图了{favorite_partner_times}次，这可真是个强大的二人组合呢！\n回首过去的一年，你的表现无疑是让人眼花缭乱的。在新的一年里，我希望你能继续享受游戏的快乐，保持热情，接受更多的挑战，并与你的合作伙伴共同创造更多的辉煌！让我们一起期待未来的每一天，祝你游戏愉快，喵~！'

        # 年度总结创新2版
        annual_summary_2 = f'从{first_passing_map_time}你破解{first_passing_map}的那一刻开始，嘿嘿~{player_name}的ddnet之旅才算是真正开启了。\n过去一年你花了{played_time}小时在这款游戏中享乐，这种投入，简直像是柔情似水的恋人。最长的一天出现在{longest_time_date}，你和游戏度过了美妙的{longest_time}小时，这让人不禁会想起一场激情四溢的约会哦！记得那个夜晚吗？{lasted_palaying_time_date}深夜{lasted_palaying_time_time}你成功通关{lasted_palaying_map}，这就如同在月色下的柔情密语，证明了你的执着和热爱。而你在{map_with_highest_score}取得的最高分数是惊人的{highest_score}分，这可看出了你的游戏技巧如同熟练的爱情专家般流畅。'
        if number_of_months != 0:
            annual_summary_2 += f'在{full_attendance}这{number_of_months}个月里，你每天都与游戏共度时光，宛如痴迷的情人，每日都怀揣对她的思恋。'
        annual_summary_2 += f'过去一年，你一共得到了{scores_obtained_past_year}分，这个数字就像是你对游戏的深情告白。\n要说起你最喜欢去的地方，那必须是{map_with_most_completion_times}了，你在这里成功攻克了{most_completion_times}次，像是情人间不断重复的甜蜜互动。而{favorite_partner}成为了你最常携手共进的伙伴，你们一同过关斩将了{favorite_partner_times}次，就像是两颗心跳步调一致的恋人。\n过去的一年，你的表现让人如痴如醉。在新的一年里，希望你继续享受游戏的乐趣，保持对挑战的热情，并与你的伙伴一起创造更多的浪漫时刻。期待未来的每一天，祝你游戏愉快，嘿嘿~！'

        # 年度总结创新3版
        annual_summary_3 = f'就从那个{first_passing_map_time}你首次攻克{first_passing_map}的时刻开始，哼~看来{player_name}也算是正式踏上了ddnet的旅程了嘛。\n在过去的一年中，你竟然花了{played_time}小时玩这款游戏。好吧，我承认，你这样的投入让我有些惊讶。你最长时间的游戏记录出现在{longest_time_date}，你居然玩了整整{longest_time}小时，恕我直言，你真是一个游戏疯子啊！而你在{lasted_palaying_time_date}深夜{lasted_palaying_time_time}通关{lasted_palaying_map}的壮举，虽然我不大愿意承认，但这确实证明了你的坚韧和热情。再说，你在{map_with_highest_score}获得的最高分数居然达到了{highest_score}分，这一定是运气好，对，一定是运气好。'
        if number_of_months != 0:
            annual_summary_3 += f'在{full_attendance}这{number_of_months}个月里，你每天都会抽出时间来玩游戏，看来你果然是一个勤奋的人呢。'
        annual_summary_3 += f'过去一年，你累计获得了{scores_obtained_past_year}分，哼，虽然我不想说，但这个成绩确实证明了你的努力和才能。\n在你的游戏历程中，{map_with_most_completion_times}是你最常挑战并成功的地图，你居然过了{most_completion_times}次，这也反映出你对这张地图的熟悉和精通。同时，{favorite_partner}成为了你最频繁合作的伙伴，你们一起过图{favorite_partner_times}次，看来你们确实有很好的默契和团队精神。\n回顾过去一年，虽然我不想承认，但是你的表现确实出色。新的一年，愿你继续享受游戏，接受更多的挑战，并与你的伙伴一起创造更多的辉煌。期待未来的每一天，祝你游戏愉快，不过，别以为我会因此而佩服你哦！'

        # 年度总结创新4版
        annual_summary_4 = f'自{first_passing_map_time}你首次征服{first_passing_map}的那一刻开始...呵呵，我的{player_name}~你在ddnet的旅程终于启航了呢。\n你已经沉迷这款游戏整整{played_time}小时了，看来你在这个游戏中找到了属于你的乐趣呢。最长的一天是{longest_time_date}，你陪着游戏度过了{longest_time}小时，和她相处的时间好长啊，我都快嫉妒起来了哦。还记得那个晚上吗？在{lasted_palaying_time_date}深夜{lasted_palaying_time_time}，你完成了{lasted_palaying_map}，就像在黑暗中找到了亮光，你真的是太厉害了。而且你在{map_with_highest_score}拿下了最高的{highest_score}分，你真的是太棒了，我都有些无法直视了呢。'
        if number_of_months != 0:
            annual_summary_4 += f'在过去的{full_attendance}个月里，你每天都会抽出时间来陪伴游戏，就像那个永远不离开她的骑士一样。'
        annual_summary_4 += f'过去的一年，你获得了{scores_obtained_past_year}分，这个数字就像是你对游戏的疯狂热爱的见证。\n在你的游戏历程中，{map_with_most_completion_times}是你最常通过的地图，成功通关了{most_completion_times}次，看来这个地方对你有特殊的意义呢。而{favorite_partner}成为了你最频繁合作的伙伴，你们一起过图了{favorite_partner_times}次，你们的默契真是令人羡慕啊。\n回顾过去的一年，你的表现自然是出色的，我也会一直在这里守候你，见证你的成长。新的一年，我希望你可以继续享受游戏的乐趣，接受更多的挑战，并与你的伙伴一起创造更多辉煌的记录。期待未来的每一天，祝你游戏愉快，我会一直在这里陪着你的，永远都不会离开哦~'

        # 年度总结创新5版
        annual_summary_5 = f'从{first_passing_map_time}你可爱地完成了{first_passing_map}的挑战那一刻开始，噔噔~我家的{player_name}在ddnet的冒险之旅就正式启动啦！\n在过去的一年里，你用肉肉的小手玩了{played_time}小时的这款游戏，真是个勤劳的小豆包呢！最长的一天出现在{longest_time_date}，你和游戏度过了甜蜜的{longest_time}小时，好像是在无尽的糖果森林中遨游呀！说起来，你还记得那个夜晚吗？{lasted_palaying_time_date}深夜{lasted_palaying_time_time}你成功通关{lasted_palaying_map}，就像是在梦境中找到了宝藏，真是证明了你持之以恒的爱好和坚定不移的精神哟！而你在{map_with_highest_score}获得的最高分数是惊人的{highest_score}分，这也足以证明你的技艺和实力了。'
        if number_of_months != 0:
            annual_summary_5 += f'在{full_attendance}这{number_of_months}个月中，你每天都会抽出时间来享受游戏，真是个游戏狂魔呢！'
        annual_summary_5 += f'过去的一年，你累积了{scores_obtained_past_year}分，这个数字就是对你努力和技巧的最好证明。\n在你的游戏历程中，{map_with_most_completion_times}显然是你最常挑战并成功的地图，你过了{most_completion_times}次，这充分展示了你对它的热爱和精通。与此同时，{favorite_partner}成为了你最喜欢的合作伙伴，你们两个一起过图了{favorite_partner_times}次，这可真是个强大的二人组合呢！\n回首过去的一年，你的表现无疑是让人眼花缭乱的。在新的一年里，我希望你能继续享受游戏的快乐，保持热情，接受更多的挑战，并与你的合作伙伴共同创造更多的辉煌！让我们一起期待未来的每一天，祝你游戏愉快，噔噔~！'

        # 年度总结创新6版
        annual_summary_6 = f'自{first_passing_map_time}你轻轻地踏入了{first_passing_map}的胜利之门，啊，{player_name}，就在那一刻，你的ddnet旅程像诗一般展开了。\n在过去的一年里，你以{played_time}小时的时间，像是在临摹一幅精美画卷，将这款游戏深深铭记在心。最长的一天出现在{longest_time_date}，那一天，你与游戏相伴了{longest_time}小时，宛如在浩瀚的星空下，陷入了一段深深的沉思。你可还记得{lasted_palaying_time_date}那个深夜{lasted_palaying_time_time}的时刻？你成功通关了{lasted_palaying_map}，那一刻，就像是在琴弦上拂过一道清亮的音符，证明了你的执着和热情。而你在{map_with_highest_score}所取得的{highest_score}分，仿佛是最纯洁的白色，展示了你超凡的技艺。'
        if number_of_months != 0:
            annual_summary_6 += f'在{full_attendance}的{number_of_months}个月中，你每一天都会抽出时间来温柔对待这场游戏，如同每日书写一首甜美的小诗。'
        annual_summary_6 += f'过去的一年，你累积了{scores_obtained_past_year}分，这个数字就像是你历尽风雨后绽放的一朵花。\n在你的游戏历程中，{map_with_most_completion_times}是你最热衷的舞台，你在这里演绎了{most_completion_times}次精彩。同时，{favorite_partner}成为了你最频繁的合作伙伴，你们共同创造了{favorite_partner_times}次美妙的和谐之声，仿佛是一首动人的二重奏。\n回望过去的一年，你的表现就像是一篇美妙的诗歌。新的一年，愿你依旧享受游戏的乐趣，面对更多的挑战，并与你的伙伴共同创造属于你们的故事。期待未来每一个温馨的日子，祝你游戏愉快，一路芬芳~'

        # 年度总结创新7版
        annual_summary_7 = f'从...嗯，那个，就是{first_passing_map_time}你第一次通过{first_passing_map}的那一刻开始，呃...{player_name}您在ddnet的旅程，就像悄悄开启了一扇门...\n过去的一年里，您，您投入了{played_time}小时在这款游戏上。最...最长的一天是在{longest_time_date}，那天您玩了整整{longest_time}小时，简直像是被游戏吸引得无法自拔呢。还有...那个晚上，您记得吗？{lasted_palaying_time_date}深夜{lasted_palaying_time_time}，您成功通关了{lasted_palaying_map}，虽然我不好意思说，但那真的证明了您的坚持和热爱。而且，您在{map_with_highest_score}获得的高分达到了{highest_score}分，这，这也足以见证您的技艺和水平啦。'
        if number_of_months != 0:
            annual_summary_7 += f'在过去的{full_attendance}这{number_of_months}个月里，您每天都会抽出时间来，来玩游戏。'
        annual_summary_7 += f'过去的一年，您共计积累了{scores_obtained_past_year}分，这个成绩...我想，这应该证明了您的努力和技巧吧。\n在您的游戏历程中，{map_with_most_completion_times}是您最常挑战并成功的，您在那里成功了{most_completion_times}次，这应该反映出您对这张地图的喜爱和技巧。同时，{favorite_partner}成为了您最常合作的伙伴，你们一起过图了{favorite_partner_times}次，我想，这应该展示了你们深厚的默契和友情吧。\n回顾过去的一年，您的表现无疑是...是杰出的。在新的一年中，希望您能继续享受游戏的乐趣，保持对挑战的热情，并与您的伙伴一起创造更多的精彩。期待未来的每一天，祝您游戏愉快，嗯...再见。'

        if random.choice([1, 2]) == 1 or favorite_partner_information == '':
            return annual_summary
        else:
            return random.choice(
                [annual_summary_1, annual_summary_2, annual_summary_3, annual_summary_4, annual_summary_5,
                 annual_summary_6, annual_summary_7])

    elif player_data == {}:
        return random.choice([f'{player_name}，看起来你的游戏ID在玩捉迷藏，我们暂时找不到它呢！',
                              f'{player_name}，唔……你的游戏ID似乎穿上了隐形斗篷，我们暂时无法找到它呢！',
                              f'{player_name}，嘿，你的游戏ID似乎开启了隐身模式，我们正在努力寻找它！'])

    else:
        return random.choice([f'{player_name}，看来我们的网络信使鸽子飞走了，暂时无法完成你的请求呢！',
                              f'{player_name}，看来我们的网络正在度假，暂时无法完成你的请求哦！',
                              f'{player_name}，似乎我们的网线被猫玩过了，暂时无法完成你的请求呢'])


@app.route('/rank20/<player_name>/')
def Obtain_best_ranking_result(player_name):
    best_ranking = get_best_ranking(player_name)
    if best_ranking=='':
        return '查询失败，请检查id或稍后再试'
    best_ranking_result = ''
    count = 1
    for i in best_ranking:
        best_ranking_result += f'{number_to_circle_symbol(count)}'
        best_ranking_result += f"【{i[0]}】，【{i[1]['type']}{i[1]['difficulty']}星{i[1]['points']}分】，世界个人排名：{i[1]['rank']}，"
        if i[1]['team_rank'] != None:
            best_ranking_result += f"世界队伍排名：{i[1]['team_rank']}，"
        else:
            best_ranking_result += f'世界队伍排名：无，'
        if i[1].get('rank_CHN') != None:
            best_ranking_result += f"国服个人排名{i[1]['rank_CHN']}，"
        if i[1].get('team_rank_CHN') != None:
            best_ranking_result += f"国服队伍排名{i[1]['team_rank_CHN']}，"
        hours, remainder = divmod(i[1]['time'], 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        formatted_time = "{:02}:{:02}:{:02}.{:03}".format(int(hours), int(minutes), int(seconds), milliseconds)
        best_ranking_result += f'最佳用时：{formatted_time}。\n'
        count += 1
    return best_ranking_result


if __name__ == '__main__':
    app.run(debug=True)

    # player_name='飞翔的翅膀'
    # player_data = get_player_data_from_ddnet(player_name)
    # testing=get_best_ranking(player_name)
    # print(testing)

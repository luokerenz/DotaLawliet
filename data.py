from re import findall
from urllib.request import urlopen, Request
import json

def opendotaRequest(steamID,request_data):
    cusHeader = {'User-Agent' : 'DotaLawliet'}
    if request_data == 'basic':
        url = 'http://api.opendota.com/api/players/%s' %steamID
    elif request_data == 'hero_ranking':
        #url = 'http://api.opendota.com/api/players/%s/rankings' %steamID
        url = 'http://api.opendota.com/api/players/%s/heroes?limit=50' %steamID
    temp = Request(url,data=None,headers=cusHeader)
    match_return = urlopen(temp).read()
    return match_return.decode('utf-8')
#------------------------------------------------------------------------------------------

def refreshMatch(serLogAdd):
    steamIDmask = "DOTA_GAMEMODE_.*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\].*?:(\d{5,})\]"
    try:
        f = open(serLogAdd)
    except Exception:
        return 'invalid server_log.txt path!', ['']

    for check_line in reversed(f.readlines()):
        idList = findall(steamIDmask, check_line)
        if idList:
            final_steamID_list = idList[0]
            break
        else:
            pass

    # final_steamID_list format: [id0, id1, ..., id9]

    final_return = []
    for i in range(0,10):
        temp_list = []
        #print 'processing steamID: %s' %final_steamID_list[i]
        match_return = opendotaRequest(final_steamID_list[i], 'basic')
        test_jsonFormat = json.loads(match_return)

        if test_jsonFormat.get("profile"):
            name = test_jsonFormat["profile"]["personaname"]
            ava = test_jsonFormat["profile"]["avatar"]
            temp_list.append(name)
            temp_list.append(ava)
        else:
            temp_list.append(0)
            temp_list.append(0)

        mmr_esti = test_jsonFormat["mmr_estimate"]["estimate"]
        solo_mmr = test_jsonFormat["solo_competitive_rank"]
        team_mmr = test_jsonFormat["competitive_rank"]
        temp_list.append(mmr_esti)
        temp_list.append(solo_mmr)
        temp_list.append(team_mmr)
        temp_list.append(final_steamID_list[i])
        final_return.append(temp_list)
        # final_return format: [[player0_name,avatar,mmr_esti,solo_mmr,team_mmr,steamID],[player2...]]
        # name/avatar set to 0 if not exists
    return 'Success! Click button to update again!', final_return

def localStorage(mode,data):
    if mode=='read':
        try:
            x = open("local.txt").readlines()
        except Exception:
            x = ' '
    else: #write mode
        f = open('local.txt', 'w')
        f.write(data)  # python will convert \n to os.linesep
        f.close()
        x = True
    return x

def reqUserAvatar(picAdd):
    if picAdd == 0:
        picAdd = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg'
    else:
        pass
    data = urlopen(picAdd).read()
    return data

def updateHeroRanking(steamID):
    json_return = opendotaRequest(steamID, 'hero_ranking')
    test_jsonFormat = json.loads(json_return)
    final = sorted(test_jsonFormat, key=checkSortRanking, reverse=True)
    final = final[0:10]
    return final

def checkSortRanking(item):
    if item['win'] != 0:
        #true_value =  int(item['win'])/int(item['games'])
        true_value =  int(item['games'])
    else:
        true_value = 0
    return true_value

def heroid_dict():
	with open('heroes.json') as raw_heroid:
	    data = json.load(raw_heroid)

	#create new dictionary
	hero_to_id = {}
	id_to_hero = {}
	for ind_dict in data:
		#update 2 dictionaries based on imported json
		hero_to_id.update({ind_dict['localized_name']:ind_dict['id']})
		id_to_hero.update({ind_dict['id']:ind_dict['localized_name']})
	return hero_to_id, id_to_hero

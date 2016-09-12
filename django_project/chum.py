
"""
Matthew Meehan
Drew Siedel
June 14, 2015
"""

import requests
import lxml

#TODO: make a directory of rune and mastery ids to further reduce static API calls

#Constants
URL = {'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}', 'staticBase': 'https://global.api.pvp.net/api/lol/static-data/{region}/{url}', 'summonerName': 'v{version}/summoner/by-name/{names}', 'gameList': 'v{version}/game/by-summoner/{summonerId}/recent', 'currentGame': 'https://{proxy}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}', 'rankedStats': 'v{version}/stats/by-summoner/{summonerId}/ranked', 'getChampion': 'v{version}/{type}/{championId}', 'getRune': 'v{version}/{type}/{runeId}', 'getMastery': 'v{version}/{type}/{masteryId}'}


REGIONS = {'north_america': 'na'}
PLATFORMIDS = {'north_america': 'NA1'}
SEASONS = {'currentSeason': 'SEASON2015'}

CHAMPIONS_BY_ID = {1:'Annie',2:'Olaf',3:'Galio',4:'Twisted Fate',5:'Xin Zhao',6:'Urgot',7:'LeBlanc',8:'Vladimir',9:'Fiddlesticks',10:'Kayle',11:'Master Yi',12:'Alistar',13:'Ryze',14:'Sion',15:'Sivir',16:'Soraka',17:'Teemo',18:'Tristana',19:'Warwick',20:'Nunu',21:'Miss Fortune',22:'Ashe',23:'Tryndamere',24:'Jax',25:'Morgana',26:'Zilean',27:'Singed',28:'Evelynn',29:'Twitch',30:'Karthus',31:'Cho\'Gath',32:'Amumu',33:'Rammus',34:'Anivia',35:'Shaco',36:'Dr. Mundo',37:'Sona',38:'Kassadin',39:'Irelia',40:'Janna',41:'Gangplank',42:'Corki',43:'Karma',44:'Taric',45:'Veigar',48:'Trundle',50:'Swain',51:'Caitlyn',53:'Blitzcrank',54:'Malphite',55:'Katarina',56:'Nocturne',57:'Maokai',58:'Renekton',59:'Jarvan IV',60:'Elise',61:'Orianna',62:'Wukong',63:'Brand',64:'Lee Sin',67:'Vayne',68:'Rumble',69:'Cassiopeia',72:'Skarner',74:'Heimerdinger',75:'Nasus',76:'Nidalee',77:'Udyr',78:'Poppy',79:'Gragas',80:'Pantheon',81:'Ezreal',82:'Mordekaiser',83:'Yorick',84:'Akali',85:'Kennen',86:'Garen',89:'Leona',90:'Malzahar',91:'Talon',92:'Riven',96:'Kog\'Maw',98:'Shen',99:'Lux',101:'Xerath',102:'Shyvana',103:'Ahri',104:'Graves',105:'Fizz',106:'Volibear',107:'Rengar',110:'Varus',111:'Nautilus',112:'Viktor',113:'Sejuani',114:'Fiora',115:'Ziggs',117:'Lulu',119:'Draven',120:'Hecarim',121:'Kha\'Zix',122:'Darius',126:'Jayce',127:'Lissandra',131:'Diana',133:'Quinn',134:'Syndra',143:'Zyra',150:'Gnar',154:'Zac',157:'Yasuo',161:'Vel\'Koz',201:'Braum',222:'Jinx',236:'Lucian',238:'Zed',245:'Ekko',254:'Vi',266:'Aatrox',267:'Nami',268:'Azir',412:'Thresh',421:'Rek\'Sai',429:'Kalista',432:'Bard', 92:'Tahm Kench'}
#dict of all champion names by their championId. Significantly speeds up program by removing freqeunt API calls through getChampion (each time a name is required from an ID)


class API(object):

    #Constructor for the API
    def __init__(self, key, region):
        self.key = key;
        self.region = region;

    def sendBaseRequest(self, api_url, params):
        if params is None:
            params = {}
        args = {'api_key': self.key}


        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.api.get(URL['base'].format(proxy=self.region,region=self.region,url=api_url),params=args)

        if response.status_code == 200:  #good response (user is in game)
            return response.json()

    #All static data (champions, summoner spells, runes, etc. use the 'staticBase'.
    #Use getChampion as reference for future variation
    def sendStaticBaseRequest(self, api_url, params):
        if params is None:
            params = {}
        args = {'api_key': self.key}


        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.api.get(URL['staticBase'].format(region=self.region,url=api_url),params=args)


        if response.status_code == 200:
            return response.json()
        else:
            return []


    #For all requests that do not use the 'base' or 'staticBase'. requestType is an string to specify which base to use. (Ex. 'currentGame' = currentGame request)
    def sendRequest(self, requestType, summonerID, params={}):
        args = {'api_key': self.key}


        for key, value in params.items():
            if key not in args:
                args[key] = value

        if(requestType is 'currentGame'):
            response = requests.api.get(URL['currentGame'].format(proxy=self.region, platformId=PLATFORMIDS['north_america'],summonerId=summonerID), params=args)


        if response.status_code == 200: 
            return response.json()
        else:
            return []

    #return json object with summoner
    def getSummoner(self, name):
        current_version = '1.4'

        api_url = URL['summonerName'].format(version=current_version,names=name)

        return self.sendBaseRequest(api_url, None)

    #returns the ten most recent games by the summoner with name "name"
    def getGames(self, name):
        current_version = '1.3'

        #format name to have no spaces and all lowercase letter
        name = name.replace(' ', '')
        name = name.lower()

        summoner = self.getSummoner(name) #get the summoner 

        summ_id = (summoner[name])['id']  #get the id from the summoner

        api_url = URL['gameList'].format(version=current_version,summonerId=summ_id) #make url including id to get game

        result = self.sendBaseRequest(api_url, None)

        return result

    #calls getGames and returns the first game from that list (most recent)
    def getLastGame(self, name):
        gameList = self.getGames(name)
        lastGame = (gameList['games'])[0]

        return lastGame

    #gets the game that summoner with name "name" is currently in
    def getCurrentGame(self, name):
        # current_version = '1.0' #irrelevant for this one
        formatted_name = name.replace(' ', '').lower()

        summoner = self.getSummoner(name)

        if summoner != None:
            summ_id = (summoner[formatted_name])['id']
            return self.sendRequest('currentGame', summ_id)
        else:
            return []

    #Returns ranked stats for summoner with 'name'
    def rankedStats(self, name):
        current_version = '1.3'
        season = SEASONS['currentSeason']
        params = {'season': season}

        summoner = self.getSummoner(name)
        summ_id = (summoner[name])['id']

        api_url = URL['rankedStats'].format(version=current_version,summonerId=summ_id)

        return self.sendBaseRequest(api_url, params)

    #Returns a champion based on the 'championId'
    def getChampion(self, championId):
        current_version = '1.2'

        api_url = URL['getChampion'].format(version=current_version, type='champion', championId=championId)

        return self.sendStaticBaseRequest(api_url, None)

    #returns data about a rune based on its runeId
    def getRune(self, runeId):
        current_version = '1.2'

        api_url = URL['getRune'].format(version=current_version,type='rune',runeId=runeId)

        return self.sendStaticBaseRequest(api_url, None)

    #returns data about a mastery based on its id
    def getMastery(self, masteryId):
        current_version = '1.2'

        api_url = URL['getMastery'].format(version=current_version,type='mastery',masteryId=masteryId)

        return self.sendStaticBaseRequest(api_url, None)

    #mostly a functino for testing getRune and getMastery
    #
    def allRunesAndMasteries(self, game):
        for i in range (0,10):
            print "\n"
            summoner = (game['participants'])[i]
            summonerName = summoner['summonerName']
            summonerChampion = (self.getChampion(summoner['championId']))['name']

            print summonerName
            print summonerChampion

            print 'Runes:'
            runes = summoner['runes']
            for rune in runes:
                rune_object = self.getRune(rune['runeId'])
                rune_name = rune_object['name']
                rune_count = rune['count']
                print rune_name, 'x', rune_count

            print "Masteries:"
            masteries = summoner['masteries']
            for mastery in masteries:
                mastery_object = self.getMastery(mastery['masteryId'])
                mastery_name = mastery_object['name']
                print mastery_name


    #gives all relevant information about a summoner currently in a game
    #most likely used to scout an enemy in your game
    def getEnemyData(self, name):
    	enemy = {}
        game = self.getCurrentGame(name)
        name = name.replace(' ', '').lower()
	data = {}

	if game != []:
		data['in_game'] = True
		participants = game['participants']
		data['participants'] = participants
		
		for summoner in participants:
			formatted_summ = summoner['summonerName'].replace(' ', '').lower()
			formatted_name = name.replace(' ', '').lower()
                	if formatted_summ == formatted_name:
                    		enemy = summoner
		
		enemy_champ = self.getChampion(enemy['championId'])
            	champ_name = enemy_champ['name']
            	enemy_runes = enemy['runes']
            	enemy_masteries = enemy['masteries']

        	ranked_data = self.rankedStats(name)
 	        champList = ranked_data['champions']  #look at their champion stats

		data['name'] = name
		data['champion'] = champ_name
		data['champTitle'] = enemy_champ['title']
		
		found_champ = False

		for champion in champList:
			champ_id = champion['id']
			
			if champ_id in CHAMPIONS_BY_ID:
				this_champ = CHAMPIONS_BY_ID[champ_id] #current champion		
			else:
				this_champ = self.getChampion(champ_id) #cover our ass if champ list is not up to date

			if this_champ == champ_name:  #find the stats for champ they're currently playing 
                    		found_champ = True
                    		stats = champion['stats']
                    		number_of_games   = stats['totalSessionsPlayed']
                    		number_of_kills   = stats['totalChampionKills']
                 		number_of_deaths  = stats['totalDeathsPerSession'] #inaccurate name, shame on you rito
                		number_of_assists = stats['totalAssists']
                    		data['minions_slain']   = stats['totalMinionKills']
                    		data['wins']            = stats['totalSessionsWon']
                    		data['losses']          = stats['totalSessionsLost']

				data['average_kills']   = "{:10.2f}".format((float(number_of_kills)/float(number_of_games)))
				data['average_deaths']  = "{:10.2f}".format((float(number_of_deaths)/float(number_of_games)))
				data['average_assists'] = "{:10.2f}".format((float(number_of_assists)/float(number_of_games)))


		if not found_champ:
			data['found_champ'] = False
		else:
			data['found_champ'] = True

	else:	
		data['in_game'] = False

	return data

    def getTeamData(self, name):
	game = self.getEnemyData(name)
	name = name.replace(' ', '').lower()

	#data: a full game data collection sorted by summoner
	data = {}

	#Counter for reference
	i = 0

	if game != [] and 'participants' in game:
		data['game'] = game
		participants = game['participants']

            	for summoner in participants:
                	i += 1
                	#formatted_summ = summoner['summonerName'].replace(' ', '').lower()
               		#formatted_name = name.replace(' ', '').lower()

                	#Take each key into account
                	nameKey = "s" + str(i)

                	#Find the champion each summoner is playing
			champ_id = summoner['championId']
               		champ = self.getChampion(champ_id)

                	#Grab each champion's name
                	champ_name = champ['name']

                	#Grab each summoner's runes and masteries
                	runes = summoner['runes']
                	masteries = summoner['masteries']

                	#Reserve a spot for each summoner by name
                	data[nameKey] = {}

                	#Accessing names
                	data[nameKey]['name'] = summoner['summonerName']

                	#champion currently being played
                	data[nameKey]['champion'] = champ_name
			if self.rankedStats is not None:
				ranked_stats = self.rankedStats(summoner['summonerName'].lower().replace(' ', ''))
			else:
				ranked_stats = 0

			champ_list = ranked_stats['champions']

			data[nameKey]['wins'] = 0 #default values, if they have not played in ranked with this champ$
			data[nameKey]['losses'] = 0 		
			data[nameKey]['averageKills'] = 0
			data[nameKey]['averageDeaths'] = 0
			data[nameKey]['averageAssists'] = 0
			data[nameKey]['averageCS'] = 0
			data[nameKey]['chumScore'] = 101

			for champion in champ_list:
				if champion['id'] == champ_id:
					champ_stats = champion['stats']

					wins = champ_stats['totalSessionsWon'] 
					losses = champ_stats['totalSessionsLost']
					kills = champ_stats['totalChampionKills']
					deaths = champ_stats['totalDeathsPerSession']
					assists = champ_stats['totalAssists']
					creeps = champ_stats['totalMinionKills']
					games = champ_stats['totalSessionsPlayed']

					data[nameKey]['wins'] = wins
					data[nameKey]['losses'] = losses
					data[nameKey]['averageKills'] = "{:10.1f}".format(float(kills)/float(games))
					data[nameKey]['averageDeaths'] = "{:10.1f}".format(float(deaths)/float(games))
					data[nameKey]['averageAssists'] = "{:10.1f}".format(float(assists)/float(games))
					data[nameKey]['averageCS'] = "{:10.1f}".format(float(creeps)/float(games))


					if (wins+losses) >= 5:
						data[nameKey]['chumScore'] = self.calculateChumScore(wins, losses, games, kills, deaths, assists, champ_name)
					else:	
						data[nameKey]['chumScore'] = 101 #impossible value, indicates cannot calculate						

					break #found champion, stop searching 


	return data


    #this shit's proprietary 
    def calculateChumScore(self, wins, losses, games, kills, deaths, assists, champ_id):
	winrate = float(wins)/float(games)
	average_kills = float(kills)/float(games)
	average_deaths = float(deaths)/float(games)
	average_assists = float(assists)/float(games)

	if average_deaths == 0: #can't have a divide by zero
		average_deaths == 1

	adjusted_kda = (float(average_kills) + (.65)*float(average_assists))/float(average_deaths)
	adjusted_kda = float(adjusted_kda)/100

	average_winrate = 0.5

	chum_score = 100 * (float(average_winrate) + (float(winrate-average_winrate)) + 1.2*float(adjusted_kda))
	chum_score = "{:10.1f}".format(chum_score)

	return chum_score










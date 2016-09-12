from django.http import HttpResponse
from django.shortcuts import render
from .forms import summonerForm

import chum

# Create your views here.
def index(request):
	return render(request, 'template.html')	


def summoner(request):
	#myAPI = chum.API('22096322-01cc-4aff-aee0-dd306ccd5a9d', chum.REGIONS['north_america'])
	myAPI = chum.API('4f8ba090-4f5a-44b0-92f2-9a86b17e1b5c', chum.REGIONS['north_america']) 

	summ_name = request.GET.get('q', '~') #get URL argument. if none, name is '~'

	if summ_name == '~': #found page without summoner
		return HttpResponse("<html><body>Try <a href='http://chumthewaters.net'>this</a> to search for a summoner</body></html>")



        team_data = myAPI.getTeamData(summ_name)

	if not 'game' in team_data:
		return HttpResponse("<html><body>%s is not in a game, or could not find a summoner named %s<h1><a href ='http://chumthewaters.net'>Try another summoner?</a></h1></body></html>" % (summ_name, summ_name))

	enemy_data = team_data['game']

	champ_name = enemy_data['champion'] #regular champ name (not formatted for url)

	url_champ = enemy_data['champion'].replace(' ', '').replace('.', '') #format for url, including annoying change for rek'sai and kha
	if "'" in url_champ:
		url_champ = url_champ.replace("'", "").lower().title()



	#A list of dictionaries containing summoner data, with each sublist having keys 'name', 'champion'
	summ1_list = []
	summ2_list = [] #same for other team

	for i in range(1, 11):
		index = "s{num}".format(num=i) #s1, s2, etc

		summoner = {}

		summoner['name'] = team_data[index]['name']
		summoner['wins'] = team_data[index]['wins']
		summoner['losses'] = team_data[index]['losses']
		summoner['kills'] = team_data[index]['averageKills']
		summoner['deaths'] = team_data[index]['averageDeaths']
		summoner['assists'] = team_data[index]['averageAssists']
		summoner['cs'] = team_data[index]['averageCS']

		chum_score = team_data[index]['chumScore']
		summoner['chumScore'] = chum_score


		#consider replacing in the future with a round() statement
		fish_val = 0
		round_chum = int(float(chum_score)) #cannot cast int directly on formatted float
		if round_chum != 0 and round_chum <= 100:
			fish_val = round_chum #get first digit, and multiply by ten (ie 35 -> 3x10 = 30)
			fish_val = str(fish_val)
			fish_val = fish_val[0]
			fish_val = int(fish_val)
			fish_val *= 10
		if round_chum == 100:	
			fish_val = 100
 
		summoner['fishValue'] = fish_val
		

		#begin the process of properly formatting champ name for display

		champion = team_data[index]['champion'].replace(' ', '').replace('.', '')

		if "'" in champion:
			champion = champion.replace("'", "").lower()  #for stupidass khazix
			champion = champion.title()
	
		if champion == "LeBlanc":
			champion = "Leblanc" #stupidass leblanc :/

		if champion == "Kogmaw":
			champion = "KogMaw" #hurray for consistency

		if champion == "Wukong":
			champion = "MonkeyKing" #lolwut

		if champion == "Fiddlesticks":
			champion = "FiddleSticks"

		if champion == "Reksai":
			champion = "RekSai" #getting sick of these formatting exceptions

		summoner['champion'] = champion

		if i < 6:
			summ1_list.append(summoner)
		else:
			summ2_list.append(summoner)

        return render(request,'summ_template.html', {'ddragon_version': '5.13.1', 'summ_name': summ_name, 'in_game':enemy_data['in_game'], 'champ_name': champ_name, 'url_champ': url_champ, 'champ_title':enemy_data['champTitle'], 'summ1_list':summ1_list, 'summ2_list':summ2_list})

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

def chumscore(request):
	return render(request, 'chumscore.html')

#required to have application approved by rito
def riot(request):
	return render(request, 'riot.txt')


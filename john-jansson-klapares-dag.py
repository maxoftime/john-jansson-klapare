import apikey
import os
import pprint
import requests

pp = pprint.PrettyPrinter(indent=2)
apiKey = os.environ['ES_APIKEY']

id_1997 = '44255,'
id_1998 = '44254,'
id_1999 = '1719,'
id_2000 = '2752,'
id_2001 = '3863,'
id_2002 = '5307,'
id_2003 = '6469,'
id_2004 = '8051,'
id_2005 = '9402,'
id_2006 = '10581,'
id_2007 = '21511,'
id_2008 = '27773,'
id_2009 = '32911,'
id_2010 = '38686,'
id_2011 = '44165,'
id_2012 = '51603,'
id_2013 = '57973,'
id_2014 = '63925,'
id_2015 = '69620,'
id_2016 = '73163'

year_list = id_1997 + id_1998 + id_1999 + id_2000 + id_2001 + id_2002 + id_2003 + id_2004 + id_2005 + id_2006 + id_2007 + id_2008 + id_2009 + id_2010 + id_2011 + id_2012 + id_2013 + id_2014 + id_2015 + id_2016
round_list = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30'
team_id_list = '9367, 9368'

all_the_data_url = 'http://api.everysport.com/v1/events?apikey='+ str(apiKey) + '&league=' + year_list + '&team=' + team_id_list + '&round=' + round_list + '&limit=1000'
#print(all_the_data_url)
all_the_data = requests.get(all_the_data_url)
all_the_data = all_the_data.json()

all_events = all_the_data['events']

def year_lister(events):
  year = 0
  for event in events:
    if event['startDate'][0:4] != year:
      year = event['startDate'][0:4]
      

def get_events_one_year(events, year):
  all_events_one_year = []
  for event in events:
    if (event['startDate'][0:4] == year):
      all_events_one_year.append(event)
  return all_events_one_year


def add_points(events, team):
  team_points = 0
  points_per_round = []
  i = 1
  for event in events:
    if (event['homeTeam']['shortName'].encode('utf-8') == team) and (event['homeTeamScore'] > event['visitingTeamScore']):
      team_points += 3
      points_per_round.append(('omg ' + str(i), team_points))
      i += 1
    
    elif (event['homeTeam']['shortName'].encode('utf-8') == team) and (event['homeTeamScore'] == event['visitingTeamScore']):
      team_points += 1
      points_per_round.append(('omg ' + str(i), team_points))
      i += 1

    elif (event['homeTeam']['shortName'].encode('utf-8') == team) and (event['homeTeamScore'] < event['visitingTeamScore']):
      points_per_round.append(('omg ' + str(i), team_points))
      i += 1

    elif (event['visitingTeam']['shortName'].encode('utf-8') == team) and (event['visitingTeamScore'] > event['homeTeamScore']):
      team_points += 3
      points_per_round.append(('omg ' + str(i), team_points))
      i += 1

    elif (event['visitingTeam']['shortName'].encode('utf-8') == team) and (event['visitingTeamScore'] == event['homeTeamScore']):
      team_points += 1
      points_per_round.append(('omg ' + str(i), team_points))
      i += 1

    elif (event['visitingTeam']['shortName'].encode('utf-8') == team) and (event['visitingTeamScore'] < event['homeTeamScore']):
      points_per_round.append(('omg ' + str(i), team_points))
      i += 1

    else:
      continue    
    
  return points_per_round

AIK_points_2015 = add_points(get_events_one_year(all_events, '2015'), 'AIK')
DIF_points_2015 = add_points(get_events_one_year(all_events, '2015'), 'Djurgården')

single_rounds = 0
while single_rounds <= 29:
  print(AIK_points_2015[single_rounds][1])
  single_rounds += 1


#pp.pprint(DIF_points_2015)

#add_points(all_events_2008, 'Djurgården')
#print('Vid slutet av säsongen har ' + team  + str(team_points) + ' poäng.')

#allsvenskan_year = allsvenskan['startDate'] [0:4]

#total_rounds = 30
#possible_points_left = 3 * total_rounds

##pp.pprint(total_rounds_this_year)
 #pp.pprint(total_rounds_this_year['events'][0]['round'])
 ##the_current_round = total_rounds_this_year.content
 #the_actual_nr_of_rounds = total_rounds_this_year['events'][0]['round']
 #the_actual_nr_of_rounds_left = the_actual_nr_of_rounds
 #game_round = 1
 #while game_round <= the_actual_nr_of_rounds:
 #  time.sleep(0.5)
 #  allsvenskan_table = es.get_standings(current_year_id, game_round, 'total')
 #  #print('\nOmgång ' + str(game_round))
 #  for teams in allsvenskan_table[0]['standings']:
 #    team_name = teams['team']['shortName'].encode('utf-8')
 #    if team_name == 'AIK':
 #      p_AIK = int(teams['stats'][7]['value'])
 #      #print(team_name + ' har ' + str(p_AIK) + ' poäng.')
 #
 #    elif team_name == 'Djurgårdens IF':
 #      p_DIF = int(teams['stats'][7]['value'])
 #      #print(team_name + ' har ' + str(p_DIF) + ' poäng.')
 #    
 #  game_round += 1
 #  print(game_round)
 #  the_actual_nr_of_rounds_left -= 1
 #  possible_points_left = 3 * the_actual_nr_of_rounds_left
 #  point_difference = p_AIK - p_DIF
 #  if point_difference > possible_points_left:
 #    print('här?')
 #    #print('John Jansson klåpares dag infaller den här omgången')
 #    time.sleep(0.5)
 #    allsvenskan_rounds_date = es.events.leagues(current_year_id)
 #    for all_rounds in allsvenskan_rounds_date:
 #      #pp.pprint(all_rounds)
 #      if all_rounds['round'] == game_round:
 #        if all_rounds['visitingTeam']['shortName'].encode('utf-8') == 'Djurgårdens IF' or all_rounds['homeTeam']['shortName'].encode('utf-8') == 'Djurgårdens IF':
 #          #print('Skriver till fil...')
 #          file = open('collection.txt', 'a')
 #          #file.write('\n--------------\n' + allsvenskan['shortName'] + ' ' + allsvenskan_year)
 #          file.write('\nOmgång ' + str(game_round) + '\n')
 #          file.write(all_rounds['startDate']  + '\n--------------\n')
 #          file.close()
 #          #print('Klart!')
 #          break
 #        else:
 #          #print('no no no...')
 #          continue
 #          
 #        #pp.pprint(all_rounds)
 #        #print(all_rounds['startDate'])
 #        #print(all_rounds['visitingTeam']['shortName'].encode('utf-8'))
 #        #print('\n')
 #    break
 #  else:
 #    continue
 #



print('\n--------------\nProvided by Everysport.com')
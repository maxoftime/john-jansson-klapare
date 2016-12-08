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

year_id_list = id_1997 + id_1998 + id_1999 + id_2000 + id_2001 + id_2002 + id_2003 + id_2004 + id_2005 + id_2006 + id_2007 + id_2008 + id_2009 + id_2010 + id_2011 + id_2012 + id_2013 + id_2014 + id_2015 + id_2016
round_list = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30'
team_id_list = '9367, 9368'

all_the_data_url = 'http://api.everysport.com/v1/events?apikey=' + str(apiKey) + '&league=' + year_id_list + '&team=' + team_id_list + '&round=' + round_list + '&limit=1000'
all_the_data = requests.get(all_the_data_url)
all_the_data = all_the_data.json()
all_events = all_the_data['events']

#print(all_the_data_url)

def year_lister(events):
  year = 0
  
  years_list = []
  i = 0
  for event in events:
    if event['startDate'][0:4] != year:
      year = event['startDate'][0:4]
      years_list.append(year)
      i += 1
  return years_list


def get_all_events_one_year(events, year):
  '''
  Input in events should preferably be the the response (in this case all_events).
  And also a year between 1999 and 2016 as a string.

  '''
  all_events_one_year = []
  for event in events:
    if (event['startDate'][0:4] == year):
      all_events_one_year.append(event)
  return all_events_one_year


def get_team_events_one_year(events, team):
  '''
  Input in events should preferably be the return from get_all_events_one_year().

  '''
  team_events_one_year = []
  for event in events:
    if (event['homeTeam']['shortName'].encode('utf-8') == team or event['visitingTeam']['shortName'].encode('utf-8') == team):
      team_events_one_year.append(event)
  return team_events_one_year


def get_total_rounds(events):
  '''
  Input in events should preferably be the return from get_team_events_one_year().

  '''
  total_rounds = len(events)
  return total_rounds


def add_points(events, team): 
  '''
  Input in events should preferably be the return from get_team_events_one_year().

  '''
  team_points = 0
  points_per_round = []
  i = 1
  for event in events:
    if (event['homeTeam']['shortName'].encode('utf-8') == team and (event['homeTeamScore'] > event['visitingTeamScore'])):
      team_points += 3
      points_per_round.append((i, team_points))
      i += 1
    
    elif ((event['homeTeam']['shortName'].encode('utf-8') == team) and (event['homeTeamScore'] == event['visitingTeamScore'])):
      team_points += 1
      points_per_round.append((i, team_points))
      i += 1

    elif ((event['homeTeam']['shortName'].encode('utf-8') == team) and (event['homeTeamScore'] < event['visitingTeamScore'])):
      points_per_round.append((i, team_points))
      i += 1

    elif ((event['visitingTeam']['shortName'].encode('utf-8') == team) and (event['visitingTeamScore'] > event['homeTeamScore'])):
      team_points += 3
      points_per_round.append((i, team_points))
      i += 1

    elif ((event['visitingTeam']['shortName'].encode('utf-8') == team) and (event['visitingTeamScore'] == event['homeTeamScore'])):
      team_points += 1
      points_per_round.append((i, team_points))
      i += 1

    elif ((event['visitingTeam']['shortName'].encode('utf-8') == team) and (event['visitingTeamScore'] < event['homeTeamScore'])):
      points_per_round.append((i, team_points))
      i += 1

    else:
      continue    
    
  return points_per_round



def compare(team_one, team_two, year):
  the_year = get_all_events_one_year(all_events, year)
  
  AIK = get_team_events_one_year(the_year, team_one)
  if AIK == []:
    print('Endast Djurgården spelade i Allsvenskan ' + str(the_year[0]['startDate'][0:4]) + '.')
    return
  else:
    AIK_points = add_points(AIK, team_one)
    all_rounds = len(AIK_points)
    rounds_left = len(AIK_points)
  
  DIF = get_team_events_one_year(the_year, team_two)
  if DIF == []:
    print('Endast AIK spelade i Allsvenskan ' + str(the_year[0]['startDate'][0:4]) + '.')
    return
  else:
     DIF_points = add_points(DIF, team_two)

  
  actual_round = 0

  while actual_round < all_rounds:
    possible_points_left = rounds_left * 3
    point_difference = AIK_points[actual_round][1] - DIF_points[actual_round][1]
    rounds_left -= 1

    #print('Omgång ' + str(actual_round + 1))
    #print(str(possible_points_left) + ' poäng kvar.')
    #print('AIKs poäng efter denna runda: ' + str(AIK_points[actual_round][1]))
    #print('DIFs poäng efter denna runda: ' + str(DIF_points[actual_round][1]))

    if point_difference > possible_points_left:
      the_date = DIF[actual_round]['startDate']
      

      # %-d %B %Y datum månad år. .strftime
      print('John Jansson Klåpares dag inträffade i runda ' +  str(actual_round) + ' på datumet ' + str(the_date[:10]))
      return the_date

    elif rounds_left == 0 and point_difference <= possible_points_left:
      has_not_happened = 'John Jansson Klåpares dag inträffade aldrig ' + str(DIF[actual_round]['startDate'][:4])
      print(has_not_happened)
      return (has_not_happened)

    actual_round += 1

all_years_list = year_lister(all_events)

for year in all_years_list:
  compare('AIK', 'Djurgården', year)


print('\n--------------\nProvided by Everysport.com')
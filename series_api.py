from  tabulate import tabulate
import requests
class series:
    def __init__(self,headers,config_data):
        self.filt_dict= {}
        self.choice=''
        self.sid=[]
        self.headers=headers
        self.series_id=0
        self.config=config_data
    def series_list(self):
        while True:
            end=input('Do you want to know about sereis list details (y/n):')
            if end=='y':
                while True:
                    self.filt_dict=self.config.get('series_list_dic')
                    print('Select any one of the match type')
                    for key, val in self.filt_dict.items():
                        print(f'{key} | {val}')
                    self.choice = int(input("Enter your choice : "))
                    if self.choice in self.filt_dict.keys():
                        break
                    else:
                        print('selected option not in the provided options list. Please select again..!')

                table = []
                table_list = self.config.get('series_list_headers')
                url=self.config.get('series_list_url')
                url+=self.filt_dict.get(self.choice)
                response=requests.get(url,headers=self.headers)
                if response.status_code == 200:
                    var=response.json()
                    data = var.get("seriesMapProto")
                    for i in data:
                        date = i.get('date')
                        for j in i.get('series'):
                            table.append([j['id'], date, j.get('name'), j.get('startDt'), j.get('endDt')])
                    print(tabulate(table, headers=table_list, tablefmt='pretty'))
                    break
                else:
                    print('No Data found..!')
                    break
            elif end == 'n':break
            else:print('you selected invalid option try again')
    def series_archives(self):

                while True:
                    self.filt_dict = self.config.get('series_list_dic')
                    print('Select any one of the match type for archives')
                    for key, val in self.filt_dict.items():
                        print(f'{key} | {val}')
                    self.choice = int(input("Enter your choice : "))
                    if self.choice in self.filt_dict.keys():
                        break
                    else:
                        print('selected option not in the provided options list. Please select again..!')
                while True:
                    url = self.config.get('series_archives_url')
                    url += self.filt_dict.get(self.choice)
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        var = response.json()
                        table_archives = []
                        series = var['seriesMapProto']
                        for i in series:
                            date = i.get('date')
                            for j in i.get('series'):
                                self.sid.append(j.get('id'))
                                table_archives.append([date, j.get('id'), j.get('name'), j.get('startDt'), j.get('endDt')])
                        print(tabulate(table_archives, headers=self.config.get('series_archives_headers'), tablefmt='pretty'))
                        while True:
                            try:
                                self.series_id=int(input('enter the id using above archives data: '))
                                if self.series_id in self.sid:
                                    break
                                else:print('invalid input,try again')
                            except Exception:print('only digits are allowed,please enter again')
                        break
                    else:
                        print('No Data found..!')
                        break



    def series_matches(self):
        while True:
            end = input('do you want to enter series matches details(y/n): ')
            if end == 'y':

                def trim_lines(text, char):
                    lines = ""
                    for i in range(0, len(text), char):
                        lines = lines + text[i:i + char] + "\n"
                    return lines

                table_list = self.config.get('series_matches_headers')

                url = self.config.get('series_matches_url')
                url += f"{self.series_id}"
                response=requests.get(url,headers=self.headers)

                if response.status_code == 200:
                    var=response.json()
                    matches = var.get('matchDetails')
                    table = []
                    for match in matches:
                        if 'matchDetailsMap' in match:
                            date = match.get('matchDetailsMap').get('key')
                            match_info = match.get('matchDetailsMap').get('match')
                            for details in match_info:
                                dt = details.get('matchInfo')
                                ms = details.get('matchScore')
                                matchid = dt.get('matchId')
                                seriesid = dt.get('seriesId')
                                seriesname = dt.get('seriesName')
                                matchformat = dt.get('matchFormat')
                                startdate = dt.get('startDate')
                                enddate = dt.get('endDate')
                                state = dt.get('state')
                                team1 = dt.get('team1').get('teamName')
                                team2 = dt.get('team2').get('teamName')
                                ground = dt.get('venueInfo').get('ground')
                                team1score, team2score = "", ""
                                try:
                                    scores_data1 = ms.get('team1Score')
                                    scores_data2 = ms.get('team2Score')
                                    for i in range(1, len(scores_data1.keys()) + 1):
                                        scores = scores_data1[f"inngs{i}"]
                                        team1score += f"inngs{i}:-- runs:-{scores.get('runs')},wickets:-{scores.get('wickets')},overs:-{scores.get('overs')}"
                                    for j in range(1, len(scores_data2.keys()) + 1):
                                        scores = scores_data2[f"inngs{j}"]
                                        team2score += f"inngs{j}:-- runs:-{scores.get('runs')},wickets:-{scores.get('wickets')},overs:-{scores.get('overs')}"
                                except Exception:
                                    team1score='No Data '
                                    team2score='No Data'
                                table.append(
                                    [trim_lines(date, 7), matchid, seriesid, trim_lines(seriesname, 5), matchformat, startdate,
                                     enddate, state, trim_lines(team1, 5), trim_lines(team2, 5), trim_lines(ground,5),
                                     trim_lines(team1score, 5), trim_lines(team2score, 5)])
                    print(tabulate(table, headers=table_list, tablefmt='pretty'))
                    break
                else:
                    print('No Data found..!')
                    break
            elif end == 'n':
                break
            else:
                print('you selected invalid option try again')
    def series_news(self):
        while True:
            end=input('do you want to enter series news details(y/n): ')
            if end == 'y':
                url=self.config.get('series_news_url')
                url += f"{self.series_id}"
                response = requests.get(url, headers=self.headers)
                if response.status_code==200:
                    var = response.json()
                    def trim_lines(text, char):
                        lines = ""
                        for i in range(0, len(text), char):
                            lines += text[i:i + char] + '\n'
                        return lines

                    table_list = self.config.get('series_news_headers')
                    table = []
                    for i in var.get('storyList'):
                        if 'story' in i:
                            st = i.get('story')
                            id = st.get('id')
                            headline = st.get('hline')
                            introduction = st.get('intro')
                            publishtime = st.get('pubTime')
                            source = st.get('source')
                            storytype = st.get('storyType')
                            seoheadline = st.get('seoHeadline')
                            context = st.get('context')
                            table.append(
                                [id, trim_lines(headline, 10), trim_lines(introduction, 15), publishtime, source, storytype,
                                 trim_lines(seoheadline, 10), trim_lines(context, 10)])
                    print(tabulate(table, headers=table_list, tablefmt='pretty'))
                    break
                else:
                    print('No Data found..!')
                    break
            elif end == 'n':break
            else:print('you selected invalid option try again')
    def series_squads(self):
        while True:
            end=input('do you want to enter series squads details(y/n): ')
            if end=='y':
                url = self.config.get('series_squads_url')
                url += f"{self.series_id}/squads"
                response = requests.get(url, headers=self.headers)
                if response.status_code==200:
                    var=response.json()
                    series_id = {}
                    count = 1
                    for i in var.get('squads'):
                        if i.get('squadId') is not None:
                            series_id[str(count)] = {'squadid': i.get('squadId'), 'squadtype': i.get('squadType')}
                            count += 1
                    for key, val in series_id.items():
                        print(f"{key} | {val['squadid']} | {val['squadtype']}")
                    while True:
                        ch = input('enter a your choice: ')
                        if ch in series_id.keys():
                            break
                        else:
                            print('you selected invalid option try again')
                    ch_val = series_id[ch]['squadid']
                else:
                    print('No Data found..!')
                    break

                def series_players():
                    while True:
                        end = input('do you want to enter series players details(y/n): ')
                        if end == 'y':
                            url = self.config.get('series_players_url')
                            url += f"{self.series_id}/squads/{ch_val}"
                            response = requests.get(url, headers=self.headers)
                            if response.status_code == 200:
                                var = response.json()
                                table = []
                                table_list = self.config.get('series_players_headers')
                                for players in var.get('player'):
                                    table.append(
                                        [players.get('id'), players.get('name'), players.get('role'),
                                         players.get('battingStyle'),
                                         players.get('bowlingStyle')])
                                print(tabulate(table, headers=table_list, tablefmt='pretty'))
                                break
                            else:
                                print('No Data found..!')
                                break
                        elif end == 'n':
                            break
                        else:
                            print('you selected invalid option try again')

                series_players()
                break
            elif end == 'n':
                break
            else:
                print('you entered invalid option try again')


    def series_venues(self):
        while True:
            end = input('do you want to enter series venue details(y/n): ')
            if end == 'y':
                url=self.config.get('series_venues_url')
                url += f"{self.series_id}/venues"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var=response.json()
                    table = []
                    table_venues = self.config.get('series_venues_headers')
                    for i in var.get('seriesVenue'):
                        table.append([i.get('ground'), i.get('city'), i.get('country')])
                    print(tabulate(table, tablefmt='pretty', headers=table_venues))
                    break
                else:
                    print('No Data found..!')
                    break
            elif end=='n':break
            else:print('you selected invalid option try again')

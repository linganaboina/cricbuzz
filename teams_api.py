from tabulate import tabulate
import requests
class teams:
    def __init__(self,headers,config_data):
        self.filt_dict={}
        self.choice=''
        self.headers=headers
        self.new_team_id=0
        self.config=config_data
    def teams_list(self):
        while True:
            self.filt_dict = self.config.get('teams_list_dic')
            print('Select any one of the match type')
            for key, val in self.filt_dict.items():
                print(f'{key} | {val}')
            self.choice = int(input("Enter your choice : "))
            if self.choice in self.filt_dict.keys():
                break
            else:
                print('selected option not in the provided options list. Please select again..!')
        table = []
        team_id = []
        url=self.config.get('teams_list_url')
        url+=f"{self.filt_dict.get(self.choice)}"
        response=requests.get(url,headers=self.headers)
        while True:
            if response.status_code==200:
                var=response.json()
                for data in var.get('list'):
                    table.append([data.get('teamId'), data.get('teamName')])
                    if data.get('teamId') not in team_id:
                        team_id.append(data.get('teamId'))
                print(tabulate(table, tablefmt='pretty', headers=self.config.get('teams_list_headers')))
                while True:
                    try:
                        self.new_team_id = int(input('enter teamid from above data: '))
                        if self.new_team_id in team_id:
                            break
                        else:print('invalid input teamid,try again')
                    except Exception:print('only digits are allowed,please enter a valid input')
                break
            else:
                print('No Data found..!')
                break
    def teams_schedules(self):
        while True:
            end = input('do you want to enter team schedules(y/n):')
            if end=='y':
                def trim_lines(text, char):
                    lines = ""
                    for i in range(0, len(text), char):
                        lines = lines + text[i:i + char] + "\n"
                    return lines

                table = []
                team_id = []
                head_list = self.config.get('teams_schedules_headers')

                url = self.config.get('teams_schedules_url')
                url+=f"{self.new_team_id}/schedule"
                response=requests.get(url,headers=self.headers)
                if response.status_code==200:
                    var=response.json()
                    for i in var.get('teamMatchesData'):
                        try:
                            mt_dt = i.get('matchDetailsMap')
                            key = mt_dt['key']
                            for j in mt_dt.get('match'):
                                data = j.get('matchInfo')
                                if (data.get('team1').get('teamId')) not in team_id:
                                    team_id.append(data.get('team1').get('teamId'))
                                elif (data.get('team2').get('teamId')) not in team_id:
                                    team_id.append(data.get('team2').get('teamId'))
                                table.append([data.get('seriesId'), trim_lines(data.get('seriesName'), 5), data.get('matchDesc'),
                                              data.get('startDate'), data.get('endDate'), trim_lines(data.get('status'), 5),
                                              trim_lines(data.get('team1').get('teamName'),5), data.get('team1').get('teamId'),
                                              trim_lines(data.get('team2').get('teamName'),5), data.get('team2').get('teamId'),
                                              trim_lines(data.get('venueInfo').get('ground'), 8), data.get('venueInfo').get('city'),
                                              data.get('venueInfo').get('timezone')])
                            break
                        except Exception:
                            pass
                    print(tabulate(table, tablefmt='pretty', headers=head_list))
                    break
                else:
                    print('No data found..!')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
    def teams_results(self):
        while True:
            end = input('do you want to enter team results(y/n):')
            if end == 'y':
                def trim_lines(text, char):
                    lines = ""
                    for i in range(0, len(text), char):
                        lines = lines + text[i:i + char] + "\n"
                    return lines

                table = []
                head_list = self.config.get('teams_results_headers')

                url = self.config.get('teams_results_url')
                url+=f"{self.new_team_id}/results"
                response = requests.get(url, headers=self.headers)
                if response.status_code==200:
                    var = response.json()
                    for i in var.get('teamMatchesData'):
                        try:
                            mt_dt = i.get('matchDetailsMap')
                            key = mt_dt['key']
                            for j in mt_dt.get('match'):
                                data = j.get('matchInfo')
                                for count in range(1, 3):
                                    runs = j.get('matchScore').get(f'team{count}Score').get('inngs1').get('runs')
                                    wickets = j.get('matchScore').get(f'team{count}Score').get('inngs1').get('wickets')
                                    overs = j.get('matchScore').get('team1Score').get('inngs1').get('overs')
                                    if count == 1:
                                        team1score = f"'runs':{runs}, 'wickets':{wickets}, 'overs':{overs}"
                                    else:
                                        team2score = f"'runs':{runs}, 'wickets':{wickets}, 'overs':{overs}"
                                table.append([trim_lines(data.get('seriesName'), 5),
                                              trim_lines(data.get('matchDesc'), 5), data.get('startDate'), data.get('endDate'),
                                              trim_lines(data.get('status'), 5), trim_lines(data.get('team1').get('teamName'),5),
                                              data.get('team1').get('teamId'),
                                              trim_lines(data.get('team2').get('teamName'),5), data.get('team2').get('teamId'),
                                              trim_lines(data.get('venueInfo').get('ground'), 5),
                                              data.get('venueInfo').get('city'), trim_lines(team1score, 7),
                                              trim_lines(team2score, 7)])


                        except Exception:
                            pass
                    print(tabulate(table, tablefmt='pretty', headers=head_list))
                    break

                else:
                    print('No data found..!')
                    break

            elif end=='n':break
            else:print('invalid input,try again')
    def teams_news(self):
        while True:
            end = input('do you want to enter team news(y/n):')
            if end == 'y':
                def trim_lines(text, char):
                    lines = ""
                    for i in range(0, len(text), char):
                        lines += text[i:i + char] + '\n'
                    return lines

                table_list = self.config.get('teams_news_headers')

                table = []
                url = self.config.get('teams_news_url')
                url+=f"{self.new_team_id}"
                response = requests.get(url, headers=self.headers)
                if response.status_code==200:
                    var = response.json()
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
                                [id, trim_lines(headline, 30), trim_lines(introduction, 25), publishtime, source, storytype,
                                 trim_lines(seoheadline, 25), trim_lines(context, 25)])
                    print(tabulate(table, headers=table_list, tablefmt='pretty'))
                    break
                else:
                    print('No data found..!')
                    break
            elif end == 'n':break
            else:print('invalid input,try again')
    def teams_players(self):
        while True:
            end = input('do you want to enter team playeres(y/n):')
            if end == 'y':
                table = []
                url = self.config.get('teams_players_url')
                url+=f"{self.new_team_id}/players"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var = response.json()
                    for i in var.get('player'):
                        try:
                            table.append([i.get('name'), i.get('battingStyle'), i.get('bowlingStyle')])
                        except Exception:
                            table.append([i.get('name'), None,i.get('battingStyle')])
                    print(tabulate(table,tablefmt='pretty',headers=self.config.get('teams_players_headers')))
                    break
                else:
                    print('No data found..!')
                    break
            elif end == 'n':break
            else:print('invalid input,try again')




from tabulate import  tabulate
import requests

class matches:

    def __init__(self,headers,config_data):
        self.mid=''
        self.filt_dict={}
        self.choice=''
        self.sid=''
        self.headers=headers
        self.config=config_data



    def matches_list(self):
        stats=self.config.get('matches_dic')
        for k,v in stats.items():
            print(f'{k}-{v}')
        while True:
            ch=int(input('enter your choice:'))
            if ch in stats.keys():
                break
            else:
                print('invalid selection try agian')

        url = self.config.get('matches_list_url')
        url+=stats.get(ch)
        response = requests.get(url, headers=self.headers)
        while True:
            if response.status_code == 200:
                data=response.json()
                filters_list = data.get('filters').get('matchType')
                numbers_list = [str(i) for i in range(1, len(filters_list)+1)]
                self.filt_dict = dict(zip(numbers_list, filters_list))
                print('Select any one of the match type')
                for key, val in self.filt_dict.items():
                    print(f'{key} | {val}')
                while True:
                    self.choice = input("Enter your choice : ")
                    status=False
                    if self.choice in self.filt_dict.keys():
                            for mt_type in data.get('typeMatches'):
                                if mt_type.get('matchType') == self.filt_dict.get(self.choice):
                                    status=True
                                    break
                                else:
                                    print('enter proper match type,try again')
                                    status=False
                            if status:break
                            else:continue
                    else:
                        print('enter a valid input, Please select again..!')

                team_id_list = []
                series_dict = {}
                for mt_type in data.get('typeMatches'):
                    if mt_type.get('matchType') == self.filt_dict.get(self.choice):
                        for sm in mt_type['seriesMatches']:
                            try: sm_data = sm['seriesAdWrapper']
                            except KeyError: pass
                            else:
                                match_dict = {}
                                for mtm in sm_data['matches']:
                                    mt = mtm.get('matchInfo')
                                    if (mt.get('team1').get('teamId')) not in team_id_list:
                                        team_id_list.append(mt.get('team1').get('teamId'))
                                    elif (mt.get('team2').get('teamId')) not in team_id_list:
                                        team_id_list.append(mt.get('team2').get('teamId'))
                                    else:
                                        break
                                    res,res1,res3,res4,res6,res5='','','','','',''
                                    try:
                                        ms_t1 = mtm['matchScore']['team1Score']['inngs1']
                                        res = ms_t1.get('runs')
                                        res1 = ms_t1.get('wickets')
                                        res3 = ms_t1.get('overs')
                                    except KeyError:
                                        ms_t1 = 'No Info'
                                    try:
                                        ms_t2 = mtm['matchScore']['team2Score']['inngs1']
                                        res4 = ms_t2.get('runs')
                                        res5 = ms_t2.get('wickets')
                                        res6 = ms_t2.get('overs')
                                    except KeyError: ms_t2 = 'No Info'
                                    match_dict[mt['matchId']] = {'match_desc': mt.get('matchDesc'), 'match_format': mt.get('matchFormat'),
                                                                 'start_dt': mt.get('startDate'), 'end_dt': mt.get('endDate'),
                                                                 'state': mt.get('state'), 'status': mt.get('status'),
                                                                 'teams': [mt.get('team1').get('teamName'), mt.get('team2').get('teamName')],
                                                                 'venue': f"{mt.get('venueInfo').get('ground')} - {mt.get('city')}",
                                                                 't1_score': f"Runs -{res} | Wickets - {res1} | Overs - {res3}",
                                                                 't2_score': f"Runs - {res4} | Wickets - {res5} | Overs - {res6}"}

                                series_dict[sm_data.get('seriesId')] = {'s_name': sm_data['seriesName'], 'match_info': match_dict}

                    else:print('data not found,selct the match type again')
                temp_dict = {}
                for i, (key, val) in enumerate(series_dict.items(), start=1):
                    temp_dict[str(i)] = {'sid': key, 'sname': val['s_name']}

                print('select any one of the series')
                for key, val in temp_dict.items():
                    print(f'{key} | {val.get("sid")} | {val.get("sname")}')
                while True:
                    sr_choice = input('Enter your choice : ')
                    if sr_choice in temp_dict.keys():
                        break
                    else:print('entered number not in range, please select again..!')

                self.sid = temp_dict.get(sr_choice).get('sid')
                match_info = series_dict.get(self.sid).get('match_info')


                temp_mt_dict = {}
                for i, (key, val) in enumerate(match_info.items(), start=1):
                    temp_mt_dict[str(i)] = {'mid': key, 'mf': val['match_format'], 'mt_status': val['status']}
                print('select anyone of the match')
                for key, val in temp_mt_dict.items():
                    print(f'{key} | {val["mid"]} | {val["mf"]} | {val["mt_status"]}')

                while True:
                    mt_choice = input('Enter your choice : ')
                    if mt_choice not in temp_mt_dict.keys():
                        print('entered number not in range, please select again..!')
                    else: break

                self.mid = temp_mt_dict.get(mt_choice).get('mid')
                break
            else:
                print('No data found..!')
                break

    def matches_info(self):

        url = self.config.get('matches_info_url')
        url+=str(self.mid)
        response = requests.get(url, headers=self.headers)
        while True:
            if response.status_code==200:
                var=response.json()

                data_val = self.config.get('data_val')
                second_val = self.config.get('second_val')
                data_parsing = self.config.get('data_parsing')

                self.table = []
                table1 = []
                table2 = []

                for key, val in var.get('matchInfo').items():
                    if key in data_val:
                        self.table.append(var.get('matchInfo').get(key))

                for key, val in var.get("matchInfo").get("team1").items():
                    if key == 'playerDetails':
                        for i in val:
                            table1.append([i.get(k) for k in second_val])

                for key, val in var.get("matchInfo").get("team2").items():
                    if key == 'playerDetails':
                        for i in val:
                            table2.append([i.get(k) for k in second_val])
                break
            else:
                print('No data found..!')
                break
        def team_details():
            while True:
                end=input('Do you want to know about team details (y/n):')
                if end=='y':
                    print(tabulate([self.table], headers=data_val, tablefmt='pretty'))
                    print(tabulate(table1, headers=second_val, tablefmt='pretty'))
                    print(tabulate(table2, headers=second_val, tablefmt='pretty'))
                    while True:
                        try:
                            team_id = int(input('select the team id from the above repsonse:'))
                            url = self.config.get('matches_info_url')
                            url += f"{self.mid}/team/{team_id}"

                            response = requests.get(url, headers=self.headers)
                            if response.status_code==200:
                                var_2 = response.json()

                                table = []
                                for i in var_2.get('players').get('playing XI'):
                                    table.append([i.get("fullName"), i.get("captain"), i.get("role"), i.get("keeper"),
                                                  i.get("teamId"),
                                                  i.get("battingStyle"), i.get("bowlingStyle"), i.get("teamName")])

                                print(tabulate(table, tablefmt='pretty', headers=data_parsing))
                                break
                            else:
                                print('No data found..!')
                                break
                        except Exception:
                            print('you entered a wrong input try again')
                    break

                elif end == 'n':break
                else:
                    print('you selected invalid option try again')
        team_details()

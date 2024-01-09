from tabulate import tabulate
import requests
class players:
    def __init__(self,headers,config_data):
        self.headers=headers
        self.new_id=0
        self.config=config_data
    def players_list(self):
        table = []
        player_id=[]


        url=self.config.get('players_list_url')
        response=requests.get(url,headers=self.headers)
        while True:
            if response.status_code==200:
                var=response.json()
                for data in var.get('player'):
                    table.append([data.get('id'), data.get('name'), data.get('teamName')])
                    if data.get('id') not in player_id:
                        player_id.append(data.get('id'))
                print(tabulate(table, tablefmt='pretty', headers=self.config.get('players_list_headers')))
                while True:
                        self.new_id = input('enter teamid from above data: ')
                        if self.new_id in player_id:
                            break
                        else:print('invalid input teamid,try again')
                break
            else:
                print('no data found..!')
                break
    def players_career(self):

        while True:
            end = input('do you want to enter players career(y/n):')
            if end == 'y':
                table = []
                url = self.config.get('players_career_url')
                url+=f"{self.new_id}/career"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var = response.json()
                    for data in var.get('values'):
                        table.append([data.get('name'), data.get('debut'), data.get('lastPlayed')])
                    print(tabulate(table, tablefmt='pretty', headers=self.config.get('players_list_career')))
                    break
                else:
                    print('no data found..!')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
    def players_news(self):
        def trim_lines(text, char):
            lines = ""
            for i in range(0, len(text), char):
                lines += text[i:i + char] + '\n'
            return lines


        while True:
            end = input('do you want to enter players news(y/n):')
            if end == 'y':
                table_list = self.config.get('players_news_headers')
                table = []
                url = self.config.get('players_news_url')
                url += f"{self.new_id}"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var=response.json()
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
                    print('no data found..!')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
    def players_bowling(self):
        while True:
            end = input('do you want to enter players bowling(y/n):')
            if end == 'y':
                table = []
                url = self.config.get('players_bowling_url')
                url+=f"{self.new_id}/bowling"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var = response.json()
                    for val in var.get('values'):
                        table.append(val.get('values'))
                    print(tabulate(table, tablefmt='pretty', headers=var['headers']))
                    break
                else:
                    print('no data found..!')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
    def players_batting(self):
        while True:
            end = input('do you want to enter players batting(y/n):')
            if end == 'y':
                table = []
                url = self.config.get('players_batting_url')
                url += f"{self.new_id}/batting"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var = response.json()
                    for val in var.get('values'):
                        table.append(val.get('values'))
                    print(tabulate(table, tablefmt='pretty', headers=var['headers']))
                    break
                else:
                    print('no data found..!')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
    def players_info(self):
        def trim_lines(text, char):
            lines = ""
            for i in range(0, len(text), char):
                lines += text[i:i + char] + '\n'
            return lines

        while True:
            end = input('do you want to enter players info(y/n):')
            if end == 'y':
                table = []
                url = self.config.get('players_info_url')
                url += f"{self.new_id}"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var = response.json()
                    ranks = var.get('rankings')
                    data,data1='',''
                    for bat in ranks.get('bat'):
                        data = f"bat:-{bat}"
                    for bowl in ranks.get('bowl'):
                        data1 = f"bowl:-{bowl}"
                    if len(data) <= 7 and len(data1) <= 7:
                        data1,data=None,None
                    try:
                        bowl=trim_lines(var.get('bowl'), 5)
                        birthplace=trim_lines(var.get('birthPlace'), 5)
                        bio=trim_lines(var.get('bio'), 20)
                    except Exception:
                        bowl='No data'
                        birthplace='No data'
                        bio='No data'
                        data='No data'
                    headers_list = self.config.get('players_info_headers')
                    table.append(
                        [var.get('id'), trim_lines(var.get('bat'), 5),bowl, var.get('name'),
                         var.get('height'), var.get('role'), birthplace,
                         trim_lines(var.get('intlTeam'), 5), trim_lines(var.get('teams'), 12),
                         trim_lines(var.get('DoB'), 5), trim_lines(bio,5), trim_lines(data, 12),
                         trim_lines(data1, 12)])
                    print(tabulate(table, tablefmt='pretty', headers=headers_list))
                    break
                else:
                    print('no data found..!')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
    def players_searching(self):
        while True:
            end = input('do you want to enter players search(y/n):')
            if end == 'y':
                table = []
                player_name=input('enter player name:')
                url = self.config.get('players_searching_url')
                url += f"{player_name}"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    var = response.json()
                    try:
                        for data in var.get('player'):
                            table.append([data.get('id'), data.get('name'), data.get('teamName')])
                        print(tabulate(table, tablefmt='pretty', headers=self.config.get('players_search_headers')))
                        break
                    except Exception:
                        print('cannot found the players details')
                        break
                else:
                    print('no data found..!,for the above name')
                    break
            elif end=='n':break
            else:print('invalid input,try again')
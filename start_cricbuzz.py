from matches_api import matches
from  series_api import  series
from teams_api import teams
from players_api import  players
import yaml

class common:

    def get_config(self,key):
        f = open('config.yaml', 'r')
        data = yaml.safe_load(f)
        f.close()
        return data.get(key)


    def main(self):


        while True:
            print('welcome to cricbuzz')
            print('1.matches', '2.series', '3.teams','4.players', sep='\n')
            usr_ch = input('enter your choice: ')
            if usr_ch == '1':
                mt = matches(
                             headers={
                                 'X-RapidAPI-Key': "52b8d6f78dmshd9de5be3e455893p17a750jsnd9656ca9a8ed",
                                 'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
                             },config_data=self.get_config('matches_val'))
                mt.matches_list()
                mt.matches_info()

            elif usr_ch == '2':
                series_obj = series(
                                    headers={
                                 'X-RapidAPI-Key': "52b8d6f78dmshd9de5be3e455893p17a750jsnd9656ca9a8ed",
                                 'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
                             },config_data=self.get_config('series_val'))
                series_obj.series_list()
                series_obj.series_archives()
                series_obj.series_matches()
                series_obj.series_squads()
                series_obj.series_news()
                series_obj.series_venues()
            elif usr_ch=='3':
                teams_obj=teams(
                                headers={
                                 'X-RapidAPI-Key': "52b8d6f78dmshd9de5be3e455893p17a750jsnd9656ca9a8ed",
                                 'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
                             },config_data=self.get_config('teams_val'))
                teams_obj.teams_list()
                teams_obj.teams_schedules()
                teams_obj.teams_results()
                teams_obj.teams_news()
                teams_obj.teams_players()
            elif usr_ch=='4':
                players_obj=players(headers={
                                 'X-RapidAPI-Key': "52b8d6f78dmshd9de5be3e455893p17a750jsnd9656ca9a8ed",
                                 'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
                             },config_data=self.get_config('players_val'))
                players_obj.players_list()
                players_obj.players_career()
                players_obj.players_news()
                players_obj.players_bowling()
                players_obj.players_batting()
                players_obj.players_info()
                players_obj.players_searching()

            else:
                print('invalid selection try agian')
            while True:
                end=input('do you want to continue the endpoints(y/n): ')
                if end=='y':
                    status=True
                    break
                elif end=='n':
                    status=False
                    break
                else:print('invalid input,try again')
            if status:continue
            else:break
obj=common()
obj.main()




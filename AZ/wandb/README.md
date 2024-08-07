1. install wandb modules
pip install wandb

2. python script:
```py
import wandb
from wandb.apis.public import Api
import requests
import argparse

# # wandb api_key for authorization
# TOKEN = {
#   "Authorization": f"Bearer {XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}"
# }
# # wandb url 
# wandb_api_url = 'https://dev-azimuth-wandb.paas-brown.astrazeneca.net/scim'


# Login to wandb
# print("Login to wandb start")
# wandb.login(
#     key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
#     host='https://dev-raghib-wandb.paas-brown.astrazeneca.net/'
# )
# print("Login to wandb end")

# Intiallizing wandb api
# api = wandb.Api()

# user = api.users(
#    'astrazeneca'
# )
# print(user)

def list_users(api_url):
    user_api_url = f"{api_url}/Users"
    user_response = requests.get(url=user_api_url,headers=TOKEN)
    user_data = user_response.json()['Resources']
    users = []
    user_name = []
    for user in user_data:
        user_detail = {}
        user_detail['DisplayName'] = user['displayName']
        user_detail['Username'] = user['userName']
        user_detail['Email'] = user['emails']['Value']
        users.append(user_detail)
        user_name.append(user['displayName'])
    print(f"Number of users are {len(users)}")
    print(f"List of users are:\n {user_name}")
    print("Details of each users are follwing:")
    print("\n".join(str(user) for user in users))
    return users

def list_team(api_url):
    team_api_url = f"{api_url}/Groups"
    team_response = requests.get(url=team_api_url,headers=TOKEN)
    team_data = team_response.json()['Resources']
    team_list= []
    team_details = []
    for team in team_data:
        team_list.append(team['displayName'])
        teams = {}
        if team['members'] != None:
            teams[team['displayName']] = [user['Display'] for user in team['members']]
        else:
            break
        team_details.append(teams)
    print(f"Number of team are {len(team_list)}")
    print(f"List of all teams in wandb are:\n {team_list}")
    print("List of user in each team are following:")
    print("\n".join(str(team) for team in team_details))
    return team_details

parser = argparse.ArgumentParser(description="You are missing required values")
parser.add_argument("-u", "--wand_url", help="wandb url")
parser.add_argument("-t", "--token", help="wandb token")
args = parser.parse_args()
args = vars(args)
URL = args["wand_url"]
API_KEY = args["token"]

# wandb api_key for authorization
TOKEN = {
  "Authorization": f"Bearer {API_KEY}"
}
# wandb url 
wandb_api_url = URL

list_users(api_url=wandb_api_url)
list_team(api_url=wandb_api_url)
```
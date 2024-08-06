1. install wandb modules
pip install wandb

2. python script:
```py
import wandb
from wandb.apis.public import Api
import requests

# Login to wandb 
# wandb.login(
#     key='local-d318e3cc0363420498089fa092675aa0b80e17be',
#     host='https://dev-azimuth-wandb.paas-brown.astrazeneca.net/'
# )
TOKEN = {
  "Authorization": f"Bearer {'local-d318e3cc0363420498089fa092675aa0b80e17be'}"
}
api_url = "https://dev-azimuth-wandb.paas-brown.astrazeneca.net/scim"
# Initialize the W&B API
# api = wandb.Api()

def list_users():
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

def list_team():
    team_api_url = f"{api_url}/Groups"
    team_response = requests.get(url=team_api_url,headers=TOKEN)
    team_data = team_response.json()['Resources']
    team_list= []
    team_details = []
    for team in team_data:
        teams = {}
        if team['members'] != None:
            teams[team['displayName']] = [user['Display'] for user in team['members']]
        else:
            break
        team_details.append(teams)
        team_list.append(team['displayName'])
    print(f"Number of team are {len(team_list)}")
    print(f"List of all teams in wandb are:\n {team_list}")
    print("List of user in each team are following:")
    print("\n".join(str(team) for team in team_details))

list_users()
list_team()
```
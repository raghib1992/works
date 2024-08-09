import wandb
from wandb.apis.public import Api
import requests
import argparse
import csv 

def list_users(api_url):
    user_api_url = f"{api_url}/Users"
    user_response = requests.get(url=user_api_url,headers=TOKEN)
    user_data = user_response.json()['Resources']
    users_list = []
    for user in user_data:
        if 'teamRoles' in user:
            for team in user['teamRoles']:
                user_detail = {}
                user_detail['GroupName']= team['teamName']
                user_detail['TeamMemberName'] = user['displayName']
                user_detail['UserEmail'] = user['emails']['Value']
                user_detail['UserOrganizationRole'] = user['organizationRole']
                user_detail['Username'] = user['userName']
                user_detail['Active'] = user['active']
                users_list.append(user_detail)
        else:
            user_detail = {}
            user_detail['GroupName']= None
            user_detail['TeamMemberName'] = user['displayName']
            user_detail['UserEmail'] = user['emails']['Value']
            user_detail['UserOrganizationRole'] = user['organizationRole']
            user_detail['Username'] = user['userName']
            user_detail['Active'] = user['active']
            users_list.append(user_detail)
    print(users_list)
    return users_list

def list_team(api_url):
    team_api_url = f"{api_url}/Groups"
    team_response = requests.get(url=team_api_url,headers=TOKEN)
    team_data = team_response.json()['Resources']
    team_list= []
    for team in team_data:
        team_details = {}
        team_details['GroupName'] = team['displayName']
        if team['members'] != None:
            team_details['GroupMember'] = [user['Display'] for user in team['members']]
        else:
            team_details['GroupMember'] = None
        team_list.append(team_details)
    print(team_list)
    return team_list

def create_csv(users_list):
    users = users_list
    fields = ['GroupName', 'TeamMemberName', 'UserEmail', 'UserOrganizationRole', 'Active', 'Username'] 

    with open('wandb_user_details.csv', 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()
        writer.writerows(users)


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

user_list = list_users(api_url=wandb_api_url)
print("Start: Creating csv file...")
create_csv(user_list)
print("Successfully created csv file")

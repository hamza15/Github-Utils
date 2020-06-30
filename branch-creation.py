from github import Github
from github import GithubException
import requests
from sys import exit
import re


#Get input from user for username, repo and branch name
username = input("Please enter your github username: \n")
repo_name = input("Please enter the repo name, you would like to create a branch for: \n")
name = input("Please enter the branch name you would like to create: \n")

#Source repo you would like to create target branch against - Can change this to use a different branch as reference.
source_branch= "master"

#INSERT GITHUB TOKEN HERE
token = ''

#Credentials / Token
g = Github(token)

#Find repo name in list of repos
try:
	repo = g.get_user().get_repo(repo_name)
except GithubException as e:
	print("You are missing the Github token. Please insert in script.")
	exit(0)


for branch in list(repo.get_branches()):
	branch_string = str(branch)
	branch_name = branch_string[13:-2]
	if branch_name == name:
		print(branch_name + " already exists! Please enter another branch name.")
		exit(0)

#Get sha from master to create reference for new branch
master_sha = repo.get_branch(source_branch).commit.sha

print("Creating new branch "+ name)

#Oauth token for your user
headers = {
    'Authorization': 'token ' + token,
}

#data passed with post request - gives name of new branch and sha reference.
data = {
    "ref": "refs/heads/" + name,
    "sha": master_sha
}

#Create a new branch
response = requests.post('https://api.github.com/repos/' + username + '/' + repo_name + '/git/refs', json=data, headers=headers)

print(response)
print(response.content)



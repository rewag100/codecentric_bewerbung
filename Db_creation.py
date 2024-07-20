import argparse
from Db_handler import Db_handler
import urllib.request
import json


def fetch_users(url):
    employees_json = urllib.request.urlopen(url).read()
    employees_data = json.loads(employees_json)
    print('employee')
    for employee in employees_data:
        db.insert_employee(employee['id'], employee['login'])
        fetch_repos(employee['repos_url'])
        
def fetch_repos(url):
    repos_json = urllib.request.urlopen(url).read()
    repos_data = json.loads(repos_json)
    print('repo')
    for repo in repos_data:
        db.insert_repo(repo['id'], repo['name'], repo['owner']['id'], repo['language'])
        if args.more:
            fetch_languages(repo['languages_url'], repo['id'])
            fetch_contributors(repo['contributors_url'], repo['id'])

def fetch_contributors(url, foreign_id=None):
    contributors_json = urllib.request.urlopen(url).read()
    contributors_data = json.loads(contributors_json)
    print('contrib')
    for contributor in contributors_data:
        db.insert_contribution(contributor['id'], foreign_id, contributor['contributions'])
    
def fetch_languages(url, foreign_id=None):
    languages_json = urllib.request.urlopen(url).read()
    languages_data = json.loads(languages_json)
    for language in languages_data:
        db.insert_language(language, languages_data[language], foreign_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a database of codecentric employees and their repositories')
    parser.add_argument('-m', '--more', help='Adds contributions and languages to database --Cant process entire data due to API limitations--', action='store_true')
    args = parser.parse_args()
    db = Db_handler()
    url = "https://api.github.com/orgs/codecentric/members"
    fetch_users(url)
    db.close()

    


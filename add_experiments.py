import argparse
import os
import json
import subprocess


REPO_PATH='/home/arno/Téléchargements/P5A January work/test command/Write apps/easy_experiment_backup_poc/'
DATABASE_NAME ="experiments.json"
DATABASE_PATH = REPO_PATH+DATABASE_NAME

def commit_and_push(dir_path):
    # Change to the directory
    os.chdir(dir_path)
    # Add all modified files to the staging area
    subprocess.run(['git', 'add', '.'])
    # Commit the changes with a commit message that includes the current date
    current_date = subprocess.run(['date', '+%Y-%m-%d'], stdout=subprocess.PIPE).stdout.decode().strip()
    subprocess.run(['git', 'commit', '-m', f'Backup {current_date}'])
    # Push the changes to the repository
    subprocess.run(['git', 'push'])

def add_experiment(database, new_experiment):
    with open(database, 'r') as f:
        database_data = json.load(f)
    with open(new_experiment, 'r') as f:
        new_experiment_data = json.load(f)
    if new_experiment_data["title"] in database_data['experiments']:
        print('An experiment with that title already exist please change title or remove the previously stored experience from database.')
        exit()
    database_data['experiments'][new_experiment_data["title"]]=new_experiment_data
    with open(database, 'w') as f:
        json.dump(database_data, f)

def print_experiment(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    print(json.dumps(data, indent=4, sort_keys=True))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('new_experiment', help='path to the new_experiment')
    args = parser.parse_args()
    print_experiment(args.new_experiment)
    confirm = input('Do you want to add this experiment to the database? (y/n) ')
    if confirm == 'y':
        add_experiment(DATABASE_PATH, args.new_experiment)
        print('Experiment added to the database.')
        commit_and_push(REPO_PATH)
	
    else:
        print('Cancelled.')

if __name__ == '__main__':
    main()


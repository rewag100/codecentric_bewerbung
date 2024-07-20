import sqlite3
import argparse



class Db_handler:
    def __init__(self, path='codecentric_employee.db'):
        print('Init database')
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employees  
                       (id Integer PRIMARY KEY NOT NULL, login text);''')  
        self.con.commit()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS repos  
                            (id Integer PRIMARY KEY NOT NULL, name text, language text, owner_id Integer NOT NULL);''')
        self.con.commit()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employee_repo_contribution  
                       (id Integer PRIMARY KEY NOT NULL, employee_id Integer NOT NULL, 
                       repo_id integer NOT NULL, contributions integer NOT NULL);''')  
        self.con.commit()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS languages  
                       (id Integer PRIMARY KEY NOT NULL, repo_id Integer NOT NULL, language text NOT NULL, 
                       number integer);''')  
        self.con.commit()
        self.con.commit()
        print('..done')


    def insert_employee(self, id, name):
        self.cur.execute('''INSERT INTO employees(id, login) VALUES (?,?)''',
                         [id, name])
        self.con.commit()
        return
        
    def insert_repo(self, id, name, language, owner_id):
        self.cur.execute('''INSERT INTO repos(id, name, language, owner_id) VALUES (?,?,?,?)''',
                         [id, name, language, owner_id])
        self.con.commit()
        return
        
    def insert_language(self, language, number, repo_id):
        self.cur.execute('''INSERT INTO languages(repo_id, language, number) VALUES (?,?,?)''',
                         [repo_id, language, number])
        self.con.commit()
        return
        
    def insert_contribution(self, employee_id, repo_id, contributions):
        self.cur.execute('''INSERT INTO employee_repo_contribution(employee_id, repo_id, contributions) VALUES (?,?,?)''',
                         [employee_id, repo_id, contributions])
        self.con.commit()
        return

# Returns and prints all users, which own at least one repo with the desired language
    def get_language_owners(self, language):
        self.cur.execute('''SELECT DISTINCT id, login FROM
                            (SELECT * FROM employees JOIN repos on employees.id=repos.owner_id
                            WHERE repos.language=='?') ''',[language])
        res = self.cur.fetchall()
        return res 
        
    def get_language_contributors(self, language):
        return

    def close(self):
        self.con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query the employee database')
    parser.add_argument('--olang', help='Gets all people with repos in given programming language')
    parser.add_argument('--clang', help='Gets all people with contributions to repos in given programming language')
    args = parser.parse_args()
    db = Db_handler()
    if args.olang:
        print('Users owning repos containing ',args.olang, ':')
        db.get_language_owners(args.olang)
    if args.clang:
        print('Users who contributed to repos containing ',args.clang, ':')
        db.get_language_contributors(args.clang)
    # if args.insert_paper:
    #    print('Processing clean papers')
    #    db.all_clean_paper_into_db()
    db.close()


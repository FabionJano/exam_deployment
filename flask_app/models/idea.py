from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Idea:
    DB = "provimi"
    def __init__(self,data):
        self.id = data['id']
        self.idea = data['idea']
        self.user_id = data['user_id']
        self.team_id = data['team_id']


    @classmethod
    def get_all_ideas(cls):
        query = "SELECT * FROM ideas;"
        results = connectToMySQL(cls.DB).query_db(query)
        ideas = []
        if results:
            for idea in results:
                ideas.append(idea)
            return ideas
        return ideas
    
    @classmethod
    def get_idea_by_id(cls, data):
        query = 'SELECT * FROM ideas left join users on ideas.user_id = users.id where ideas.id = %(id)s;'
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_ideas_for_user(cls, data):
        query = 'SELECT * FROM ideas where user_id = %(id)s;'
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO ideas (idea, user_id) VALUES (%(idea)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE ideas set idea=%(idea)s where ideas.id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
   
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM ideas where id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def create_team(cls,data):
        query = "INSERT INTO teams (teamName, user_id) VALUES (%(teamName)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_teams(cls):
        query = "SELECT teamName FROM teams where user_id = %(user_id)s;"
        results = connectToMySQL(cls.DB).query_db(query)
        teams = []
        if results:
            for team in results:
                teams.append(team)
            return teams
        return teams

    @classmethod
    def get_team_by_id(cls, data):
        query = 'SELECT * FROM teams left join users on teams.user_id = users.id where teams.id = %(id)s;'
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @staticmethod
    def validate_idea(idea):
        is_valid = True
        
        if len(idea['idea'])<5:
            flash("Idea is required!", 'idea')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_team(team):
        is_valid = True

        if len(team['teamName'])<1:
            flash('Team Name required!' , 'team')
            is_valid = False
        return is_valid
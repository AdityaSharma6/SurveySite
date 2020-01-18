import random

class AlgorithmSolutions():
    def random_links(self):
        low_data = "https://ldd1.herokuapp.com/"
        big_data = "https://bdd1.herokuapp.com/"
        choice = [low_data, big_data]
        random_choice = random.randint(0,1)
        return choice[random_choice]
    
    def is_cheating(self, survey_token):
        stringify = str(survey_token)
        if "8" in stringify:
            return True
        else:
            return False
    
    def num_clicks(self, survey_token, boolean_cheating):
        stringify = str(survey_token)
        if boolean_cheating == True:
            return len(stringify) - 1
        else:
            return len(stringify)
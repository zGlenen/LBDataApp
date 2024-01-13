class Util:
    def __init__(self,number_of_stats):
        self.number_of_stats = number_of_stats

    #returns a sorted dictionary 
    def get_highest_values_in_object(self, object):
        sorted_genres = sorted(object.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_genres[:self.number_of_stats])
    
class Util:
    def __init__(self,number_of_stats):
        self.number_of_stats = number_of_stats

    def get_highest_values_in_object(self, genre_stats):
        sorted_genres = sorted(genre_stats.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_genres[:self.number_of_stats])
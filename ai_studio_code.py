class MediaError(Exception):
    """Custom exception for media-related errors."""
    def __init__(self, message, obj):
        super().__init__(message)
        self.obj = obj

class Movie:
    def __init__(self, title, year, director, duration):
        if not title.strip():
            raise ValueError('Title cannot be empty')
        if year < 1895:
            raise ValueError('Year must be 1895 or later')
        if not director.strip():
            raise ValueError('Director cannot be empty')
        if duration <= 0:
            raise ValueError('Duration must be positive')
        
        self.title = title
        self.year = year
        self.director = director
        self.duration = duration

    def __str__(self):
        return f'{self.title} ({self.year}) - {self.duration} min, {self.director}'

class TVSeries(Movie):
    def __init__(self, title, year, director, duration, seasons, total_episodes):
        # Initialize attributes from the Movie parent class
        super().__init__(title, year, director, duration)

        if seasons < 1:
            raise ValueError('Seasons must be 1 or greater')
        if total_episodes < 1:
            raise ValueError('Total episodes must be 1 or greater')
        
        self.seasons = seasons
        self.total_episodes = total_episodes

    def __str__(self):
        return f'{self.title} ({self.year}) - {self.seasons} seasons, {self.total_episodes} episodes, {self.duration} min avg, {self.director}'

class MediaCatalogue:
    def __init__(self):
        self.items = []

    def add(self, media_item):
        # Ensure only Movie or TVSeries instances are added
        if not isinstance(media_item, Movie):
            raise MediaError('Only Movie or TVSeries instances can be added', media_item)
        self.items.append(media_item)

    def get_movies(self):
        # Uses type() to ensure we ONLY get Movies, not TVSeries (subclasses)
        return [item for item in self.items if type(item) is Movie]

    def get_tv_series(self):
        # Uses isinstance() to get TVSeries items
        return [item for item in self.items if isinstance(item, TVSeries)]
    
    def __str__(self):
        if not self.items:
            return "Media Catalogue (empty)"
        
        movies = self.get_movies()
        tv_series = self.get_tv_series()
        
        result = f"Media Catalogue ({len(self.items)} items):\n\n"
        
        # Format Movies Section
        if movies:
            result += "=== MOVIES ===\n"
            for index, item in enumerate(movies, start=1):
                result += f"{index}. {item}\n"
        
        # Add a separator if both sections exist
        if movies and tv_series:
            result += "\n"

        # Format TV Series Section
        if tv_series:
            result += "=== TV SERIES ===\n"
            for index, item in enumerate(tv_series, start=1):
                result += f"{index}. {item}\n"
                
        return result.strip() # .strip() removes trailing whitespace

# --- Testing the implementation ---
if __name__ == "__main__":
    catalogue = MediaCatalogue()

    try:
        # Adding Movies
        movie1 = Movie('The Matrix', 1999, 'The Wachowskis', 136)
        catalogue.add(movie1)
        movie2 = Movie('Inception', 2010, 'Christopher Nolan', 148)
        catalogue.add(movie2)

        # Adding TV Series
        series1 = TVSeries('Scrubs', 2001, 'Bill Lawrence', 24, 9, 182)
        catalogue.add(series1)
        series2 = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)
        catalogue.add(series2)

        # Displaying the Catalogue
        print(catalogue)

    except ValueError as e:
        print(f'Validation Error: {e}')
    except MediaError as e:
        print(f'Media Error: {e}')
        print(f'Unable to add {e.obj}: {type(e.obj)}')
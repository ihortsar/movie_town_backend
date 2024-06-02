from movies.admin import CustomMovieResource
from user.admin import CustomUserResource


def export_data():
    
    movie_resource = CustomMovieResource()
    user_resource = CustomUserResource()

    # Exports datasets using the instances
    movie_dataset = movie_resource.export()
    user_dataset = user_resource.export()

    # Saves datasets to CSV files
    with open('movies.csv', 'w') as movie_file:
        movie_file.write(movie_dataset.csv)

    with open('users.csv', 'w') as user_file:
        user_file.write(user_dataset.csv)

   


from utils.loadutils import *
import numpy as np
import tensorflow as tf
from movieModel import Mymodel
from utils.databaseUtils import MyDataBase

isfirstrun=True

X, W, b, num_movies, num_features, num_users = load_precalc_params_small()
Y, R = load_ratings_small()
movieList, movieList_df = load_Movie_List_pd()

my_ratings = np.zeros(num_movies)  # Initialize my ratings

# Check the file small_movie_list.csv for id of each movie in our dataset
# For example, Toy Story 3 (2010) has ID 2700, so to rate it "5", you can set
my_ratings[2700] = 5
# Or suppose you did not enjoy Persuasion (2007), you can set
my_ratings[2609] = 2
# We have selected a few movies we liked / did not like and the ratings we
# gave are as follows:
my_ratings[929] = 5  # Lord of the Rings: The Return of the King, The
my_ratings[246] = 5  # Shrek (2001)
my_ratings[2716] = 3  # Inception
my_ratings[1150] = 5  # Incredibles, The (2004)
my_ratings[382] = 2  # Amelie (Fabuleux destin d'Amélie Poulain, Le)
my_ratings[366] = 5  # Harry Potter and the Sorcerer's Stone (a.k.a. Harry Potter and the Philosopher's Stone) (2001)
my_ratings[622] = 5  # Harry Potter and the Chamber of Secrets (2002)
my_ratings[988] = 3  # Eternal Sunshine of the Spotless Mind (2004)
my_ratings[2925] = 1  # Louis Theroux: Law & Disorder (2008)
my_ratings[2937] = 1  # Nothing to Declare (Rien à déclarer)
my_ratings[793] = 5  # Pirates of the Caribbean: The Curse of the Black Pearl (2003)
my_rated = [i for i in range(len(my_ratings)) if my_ratings[i] > 0]

print('\nNew user ratings:\n')
for i in range(len(my_ratings)):
    if my_ratings[i] > 0:
        print(f'Rated {my_ratings[i]} for  {movieList_df.loc[i, "title"]}')

# Add new user ratings to Y
Y = np.c_[my_ratings, Y]

# Add new user indicator matrix to R
R = np.c_[(my_ratings != 0).astype(int), R]

model = Mymodel()
model.fit(Y, R)
my_predictions = model.predict(0)

# sort predictions
ix = tf.argsort(my_predictions, direction='DESCENDING')


print('\n\nPredicted movie\n')
recommend_list=[]
recommend_score=[]
for i in range(17):
    j = ix[i]
    if j not in my_rated:
        recommend_list.append(int(j))
        recommend_score.append(float(my_predictions[j]))
        print(f'Predicting rating {my_predictions[j]:0.2f} for movie {movieList[j]}')

print("display the data to neo4j...this may take minutes")
#show to neo4j
database = MyDataBase()
database.ShowToDatabase(movieList_df, Y,reload=isfirstrun)
database.ShowRecommed(0,recommend_list,recommend_score)
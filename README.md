language
- [中文文档](./阅读我.md)

1. **Q: What is this project about?**
   - This project obtains a user-movie rating table by reading a local csv file, and then calculates the movies to be recommended to a certain user based on a collaborative filtering algorithm.
   - The results of the collaborative recommendations are then displayed in a graph database for visualization.


2. **Q: How do I run this project??**
   - You need to first set up a [neo4j](https://blog.csdn.net/zsh1184528359/article/details/105893647) database.
   -  Configure the `config.yaml` in the project directory, entering your database password, database URL, and database name.
   - After configuration, enter `neo4j console` in the command line to start the database (i.e., the `runneo4j.bat` script in this project)
   - Then run `main.py` in the project.
   - Open the relevant database interface.
   - Enter the relevant query statements
        ```
        MATCH (u1:user)-[:recommend]->(recmovie:movie)
        WITH u1, recmovie, rand() AS randomOrder1
        ORDER BY randomOrder1
        LIMIT 1
        MATCH (u2:user)-[ratingRelation:`rated`]->(recmovie)
        WITH u1, u2,recmovie,rand() AS randomOrder2
        order by randomOrder2
        LIMIT 2
        MATCH (u1)-[:`rated`]->(commonMovie:movie)<-[:`rated`]-(u2)
        RETURN u1, u2, collect(commonMovie) AS CommonMovies,recmovie
        ```
   you might get image like this
   <img src="img/dataresult.png"/>
   this might help you explore the reason you were recommended a certain movie (whether there is a user with similar interests who liked this movie)

3. **Q: How can I change my current movie ratings?**
   - You can modify your movie ratings in the code block in `main.py`
   ```
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
    ```

4. **Q: How can I contact the author?** 
   - You can contact me through my QQ email `1023097618@qq.com`.
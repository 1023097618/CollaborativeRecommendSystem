from py2neo import Graph, Subgraph, Node, NodeMatcher, Relationship
import pandas as pd
import yaml


class MyDataBase:

    def __init__(self):
        with open("config.yaml", 'r') as fp:
            config = yaml.safe_load(fp)
        password = config['password']
        boltUrl = config['boltUrl']
        databaseName = config['databaseName']
        self.graph = Graph(boltUrl, auth=(databaseName, password))
        self.matcher = NodeMatcher(self.graph)

    def ShowToDatabase(self, Movie: pd.DataFrame, ratings, reload=True):
        if not reload:
            return
        self.graph.delete_all()
        for id, movie in Movie.iterrows():
            movienode = Node('movie', id=id, meanRating=movie[0], numberOfRating=movie[1], title=movie[2])
            self.graph.create(movienode)
        movieNumber, userNumber = ratings.shape
        for j in range(userNumber):
            user = Node('user', id=j)
            self.graph.create(user)
        for i in range(movieNumber):
            movie_node = self.matcher.match("movie", title=Movie.loc[i, 'title']).first()
            for j in range(userNumber):
                if ratings[i, j] != 0:
                    user_node = self.matcher.match("user", id=j).first()
                    rela = Relationship(user_node, 'rated', movie_node, score=float(ratings[i, j]))
                    self.graph.create(rela)

    def ShowRecommed(self, userid, recommendid, predictedscore):
        user = self.matcher.match("user", id=userid).first()
        for i, id in enumerate(recommendid):
            movie = self.matcher.match("movie", id=id).first()
            rela = Relationship(user, "recommend", movie, predictedScore=predictedscore[i])
            self.graph.create(rela)

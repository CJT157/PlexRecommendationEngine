from neo4j import GraphDatabase

class Database:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_new_user(self, id, name):
        with self.driver.session() as session:
            user = session.execute_write(self._create_user, id, name)

    @staticmethod
    def _create_user(tx, id, name):
        result = tx.run("MERGE (u:USER {id: $id, name: $name})", id=id, name=name)
        return result
    
    def create_new_movie(self, title, rating, aud_rating, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._create_new_movie, title, rating, aud_rating, guid)

    @staticmethod
    def _create_new_movie(tx, title, rating, aud_rating, guid):
        result = tx.run("MERGE (m:MOVIE {title: $title, rating: $rating, aud_rating: $aud_rating, guid: $guid})", title=title, rating=rating, aud_rating=aud_rating, guid=guid)
        return result
    
    def create_new_show(self, title):
        with self.driver.session() as session:
            user = session.execute_write(self._create_new_show, title)

    @staticmethod
    def _create_new_show(tx, title):
        result = tx.run("MERGE (s:SHOW {title: $title})", title=title)
        return result
    
    def create_new_episode(self, title, show_title):
        with self.driver.session() as session:
            user = session.execute_write(self._create_new_episode, title, show_title)

    @staticmethod
    def _create_new_episode(tx, title, show_title):
        result = tx.run("MERGE (e:EPISODE {title: $title, show_title: $show_title})", title=title, show_title=show_title)
        return result
    
    def create_new_person(self, name):
        with self.driver.session() as session:
            user = session.execute_write(self._create_new_person, name)

    @staticmethod
    def _create_new_person(tx, name):
        result = tx.run("MERGE (a:PERSON {name: $name})", name=name)
        return result
    
    def create_new_genre(self, name):
        with self.driver.session() as session:
            user = session.execute_write(self._create_new_genre, name)

    @staticmethod
    def _create_new_genre(tx, name):
        result = tx.run("MERGE (a:GENRE {name: $name})", name=name)
        return result
    
    def create_new_content_rating(self, name):
        with self.driver.session() as session:
            user = session.execute_write(self._create_new_content_rating, name)

    @staticmethod
    def _create_new_content_rating(tx, name):
        result = tx.run("MERGE (a:CONTENT_RATING {name: $name})", name=name)
        return result

        
    def connect_user_and_movie(self, id, title, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_user_and_movie, id, title, guid)

    @staticmethod
    def _connect_user_and_movie(tx, id, title, guid):
        result = tx.run("MATCH (u:USER), (m:MOVIE)"
                        "WHERE u.id = $id AND m.title = $title AND m.guid = $guid "
                        "MERGE (u)-[r:WATCHED]->(m)", id=id, title=title, guid=guid)
        return result
    
    def connect_show_and_episode(self, title, show_title):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_show_and_episode, title, show_title)

    @staticmethod
    def _connect_show_and_episode(tx, title, show_title):
        result = tx.run("MATCH (s:SHOW), (e:EPISODE)"
                        "WHERE s.title = $show_title AND e.title = $title AND e.show_title = $show_title "
                        "MERGE (s)-[r:HAS_EPISODE]->(e)", title=title, show_title=show_title)
        return result
    
    def connect_user_and_episode(self, id, title, show_title):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_user_and_episode, id, title, show_title)

    @staticmethod
    def _connect_user_and_episode(tx, id, title, show_title):
        result = tx.run("MATCH (u:USER), (e:EPISODE)"
                        "WHERE u.id = $id AND e.title = $title AND e.show_title = $show_title "
                        "MERGE (u)-[r:WATCHED]->(e)", id=id, title=title, show_title=show_title)
        return result
    
    
    def connect_actor_and_movie(self, name, title, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_actor_and_movie, name, title, guid)
    
    @staticmethod
    def _connect_actor_and_movie(tx, name, title, guid):
        result = tx.run("MATCH (a:PERSON), (b:MOVIE)"
                        "WHERE a.name = $name AND b.title = $title AND b.guid = $guid "
                        "MERGE (a)-[r:STARS_IN]->(b)", name=name, title=title, guid=guid)
        return result
    
    def connect_actor_and_show(self, name, title):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_actor_and_show, name, title)
    
    @staticmethod
    def _connect_actor_and_show(tx, name, title):
        result = tx.run("MATCH (a:PERSON), (b:SHOW)"
                        "WHERE a.name = $name AND b.title = $title "
                        "MERGE (a)-[r:STARS_IN]->(b)", name=name, title=title)
        return result
    
    def connect_director_and_movie(self, name, title, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_director_and_movie, name, title, guid)
    
    @staticmethod
    def _connect_director_and_movie(tx, name, title, guid):
        result = tx.run("MATCH (a:PERSON), (b:MOVIE)"
                        "WHERE a.name = $name AND b.title = $title AND b.guid = $guid "
                        "MERGE (a)-[r:DIRECTED]->(b)", name=name, title=title, guid=guid)
        return result
    
    def connect_director_and_show(self, name, title, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_director_and_show, name, title, guid)
    
    @staticmethod
    def _connect_director_and_show(tx, name, title):
        result = tx.run("MATCH (a:PERSON), (b:SHOW)"
                        "WHERE a.name = $name AND b.title = $title "
                        "MERGE (a)-[r:DIRECTED]->(b)", name=name, title=title)
        return result
    
    def connect_movie_and_genre(self, name, title, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_movie_and_genre, name, title, guid)
    
    @staticmethod
    def _connect_movie_and_genre(tx, name, title, guid):
        result = tx.run("MATCH (a:MOVIE), (b:GENRE)"
                        "WHERE a.title = $title AND b.name = $name AND a.guid = $guid "
                        "MERGE (a)-[r:MOVIE_GENRE]->(b)", title=title, name=name, guid=guid)
        return result
    
    def connect_movie_and_content_rating(self, name, title, guid):
        with self.driver.session() as session:
            user = session.execute_write(self._connect_movie_and_content_rating, name, title, guid)
    
    @staticmethod
    def _connect_movie_and_content_rating(tx, name, title, guid):
        result = tx.run("MATCH (a:MOVIE), (b:CONTENT_RATING)"
                        "WHERE a.title = $title AND b.name = $name AND a.guid = $guid  "
                        "MERGE (a)-[r:MOVIE_CONTENT_RATING]->(b)", title=title, name=name, guid=guid)
        return result


    def get_movie_for_user(self, id):
        with self.driver.session() as session:
            results = session.execute_write(self._get_movie_for_user, id)
            return results
    
    @staticmethod
    def _get_movie_for_user(tx, id):

        """

        Currently this:
        - Grabs movies based on watched genres
        - Ensures there aren't any already watched
        - Orders based on rating

        Needs to:
        - Grab a movie once
        - Order based on how close user's rating is to either critic or audience
            - Use watched movie ratings as backup if not rated

        """

        result = tx.run("MATCH (a:USER)-[:WATCHED]->(m1:MOVIE)-[:MOVIE_GENRE]->(g1:GENRE)<-[:MOVIE_GENRE]-(m2:MOVIE)-[:MOVIE_GENRE]->(g2:GENRE)<-[:MOVIE_GENRE]-(m1:MOVIE)-[:MOVIE_CONTENT_RATING]->(r1:CONTENT_RATING)<-[:MOVIE_CONTENT_RATING]-(m2:MOVIE) "
                        "WHERE a.id = $id AND NOT (a)-[:WATCHED]->(m2) AND m1 <> m2 AND g1 <> g2 "
                        "WITH toInteger(5*rand()-2.5) AS random, m1, m2 " 
                        "WITH SUM(ABS(m1.rating - m2.rating) + ABS(m1.aud_rating - m2.aud_rating) + random) AS sim, m2 "
                        "ORDER BY sim ASC "
                        "RETURN DISTINCT m2 "
                        "LIMIT 50", id=id)
        return result.data()
# Plex Recommendation Engine

Plex doesn't have a recommendation system for personal media servers, so I wanted to try and make one. This project creates a playlist for each user to get recommended movies based on what they have watched on your server.

### Project Requirements

- Tautulli
    - https://tautulli.com/
    - Tracks user activity on your plex server. Will only have watched data from the day it is set up.
- Neo4j Desktop
    - https://neo4j.com/download/
    - This project is set up to use a local instance on neo4j to generate recommendations. There is probably a more lightweight way to do this, but it works for me.

### Setup Tutorial

1. Create a new python env in the project

```
python -m venv ./venv
```

2. Activate virtual environment

```
source venv/Scripts/activate
```

3. Download requirements

```
pip install -r requirements.txt
```

4. Create a new Neo4j DBMS instance

5. Add an `.env` file to the project with the following content

```
PLEX_URL=plex_server_url #(likely http://host_ip:32400)
PLEX_TOKEN=your_plex_token
TAUTULLI_URL=your_tautulli_url #(likely http://host_ip:8181)
TAUTULLI_API_KEY=your_tautulli_api_key
DATABASE_URL=neo4j_database_url #(likely bolt://localhost:7687)
DATABASE_USERNAME=neo4j_dbms_username
DATABASE_PASSWORD=neo4j_dbms_password
```

6. Run the recommendation script (Will take some time on first run)

```
python app.py
```
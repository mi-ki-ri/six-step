import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from graphviz import Graph
import argparse

g = Graph(format='png')

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--primary", help="primary artist")
parser.add_argument("-s", "--secondary", help="secondary artist")
args = parser.parse_args()
print(args)
primary = args.primary
secondary = args.secondary


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results1 = spotify.search(q='artist:' + primary, type='artist')
items1 = results1['artists']['items']
if len(items1) > 0:
    artist1 = items1[0]
    print(artist1['name'], artist1['images'][0]['url'])

results2 = spotify.search(q='artist:' + secondary, type='artist')
items2 = results2['artists']['items']
if len(items2) > 0:
    artist2 = items2[0]
    print(artist2['name'], artist2['images'][0]['url'])

relation_list = []

step = 1
with g.subgraph(name=f"STEP: {step}") as c:
    c.attr(color='blue')
    c.node(artist1["name"], fontcolor='red')


artist_ids = [artist1["id"]]
last_name = artist1["name"]

flag = False

readed = []

while flag == False:
    with g.subgraph(name=f"STEP: {step}") as cfor:
        cfor.attr(color='blue')
        for artist_id in artist_ids:

            last_name = spotify.artist(artist_id=artist_id)["name"]

            artist_id_tmp = []
            relatetions = spotify.artist_related_artists(artist_id=artist_id)
            time.sleep(0.5)

            for relation in relatetions["artists"]:
                print(step, relation["name"], relation["id"])

                if relation["id"] == artist2["id"]:
                    print("!!!!!!TRUE!!!!!")
                    flag = True
                    cfor.node(relation["name"], fontcolor="red")
                    cfor .edge(last_name, relation["name"])
                    break
                else:
                    cfor.node(relation["name"])
                    cfor.edge(last_name, relation["name"])
                    flag = False

                # relation_list.append(relation)
                # relation_list = list(set (relation_list))

                if relation["id"] in readed:
                    readed.append(relation["id"])
                    readed = list(set(readed))
                    continue

                artist_id_tmp.append(relation["id"])
                artist_id_tmp = list(set(artist_id_tmp))
                readed.append(relation["id"])
                readed = list(set(readed))

            artist_ids = artist_id_tmp

            if flag == True:
                break

        step += 1
        if step >= 6:
            break

g.render('./graph', view=True)

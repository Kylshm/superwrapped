from pyfiglet import Figlet
import os
import json

breaker = "\n═══════════════════════════════════════════════════════════════════"
# inits
songs = {}
podcasts = {}
audiobooks = {}
general_data = [0, 0, 0,]

"""
Work in progress
audio dict is structured as such:
    {spotify_track_uri: [song_name, album, artist, listening_count, listening_ms, skip_count, time: list, reasons: list of list]}

general data is structured as such:
    [listening_time: int, unique_song_count: int, song_count: int, reason_start: list, reason_end: list]
"""
def populate(entry: dict, uri: str, isSong: bool = False, isPodcast: bool = False, isAudiobook: bool = False):
    # initialisations
    name = ""
    album = ""
    artist = ""
    listening_count = 0
    listening_ms = 0
    skip_count = 0
    time = []
    reasons = ["", ""]

    listening_count = 1
    listening_ms = entry["ms_played"]
    general_data[0] += listening_ms
    skip_count = int(entry["skipped"])
    reasons[0] = entry["reason_start"]
    reasons[1] = entry["reason_end"]
    time.append(entry["ts"])

    if isSong:
        name = entry["master_metadata_track_name"]
        album = entry["master_metadata_album_album_name"]
        artist = entry["master_metadata_album_artist_name"]

        songs.update({uri: [name, album, artist, listening_count, listening_ms, skip_count, time, [reasons]]})
    elif isPodcast:
        name = entry["episode_name"]
        artist = entry["episode_show_name"] 
        podcasts.update({uri: [name, album, artist, listening_count, listening_ms, skip_count, time, [reasons]]})
    elif isAudiobook:
        name = entry["audiobook_title"]
        audiobooks.update({uri: [name, album, artist, listening_count, listening_ms, skip_count, time, [reasons]]})
    else:
        # raise Exception("Invalid type: `populate` acccepts songs, podcasts or audiobooks")
        pass
    

def extract_audiodata(JSONfile):
    """
    Takes in a JSON file and extracts data on songs
    """

    f = open(JSONfile, encoding="utf-8")
    bigdata = json.load(f)

    # bigdata is a list of dictionaries
    for entry in bigdata:
        
        song_uri = entry["spotify_track_uri"]
        episode_uri = entry["spotify_episode_uri"]
        audiobook_uri = entry["audiobook_uri"]

        if song_uri != None and song_uri in songs.keys():
            song_update = songs[song_uri]
            song_update[3] += 1
            song_update[4] += entry["ms_played"]
            song_update[5] += int(entry["skipped"])
            song_update[6].append(entry["ts"])
            song_update[7].append([entry["reason_start"], entry["reason_end"]])
            songs[song_uri] = song_update
            general_data[0] += entry["ms_played"]
            general_data[2] += 1
            continue

        elif episode_uri != None and episode_uri in podcasts.keys():
            continue

        elif audiobook_uri != None and audiobook_uri in audiobooks.keys():
            continue

        general_data[1] += 1
        if song_uri:
            populate(entry, song_uri, isSong=True)
        elif episode_uri:
            populate(entry, episode_uri, isPodcast=True)
        elif audiobook_uri:
            populate(entry, audiobook_uri, isAudiobook=True)
        


def main():
    font = Figlet(font="ansi_shadow")
    print(breaker)
    print(font.renderText("super\nwrapped"))
    print(breaker)
    print("""
superwrapped is a fun sideproject that takes in your listening history and analyses it. More specifically, it finds your
    - Most (and least) listened song/album/artist
    - total listening time
    - most common time to listen songs

and more...

superwrapped is a work in progress and will be made entirely WITHOUT AI.
    """
    )

    keyInput = input("Press Enter to Start ")
    print("Looking for the Spotify Extended Streaming History folder...\n")

    if not os.path.exists("./Spotify Extended Streaming History"):
        print("Directory does not exist. Ensure this program and the folder are in the same location")
        print(breaker)
        exit()
    
    files = os.listdir("./Spotify Extended Streaming History")
    if not files:
        print("This directory is empty. Ending program")
        print(breaker)
        exit()

    print("Folder found, has the following files:")
    for file in files:
        print("./Spotify Extended Streaming History/" + file)

    
    extract_audiodata("./Spotify Extended Streaming History/" + files[1])
    # print(songs["spotify:track:0Ky1rnbxYY41g4H9plxK6Q"])
    # print("spotify:track:0Ky1rnbxYY41g4H9plxK6Q" in songs.keys())
    print(songs)
    print(general_data)
    # print(songs["spotify:track:658Y5hbi22nw7ABEYVlwXZ"])
    # print("spotify:track:658Y5hbi22nw7ABEYVlwXZ" in songs.keys())
    print(files)
    # print(songs)
    # for idk in songs:
    #     print(idk == "spotify:track:0Ky1rnbxYY41g4H9plxK6Q")
    

if __name__=="__main__":
    main()
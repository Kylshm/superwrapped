from pyfiglet import Figlet
import os
import json

breaker = "\n═══════════════════════════════════════════════════════════════════"
# inits
songs = videos = podcasts = audiobooks = {}
general_data = []

"""
Work in progress
audio dict is structured as such:
    {spotify_track_uri: [song_name, album, artist, listening_count, listening_ms, skip_count, reason_start: list, reason_end: list]}

general data is structured as such:
    [time_count: int, unique_song_count: int, song_count: int, reason_start: list, reason_end: list]
"""
def populate(entry: dict, isSong: bool=False, isPodcast:bool=False, isAudiobook:bool=False) -> None:
    # TODO: generalise lines 45-80 to this func
    pass # idk


def extract_audiodata(JSONfile):
    """
    Takes in a JSON file and extracts data on songs
    """

    # inits
    # podcast alternatives: album = podcast name, artist = podcast artist
    # audiobook alt's: artist = author
    name = ""
    album = ""
    artist = ""
    listening_count = 0
    listening_ms = 0
    skip_count = 0

    f = open(JSONfile, encoding="utf-8")
    bigdata = json.load(f)
    print(bigdata[0].keys())
    print(bigdata[0].values())

    # bigdata is a list of dictionaries
    for entry in bigdata:
        # get data, then put it in relevant audio dict (songs or podcasts or audiobooks)
        # entry_values = [song_name, album, artist, listening_count, listening_ms, skip_count]
        reason_start = reason_end = [] # for now
        song_uri = entry["spotify_track_uri"]
        episode_uri = entry["spotify_episode_uri"]
        audiobook_uri = entry["audiobook_uri"]

        # check if already counted - if so, increment the listening count and add ms listened
        #  If not, add as new entry
        if song_uri != None and song_uri in songs.values():
            songs[song_uri][3] += 1
            songs[song_uri][4] += entry["ms_played"]
            songs[song_uri][5] += int(entry["skipped"])

        elif episode_uri != None and episode_uri in podcasts.values():
            continue

        elif audiobook_uri != None and audiobook_uri in audiobooks.values():
            continue

        else:
            # add new entry

            if song_uri != None:
                name = entry["master_metadata_track_name"]
                album = entry["master_metadata_album_album_name"]
                artist = entry["master_metadata_album_artist_name"]
            elif audiobook_uri != None:
                continue
            elif episode_uri != None:
                continue

            listening_count = 1
            listening_ms = entry["ms_played"]
            skip_count += int(entry["skipped"])
            
        # print(entry["spotify_track_uri"])


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

    # analyse songs
    # for file in files[1:]:
    #     # f = open("./Spotify Extended Streaming History/" + file, encoding="utf-8")
    #     # print("for file " + file)
    #     # print(json.load(f))
    #     extract_songs("./Spotify Extended Streaming History/" + file)
    extract_audiodata("./Spotify Extended Streaming History/" + files[1])

if __name__=="__main__":
    main()
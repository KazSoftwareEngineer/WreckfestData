import csv
import json

ALL_TRACKS_KEY = 'allTracks'
LOCATION_COL = 0
TRACK_COL = 1
SERVER_ID_COL = 2
TIME_COL = 3
IMG_LOC_COL = 4
IMG_TRACK_COL = 5
SURFACE_COL = 6
LENGTH_COL = 7
AREA_COL = 8
ATTRIBUTE_RANGE = (9, 14)
MOD_COL = 15
WEATHER_TOD_RANGE = (17, 41)
NOTES_COL = 42

attributes_list = []


def computeRoughTrackTime(time):
    minuteSeconds = time.split(':')
    seconds = int(minuteSeconds[1])
    minutes = int(minuteSeconds[0])
    seconds = seconds + minutes * 60
    return seconds

def readInRowFromCSV(row, trackDictionary):
    newTrackDict = {}
    newTrackDict['location'] = row[LOCATION_COL].strip(' ')
    newTrackDict['track'] = row[TRACK_COL]. strip(' ')
    newTrackDict['serverID'] = row[SERVER_ID_COL].strip(' ')

    if len(row[TIME_COL].strip(' ')) > 0:
        newTrackDict['strRoughLapTime'] = row[TIME_COL].strip(' "')
        newTrackDict['roughLapTimeSeconds'] = computeRoughTrackTime(row[TIME_COL].strip(' "'))
    
    newTrackDict['imgLocURL'] = row[IMG_LOC_COL].strip(' ')
    newTrackDict['imgTrackURL'] = row[IMG_TRACK_COL].strip(' ')
    newTrackDict['surface'] = row[SURFACE_COL].strip(' ')

    if len(row[7].strip(' ')) > 0:
        newTrackDict['trackLengthKm'] = float(row[LENGTH_COL])
    if len(row[8].strip(' ')) > 0:
        newTrackDict['arenaSizeHA'] = float(row[AREA_COL])

    newTrackDict['trackAttributes'] = []
    for i in range(ATTRIBUTE_RANGE[0], ATTRIBUTE_RANGE[1] + 1):
        if(row[i] == 'TRUE'):
            newTrackDict['trackAttributes'].append(attributes_list[i])
    
    newTrackDict['weatherToD'] = []
    for j in range(WEATHER_TOD_RANGE[0], WEATHER_TOD_RANGE[1] + 1):
        if(row[j] == 'TRUE'):
            newTrackDict['weatherToD'].append(attributes_list[j])

    newTrackDict['notes'] = row[NOTES_COL]

    trackDictionary[ALL_TRACKS_KEY].append(newTrackDict)
    
    

### END OF FUNCTIONS

### BEGINNING OF MAIN PART OF SCRIPT
with open('./BaseCSV.csv', mode='r') as WreckfestBaseTracksCSV:

    # Takes the column headers as attributes
    attributes_list = next(WreckfestBaseTracksCSV).split(',')

    csv_reader = csv.reader(WreckfestBaseTracksCSV, delimiter=',')
    
    all_tracks_dict = {ALL_TRACKS_KEY: []}

    # TESTING PURPOSES ONLY
    # index = 0
    # TESTING PURPOSES ONLY

    for row in csv_reader:
        readInRowFromCSV(row, all_tracks_dict)

        # TESTING PURPOSES ONLY
        # print()
        # print(all_tracks_dict[ALL_TRACKS_KEY][index])
        # print()
        # index = index + 1
        # if index > 2:
        #     break
        # TESTING PURPOSES ONLY

        
WreckfestBaseTracksCSV.close()

with open('BaseJSONType1.json', 'w') as WreckfestBaseTracksJSON:
    json.dump(all_tracks_dict, WreckfestBaseTracksJSON)

WreckfestBaseTracksJSON.close()
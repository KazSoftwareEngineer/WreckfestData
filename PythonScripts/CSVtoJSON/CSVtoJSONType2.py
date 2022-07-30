import csv
import json

ALL_LOCATIONS_KEY = 'allLocations'
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

def computeRoughTrackTime(time):
    minuteSeconds = time.split(':')
    seconds = int(minuteSeconds[1])
    minutes = int(minuteSeconds[0])
    seconds = seconds + minutes * 60
    return seconds

def readInRowFromCSV(row, locDictionary, locationIndex):

    if locationIndex == -1 or (locDictionary[ALL_LOCATIONS_KEY][locationIndex]['location'] != row[LOCATION_COL]):
        newLocDict = {}
        newLocDict['location'] = row[LOCATION_COL].strip(' ')
        newLocDict[ALL_TRACKS_KEY] = []
        newLocDict['imgLocURL'] = row[IMG_LOC_COL].strip(' ')

        newLocDict['weatherToD'] = []
        for j in range(WEATHER_TOD_RANGE[0], WEATHER_TOD_RANGE[1] + 1):
            if(row[j] == 'TRUE'):
                newLocDict['weatherToD'].append(attributes_list[j])
        
        locDictionary[ALL_LOCATIONS_KEY].append(newLocDict)
        locationIndex = locationIndex + 1

    targetLoc = locDictionary[ALL_LOCATIONS_KEY][locationIndex]

    newTrackDict = {}
    newTrackDict['track'] = row[TRACK_COL]. strip(' ')
    newTrackDict['serverID'] = row[SERVER_ID_COL].strip(' ')
    if len(row[TIME_COL].strip(' ')) > 0:
        newTrackDict['strRoughLapTime'] = row[TIME_COL].strip(' "')
        newTrackDict['roughLapTimeSeconds'] = computeRoughTrackTime(row[TIME_COL].strip(' "'))
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
    
    newTrackDict['notes'] = row[NOTES_COL]

    targetLoc[ALL_TRACKS_KEY].append(newTrackDict)

    return locationIndex
    


### BEGINNING OF MAIN PART OF SCRIPT
with open('./BaseCSV.csv', mode='r') as WreckfestBaseTracksCSV:

    # Takes the column headers as attributes
    attributes_list = next(WreckfestBaseTracksCSV).split(',')

    csv_reader = csv.reader(WreckfestBaseTracksCSV, delimiter=',')
    
    all_locations_dict = {ALL_LOCATIONS_KEY: []}

    locationIndex = -1

    # TESTING PURPOSES ONLY
    # index = 0
    # TESTING PURPOSES ONLY

    for row in csv_reader:
        locationIndex = readInRowFromCSV(row, all_locations_dict, locationIndex)

        # TESTING PURPOSES ONLY
        # print()
        # print(all_locations_dict[ALL_LOCATIONS_KEY][index])
        # print()
        # index = index + 1
        # if index > 2:
        #     break
        # TESTING PURPOSES ONLY

        
WreckfestBaseTracksCSV.close()

with open('BaseJSONType2.json', 'w') as WreckfestBaseTracksJSON2:
    json.dump(all_locations_dict, WreckfestBaseTracksJSON2)

WreckfestBaseTracksJSON2.close()
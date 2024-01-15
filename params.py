team_number = 3543  # Your team number
allowed_file_extensions = ["xlsx", "xlsx"]  # Used for data processing
teams = [
    417,
    3543,
    6220,
    7330,
    8103,
    8923,
    9884,
    11138,
    14343,
    16113,
    16493,
    16750,
    16942,
    16965,
    17239,
    19929,
    20403,
    21229,
    22033,
    22556,
    23244,
    23269,
    23368,
    23602,
    23767,
    23849,
    23925,
    24112,
    24245,
    24330,
    # 24621,
]

upload_folder = "scouting_data"  # Directory for where the folders are updated
download_folder = "processed_data"  # Directory where processed data is stored and where users download data

#
# Data-correction/Completion
#

auto_replace_team_names = False  # Enable autocorrect for invalid team numbers
team_number_threshold = 2  # Threshold for characters when finding team replacements

#
# Team Data Compilation
#

point_values = {
    "Does the team have a team prop?": {
        True: 20,
        False: 10,
    },
    "Robot Scores Purple Pixel on correct spike mark?": 10,
    "Robot Scores Yellow Pixel on Backdrop correctly?": 10,
    "Robot navigates to the backstage corners/center?": 5,
    "Number of scored Pixels. [Backstage]": 3,
    "Number of scored Pixels. [Backdrop]": 5,

    # Teleop
    "Scored Backstage Pixels": 1,
    "Scored Backdrop Pixels": 3,
    "De-scored Backstage Pixels": -1,
    "De-scored Backdrop Pixels": -3,
    # Endgame
    "Mosaics": 10,
    "Max Set Line": 10,
    "Parking": {
        None: 0,
        "Backstage": 5,
        "Rigging": 20,
    },
    "Drone Zones": {
        None: 0,
        1: 30,
        2: 20,
        3: 10,
    },
    "Minor": 10,
    "Major": 30,
}

data = {
    "Score": [
        {
            "header": "Avg Total",
            "operation": "AVERAGE",
            "fields": ["Final Alliance Score"],
        },
        {"header": "EPA", "operation": "EPA", "fields": "all"},
    ],
    "Autonomous": [
        {
            "header": "Avg Peices",
            "operation": "AVERAGE",
            "fields": ["Number of scored Pixels. [Backstage]", "Number of scored Pixels. [Backdrop]"],
        },
    ],
    "Teleop": [
        {
            "header": "Avg Peices",
            "operation": "AVERAGE",
            "fields": ["Scored Backstage Pixels", "Scored Backdrop Pixels"],
        },
        {
            "header": "Avg De-scored",
            "operation": "AVERAGE",
            "fields": ["De-scored Backstage Pixels", "De-scored Backdrop Pixels"],
        },
        
    ],
    "Endgame": [
        {
            "header": "Max Drone",
            "operation": "MAX_VALUE",
            "field": "Drone Zones",
            "values": [1, 2, 3],
            "default": None,
        },
        {
            "header": "Max Endgame State",
            "operation": "MAX_VALUE",
            "field": "Parking",
            "values": ["Rigging", "Backstage", None]
        }
    ]
}

# Options
#    1. AVERAGE
#    2. MAX
#    3. MAX_VALUE
#    4. STANDARD_DEV
#    5. EPA

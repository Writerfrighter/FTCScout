team_number = 3543  # Your team number
allowed_file_extensions = ["xlsx", "xlsx"]  # Used for data processing
teams = []
upload_folder = "scouting_data"  # Directory for where the folders are updated
download_folder = "processed_data"  # Directory where processed data is stored and where users download data

#
# Data-correction/Completion
#

auto_replace_team_names = True  # Enable autocorrect for invalid team numbers
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
    "Minor": 5,
    "Major": 10,
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
            "fields": ["Auto Scored Low", "Auto Scored Med", "Auto Scored High"],
        },
    ],
    "Teleop": [
        {
            "header": "Avg Peices",
            "operation": "AVERAGE",
            "fields": ["Teleop Goals Low", "Teleop Goals Med", "Teleop Goals High"],
        },
        {
            "header": "Avg Missed",
            "operation": "AVERAGE",
            "fields": ["Teleop Missed Attempts"],
        },
        {
            "header": "Max Level",
            "operation": "MAX",
            "fields": ["Teleop Goals High", "Teleop Goals Med", "Teleop Goals Low"],
            "values": ["High", "Mid", "Low"],
            "default": 0,
        },
    ],
}

# Options
#    1. AVERAGE
#    2. MAX
#    3. MAX_VALUE
#    4. STANDARD_DEV
#    5. EPA

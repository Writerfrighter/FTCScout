# External Imports
import pandas as pd
from numpy import nan
import os
import glob

# Local Imports
import params

def completeData(eventCode):
    """Completes scouting data using TBA data for the event"""
    df = pd.read_excel("{}\{}.xlsx".format(params.download_folder, eventCode))
    # eventMatches = TBA.fetchEventMatches(eventCode)

    for k, entry in enumerate(list(df.values)):
        # Check if the team numbers are correct
        if str(entry[1]) not in params.teams:
            team_replace = fixInvalidTeamNumber(
                str(entry[1]), df.loc[k, "Match Number"]
            )
            if not params.auto_replace_team_names:
                print(
                    "Invalid team number was found in match {}, team number {}, our algorithm has found a possible replacement of {}. Do you accept this change? (y/n)".format(
                        df.loc[k, "Match Number"], entry[1], team_replace
                    )
                )
                answer = input().lower()
            else:
                print(
                    "Wrong team number was found in match {}: Team number {}, replacement of {} was found. Autoaccept has been enabled.".format(
                        df.loc[k, "Match Number"], entry[1], team_replace
                    )
                )
            if params.auto_replace_team_names:
                df.loc[k, "Team Number"] = int(team_replace)
            elif answer == "y":
                df.loc[k, "Team Number"] = int(team_replace)
            else:
                df.loc[k, "Team Number"] = int(input("What is your replacement? \n"))


def fixInvalidTeamNumber(givenTeamNumber, matchKey):
    givenTeamNumber = str(givenTeamNumber)
    # data = TBA.fetchMatchData(matchKey)
    teams = params.teams

    matches = []
    for i in range(len(teams)):
        matches.append(0)
        teams[i] = teams[i][3::]
        for j in range(len(teams[i])):
            try:
                if teams[i][j] == givenTeamNumber[j]:
                    matches[i] += 1
            except:
                matches[i] -= 1
    if max(matches) >= params.team_number_threshold:
        return teams[matches.index(max(matches))]
    else:
        answer = input(
            "Bad team number in match {}, team number {}, a suggested chance of {} was found that does not meet the minimum threshold do you accept the change? (y/n)".format(
                matchKey, givenTeamNumber, teams[matches.index(max(matches))]
            )
        ).lower()
        if answer == "y":
            return teams[matches.index(max(matches))]
        else:
            raise ValueError(
                "Bad team number in match {}, team number {} fixInvalid could not identity the correct team number.".format(
                    matchKey, givenTeamNumber
                )
            )


def find_team(substring, data_file=None):
    df = ""
    if data_file == None:
        files = list(filter(os.path.isfile, glob.glob(params.download_folder + "\*")))
        files.sort(key=os.path.getctime)
        file = files[0]
        df = pd.read_excel(file)
    else:
        try:
            df = pd.read_excel(data_file)
        except:
            raise FileNotFoundError(
                "File at path {} not found, please use a valid local or global path".format(
                    data_file
                )
            )
    df = df[df["Team Number"].astype(str).str.contains(substring)]
    return list(set(df.loc[::, "Team Number"].values))


def get_team_data(team_number: int, data_file=None):
    result = {}
    if data_file == None:
        files = list(filter(os.path.isfile, glob.glob(params.download_folder + "\*")))
        files.sort(key=os.path.getctime)
        file = files[0]
        df = pd.read_excel(file)
    else:
        try:
            df = pd.read_excel(data_file)
        except:
            raise FileNotFoundError(
                "File at path {} not found, please use a valid local or global path".format(
                    data_file
                )
            )
    df = df.loc[df["Team Number"] == team_number]
    for catagory in params.data.keys():
        result[catagory] = {}
        for item in params.data[catagory]:
            if item["operation"] == "AVERAGE":
                val = 0
                for name in item["fields"]:
                    val += sum(df[name].tolist())
                result[catagory][item["header"]] = val / df.shape[0]
            elif item["operation"] == "MAX":
                for i in range(len(item["fields"])):  # name in item["fields"]:
                    if df[item["fields"][i]].tolist().count(item["default"]) != len(
                        df[item["fields"][i]].tolist()
                    ):
                        result[catagory][item["header"]] = item["values"][i]
                        break
                if result[catagory].get(item["header"]) == None:
                    result[catagory][item["header"]] == "None"
                    # Optional Nonetype replacement
            elif item["operation"] == "MAX_VALUE":
                pass
            elif item["operation"] == "STANDARD_DEV":
                pass
            elif item["operation"] == "EPA":
                result[catagory][item["header"]] = calculate_epa(
                    team_number, fields=item["fields"]
                )
            else:
                print("Unsupported opperation")
    return result


def calculate_epa(team_number: int, data_file=None, fields="all"):
    if data_file == None:
        files = list(filter(os.path.isfile, glob.glob(params.download_folder + "\*")))
        files.sort(key=os.path.getctime)
        file = files[0]
        df = pd.read_excel(file)
    else:
        try:
            df = pd.read_excel(data_file, true_values=["Yes", "True", "true", True], false_values=["No", "False", "false", False])
        except:
            raise FileNotFoundError(
                "File at path {} not found, please use a valid local or global path".format(
                    data_file
                )
            )
    df = df.loc[df["Team Number"] == team_number]
    df = df.replace(nan, None)
    if fields == "all":
        fields = list(params.point_values.keys())
    EPA = 0
    for field in fields:
        print(field)
        data_list = df[field].tolist()
        print(data_list[2])
        print(df.loc[::, field])
        field_type = type(data_list[0])
        
        if field_type == int or field_type == float:
            EPA += mean(data_list) * params.point_values[field]
        elif field_type == str:
            for i in range(len(data_list)):
                value = params.point_values[field].get(data_list[i])
                data_list[i] = value if value != None else 0
            EPA += mean(data_list)
        elif field_type == bool:
            if type(params.point_values[field]) == dict:
                for i in range(len(data_list)):
                    data_list[i] = params.point_values[field][data_list[i]]
            else:
                for i in range(len(data_list)):
                    data_list[i] = params.point_values[field] if data_list[i] else 0
            EPA += mean(data_list)
        else:
            print("Unsupported field type:", field_type)
        print(data_list)
    return EPA


def mean(list):
    return sum(list) / len(list)

print(calculate_epa(24621, "FTC Game Scouting Turing #2 (Responses).xlsx"))
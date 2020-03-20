import pandas as pd


def load_data(path=None):
    path = path or './eurovision_song_contest_1975_2019.xlsx'
    df = pd.read_excel(path, sheet_name='Data')

    # read the excel file to
    profiles_per_editions = {}
    for index, row in df.iterrows():
        edition = row['Edition']
        from_country = row['From country']
        to_country = row['To country']
        points = row['Points']

        if from_country == to_country:
            continue

        if edition not in profiles_per_editions:
            profiles_per_editions[edition] = {}

        if from_country in profiles_per_editions[edition]:
            profiles_per_editions[edition][from_country].append((to_country, points))
        else:
            profiles_per_editions[edition][from_country] = [(to_country, points)]

    # sort the votes to create a ballot
    final_profiles_per_editions = {}
    for edition in profiles_per_editions.keys():
        final_profiles_per_editions[edition] = {}
        for from_country, votes in profiles_per_editions[edition].items():
            final_profiles_per_editions[edition][from_country] = [to_country for to_country, score in sorted(votes, key=lambda p: p[1], reverse=True)]

    return final_profiles_per_editions


def print_profile(profile):
    for country, ballot in profile.items():
        print(f"{country}: {ballot}")

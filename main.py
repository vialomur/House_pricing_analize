import matplotlib
import pandas as pd
import quandl
import matplotlib.pyplot as plt
from matplotlib import style

matplotlib.use('TkAgg')
style.use("fivethirtyeight")

file_key = open("qunadl_key.txt", "r")
api_key = file_key.readline()
file_key.close()


def get_list_states():
    lst_df = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
    return lst_df


def get_states_data():
    states = get_list_states()
    main_df = pd.DataFrame()

    for i in range(len(states[0].values)):
        abbv = states[0].values[i][1]
        query = "FMAC/HPI_" + abbv

        df = quandl.get(query, api_key=api_key)
        df.rename(columns={'NSA Value': str(abbv) + ' NSA Value', 'SA Value': str(abbv) + ' SA Value'}, inplace=True)

        abbv_SA = str(abbv) + ' SA Value'
        abbv_NSA = str(abbv) + ' NSA Value'

        df[abbv_SA] = ((df[abbv_SA] - df[abbv_SA][0]) / df[abbv_SA][0]) * 100.0
        df[abbv_NSA] = ((df[abbv_NSA] - df[abbv_NSA][0]) / df[abbv_NSA][0]) * 100.0

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    main_df.to_pickle("data_frame.pickle")


def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", api_key=api_key)
    df["SA Value"] = ((df["SA Value"] - df["SA Value"][0]) / df["SA Value"][0]) * 100.0
    df["NSA Value"] = ((df["NSA Value"] - df["NSA Value"][0]) / df["NSA Value"][0]) * 100.0
    return df


# get_states_data()

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))

HPI_data = pd.read_pickle("data_frame.pickle")

HPI_data["TX1yr"] = HPI_data["TX SA Value"].resample("A").mean().reindex(HPI_data.index)
#HPI_data.dropna(inplace=True)
HPI_data.fillna(method="ffill", inplace=True)
print(HPI_data[["TX1yr", "TX SA Value"]])
HPI_data[["TX1yr", "TX SA Value"]].plot(ax=ax1)

plt.legend(loc=4)
plt.show()

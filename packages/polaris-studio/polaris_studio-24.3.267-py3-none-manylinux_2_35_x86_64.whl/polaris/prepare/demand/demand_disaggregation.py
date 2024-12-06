# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

from itertools import chain
from matplotlib import pyplot as plt
import numpy as np
import logging
import pandas as pd
from tqdm import tqdm
from polaris.utils.database.db_utils import read_and_close
from polaris.utils.pandas_utils import stochastic_round


def disaggregate_column(df, col_name, locations, chunksize=None):
    df = pd.DataFrame(df[["zone_origin", "zone_dest", col_name]])

    # Convert each row with "N" trips into N rows with 1 trip
    df[col_name] = stochastic_round(df[col_name])  # integerize the column first
    df = df.loc[df.index.repeat(df[col_name])]
    df = df.reset_index(drop=True).reset_index().rename(columns={"index": "trip_id"})

    def f(df_, i):

        # Do an inner join to locations on both the origin and destination to get the cross product DF
        df_ = pd.merge(df_, locations, left_on="zone_origin", right_on="zone", how="inner")
        df_ = df_.drop(columns="zone").rename(columns={"location": "origin_location"})
        df_ = pd.merge(df_, locations, left_on="zone_dest", right_on="zone", how="inner")
        df_ = df_.drop(columns="zone").rename(columns={"location": "dest_location"})

        # Finally drop the origin and destination zone and just pick a random o/d location for each trip_id
        df_ = df_.drop(columns=["zone_origin", "zone_dest", col_name])
        df_ = df_.groupby("trip_id").apply(lambda x: x.sample(1)).reset_index(drop=True)

        return df_

    # Go through the trips in chunks
    chunksize = chunksize or df.shape[0]
    rv = pd.concat(f(df[i : i + chunksize], i) for i in tqdm(range(0, df.shape[0], chunksize)))

    # Find trips that can't be matched to a location
    missing_ids = set.difference(set(df.trip_id.unique()), set(rv.trip_id.unique()))
    if missing_ids:
        logging.info(f"There were {len(missing_ids)} trips to/from a zone with no appropriate locations")

    return rv


def load_crosswalk(csv_file):
    df = pd.read_csv(csv_file)
    assert "TAZ" in df.columns
    assert "zone" in df.columns
    return df


def load_locations(supply_db, disallowed_lu_types=None):

    disallowed_lu_types = (
        disallowed_lu_types if disallowed_lu_types is not None else ["RESIDENTIAL-SINGLE", "RESIDENTIAL-MULTI"]
    )

    sql = "SELECT location, zone, land_use FROM Location"
    if disallowed_lu_types:
        types = ",".join([f"'{t}'" for t in disallowed_lu_types])
        sql += f" WHERE land_use NOT IN ({types})"

    with read_and_close(supply_db) as conn:
        df = pd.read_sql_query(sql, conn)
        assert df.shape[0] > 0
        return df


def plot_temporal_dist(df, label):
    df = df.copy()
    df["hour"] = round(df.minute / 60.0, 1)
    plt.gca().plot(df.hour, 60.0 * df.proportion, label=label)


def assign_random_start_time(trips, temporal_dist):

    minutes_in_day = list(range(0, 24 * 60))
    assert len(minutes_in_day) == temporal_dist.shape[0], f"{len(minutes_in_day)} != {temporal_dist.shape[0]}"
    trips["start_min"] = np.random.choice(minutes_in_day, size=trips.shape[0], p=temporal_dist.proportion)
    trips["start_sec"] = 60 * trips.start_min + np.random.choice(list(range(0, 60)), size=trips.shape[0])
    return trips


def subset_temporal_dist(df, hour_ranges):
    minutes_to_keep = list(chain.from_iterable(list(range(int(r[0] * 60), int(r[1] * 60))) for r in hour_ranges))
    df = df.copy()
    df.loc[~df.minute.isin(minutes_to_keep), "proportion"] = 0
    df["proportion"] = df["proportion"] / df["proportion"].sum()
    return df


def translate_period_proportion_to_hourly(df):
    """
    Converts a dataframe with proportions specified by start/end hour into a dataframe
    with a proportion for each individual hour.
    """

    assert sorted(df.columns) == [
        "end_hour",
        "proportion",
        "start_hour",
    ], f"input df has incorrect headers, {df.columns}"

    df["minute"] = df.apply(lambda r: list(range(int(r["start_hour"] * 60), int(r["end_hour"] * 60))), axis=1)
    df["proportion"] = df.proportion.astype(float) / (df.end_hour - df.start_hour).astype(float)
    df = df.explode("minute")[["proportion", "minute"]]  # .rename(columns={"mintu": "hour"})
    # assert list(range(0, 24)) == list(df.hour.unique())

    df["proportion"] = df["proportion"] / df["proportion"].sum()
    return df

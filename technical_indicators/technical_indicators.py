import pandas as pd
import numpy as np


def calculate_macd(close_prices, short_range=12, long_range=26, signal_range=9):
    """calculate macd"""
    short_EMA = close_prices.ewm(span=short_range, adjust=False).mean()
    long_EMA = close_prices.ewm(span=long_range, adjust=False).mean()
    macd = short_EMA - long_EMA
    signal = macd.ewm(span=signal_range, adjust=False).mean()
    return macd, signal


def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    avg_gain = up.rolling(window=period).mean()
    avg_loss = abs(down.rolling(window=period).mean())
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def long_df(df):
    """group by Instrument and Datetime to get long format of data"""
    return df.pivot_table(
        index=["Datetime", "Instrument"],
        columns="Price type",
        values="Price",
        aggfunc="mean",
    ).reset_index()


def add_technical_indicators(df):
    """add technical indicators to dataframe"""
    for instrument in df.Instrument.unique():
        # log ret in price 1d, 5d, 8d, 13d
        for i in [1, 5, 8, 13]:
            df.loc[df.Instrument == instrument, f"log_ret_{i}d"] = np.log(
                df.loc[df.Instrument == instrument, "Close"]
                / df.loc[df.Instrument == instrument, "Close"].shift(i)
            )
        # sma of log ret in price 1d, 5d, 8d, 13d
        # for i in [1, 5, 8, 13]:
        #     df.loc[df.Instrument == instrument, f"std_log_ret_{i}d"] = (
        #         df.loc[df.Instrument == instrument, f"log_ret_{i}d"].rolling(i).mean()
        #     )
        for i in [1, 5, 8, 13]:
            df.loc[df.Instrument == instrument, f"ewm_log_ret_{i}d"] = (
                df.loc[df.Instrument == instrument, f"log_ret_{i}d"].ewm(span=i).mean()
            )
        # macd
        macd, macd_sig = calculate_macd(df.loc[df.Instrument == instrument, "Close"])
        df.loc[df.Instrument == instrument, "macd"] = macd
        df.loc[df.Instrument == instrument, "macd_sig"] = macd_sig
        # macd slopes
        df.loc[df.Instrument == instrument, "macd_slope"] = df.loc[
            df.Instrument == instrument, "macd"
        ] - df.loc[df.Instrument == instrument, "macd"].shift(9)
        # rsi
        df.loc[df.Instrument == instrument, "rsi"] = calculate_rsi(
            df.loc[df.Instrument == instrument, "Close"], 14
        )
        # rsi slopes
        df.loc[df.Instrument == instrument, "rsi_slope"] = df.loc[
            df.Instrument == instrument, "rsi"
        ] - df.loc[df.Instrument == instrument, "rsi"].shift(9)

        # labels
        for i in [1, 5, 8, 13]:
            # positive returns
            df.loc[
                (df.Instrument == instrument) & (df[f"log_ret_{i}d"] > 0), f"label_{i}d"
            ] = 3
            # positive less than ewm
            df.loc[
                (df.Instrument == instrument)
                & (df[f"log_ret_{i}d"] > 0)
                & (df[f"log_ret_{i}d"] < df[f"ewm_log_ret_{i}d"]),
                f"label_{i}d",
            ] -= 1
            # negative returns
            df.loc[
                (df.Instrument == instrument) & (df[f"log_ret_{i}d"] < 0), f"label_{i}d"
            ] = 0
            # negative less than ewm
            df.loc[
                (df.Instrument == instrument)
                & (df[f"log_ret_{i}d"] < 0)
                & (np.abs(df[f"log_ret_{i}d"]) < df[f"ewm_log_ret_{i}d"]),
                f"label_{i}d",
            ] += 1

    return df


def flatten_byDatetime(df):
    """flatten dataframe by Datetime to serve as features for ml"""
    df_pivot = df.pivot(index="Datetime", columns="Instrument")

    # Flatten the multi-level column index
    df_pivot.columns = ["_".join(col).strip() for col in df_pivot.columns.values]

    # Reset the index to make 'Datetime' a column again
    df_pivot.reset_index(inplace=True)

    return df_pivot

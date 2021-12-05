import asyncio
import pandas as pd
import os
import json

import sys
sys.path.append("drift-py/")

os.environ["ANCHOR_WALLET"] = './.config/solana/id.json'

from drift.drift import Drift, load_config, MARKET_INDEX_TO_PERP


def drift_py():
    USER_AUTHORITY = ""
    drift = Drift(USER_AUTHORITY)
    asyncio.run(drift.load())
    return drift


def drift_history_df(drift):
    history_df = asyncio.run(drift.load_history_df())
    return history_df


if __name__ == '__main__':
    drift = drift_py()
    df_dict = drift_history_df(drift)
    os.makedirs('data/', exist_ok=True)

    with open('data/config.json','w') as f:
        json.dump({'last_update': str(drift.last_update)}, f)

    markets = drift.market_summary()
    markets.to_csv("data/markets_state.csv")

    users = drift.user_summary()
    users.to_csv("data/users_state.csv")    

    positions = drift.user_position_summary()
    users.to_csv("data/positions_state.csv")    

    for key, df in df_dict.items():
        df.to_csv('data/%s_history.csv' % str(key))

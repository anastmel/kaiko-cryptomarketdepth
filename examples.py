 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 0xanastasia
"""
# Import the module with the functions
# It should be located in the same directory as this script
import kaiko_depth as kk
from apikeys import *




### MARKET DEPTH BY MARKET : PAIR + EXCHANGE #############################

# Get the data 
market = kk.market_depth(apikey=apikey_kaiko, 
                     start_time='2023-01-21T00:00:00Z', 
                     end_time='2023-01-21T01:00:59Z',
                     instrument='eth-usd',
                     exchanges=['cbse', 'krkn', 'bnus'],
                     interval="1m",
                     instrument_class='spot')


# Create a line chart comparing the market depth of a given pair across different exchanges
kk.market_depth_chart(market, values='bid_volume0_2', file_name="market_depth_chart.jpeg", show=True)

# Create a heatmap of the market depth across pair/exchange markets at different depth levels
kk.market_heatmap(market, file_name="heatmap_market.jpeg", show=True)






### MARKET DEPTH BY ASSET #############################

# Get the data
asset = kk.asset_depth(apikey=apikey_kaiko, 
                     start_time='2023-01-21T00:00:00Z', 
                     end_time='2023-01-21T00:30:59Z',
                     base_asset='eth',
                     exchanges=['cbse','krkn', 'binc'],
                     instrument_class='spot', 
                     interval="1m",
                     # default : quote_assets=['usd', 'usdt','usdc']
                     quote_assets=['usd', 'usdt', 'dai'])

# Create a line chart comparing the market depth of an asset across several markets
kk.asset_depth_chart(asset, values='bid_volume0_2', file_name="asset_depth_chart.jpeg", show=True)

# Create a heatmap of the market depth for one asset acorss exchanges, at different depth levels
kk.asset_heatmap(asset, file_name="heatmap_asset.jpeg", show=True)






# Crypto Market Depth, the python module (by Kaiko)
A Python module that allows users to leverage Kaiko's market depth data for centralized crypto exchanges.

The module `kaiko_depth.py` provides functions to easily get data, chart it, and create heatmaps that show how liquidity is distributed across different exchanges' orderbooks and price levels, both on bid and ask sides. It also helps users to identify which exchange provides the most liquidity and the least slippage for a given market (example: ETH-USD) or a cryptoasset (example: ETH).

## Installation 
Python module with all the functions is the file named `kaiko_depth.py`. To make sure you can use its functions, you need to put it in your working directory. You can then import the module in any script and use the functions. 
```python
import kaiko_depth as kk
```
## Example of Usage

### Looking at a cryptocurrency pair 

#### Get the market depth 

To access the comparative market depth of a cryptocurrency pair, such as ETH-USD, on Coinbase and Kraken, you can use the `market_depth()` function provided by the CryptoExchangeDepth module. To use this function, you will need to provide your Kaiko API key, which you can obtain by filling out the form on Kaiko's website. Once you have your API key, you can specify the start and end time of your data request in ISO format, the instrument (i.e. the pair you are interested in), the exchanges you want to retrieve data from, and the instrument class (e.g. spot, future, perpetual-future, or option).

Please note that it is important to ensure that the instruments (pair + exchange) you are requesting are actually listed. You can find a list of all pairs listed on all cryptocurrency exchanges on the Kaiko Instruments webpage.

```python
import kaiko_depth as kk

df = kk.market_depth(apikey='your_api_key_here', 
                     start_time='2023-01-21T00:00:00Z', 
                     end_time='2023-01-21T01:00:59Z',
                     instrument='eth-usd',
                     exchanges=['cbse', 'krkn', 'bnus'],
                     instrument_class='spot')
```
#### Chart market depth across exchanges

The module provides a simple way to chart the market depth at a selected side (bid or ask) and a specific depth level in percentage, using the `market_depth_chart()` function. The depth of an orderbook is represented by the cumulative volume of the base asset at levels of 0.1%, 0.2%, 0.3%, 0.4%, 0.5%, 0.6%, 0.7%, 0.8%, 0.9%, 1%, 1.5%, 2%, 4%, 6%, 8% and 10% from the best ask and best bid respectively.

The following example illustrates how to use the `market_depth_chart()` function to examine the market depth on the bid side across the selected exchanges, at a depth of 0.2% with respect to the best bid and best ask. The volume in always expresse in base currency, here ETH. 

```python
kk.market_depth_chart(market, 'bid_volume0_2')
```
The outputed chart looks like this : 





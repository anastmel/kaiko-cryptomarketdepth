# Crypto Market Depth, the python module (by Kaiko)
A Python module that allows users to leverage Kaiko's market depth data from centralized crypto exchanges, and feed smart contracts or token liquidity analytics. 

The module `kaiko_depth.py` provides functions to easily get data, chart it, create heatmaps that show how liquidity is distributed across different exchanges or tokens, and generate fully actionable data to feed smart contract and automate decision making based on reliable liquidity data provided by Kaiko. 

## Installation 
The python module with all the functions is the file named `kaiko_depth.py`. To make sure you can use its functions, you need to put it in your working directory. You can then import the module in any script and use the functions. 
```python
import kaiko_depth as kk
```

## Get symbols for supported exchanges

To get a list of the exchanges Kaiko supports and their symbols, see [this page](https://docs.kaiko.com/#exchanges).

## Get the market depth

To access the comparative market depth of a cryptocurrency pair, such as ETH-USD, on Coinbase and Kraken, you can use the `market_depth()` function provided by the CryptoExchangeDepth module. To use this function, you will need to provide your Kaiko API key, which you can obtain by filling out the form on Kaiko's website. Once you have your API key, you can specify the start and end time of your data request in ISO format, the instrument (i.e. the pair you are interested in), the exchanges you want to retrieve data from, and the instrument class (e.g. spot, future, perpetual-future, or option).

Please note that it is important to ensure that the instruments (pair + exchange) you are requesting are actually listed. You can find a list of all pairs listed on all cryptocurrency exchanges on the Kaiko Instruments webpage.

```python
df = kk.market_depth(apikey='your_api_key_here', 
                     start_time='2023-01-21T00:00:00Z', 
                     end_time='2023-01-21T01:00:59Z',
                     instrument='eth-usd',
                     exchanges=['cbse', 'krkn'],
                     instrument_class='spot')
```

## Example of Usage : How liquid is ETH compared to BTC

To access the comparative market depth of a cryptocurrency, such as ETH with BTC or any other cryptocurrency, taken from certain exchanges, you can use the `assets_depth()` function of the module. The default exchanges used are the top 10 most liquid exchanges according to [Kaiko's proprietary liquidity scoring methodology](https://www.kaiko.com/pages/exchange-ranking), and the default quote assets are the most liquid stable assets (USD, USDT, DAI, BUSD, and USDC), but you can include additional quote assets as well. There are many different quote assets to consider for a single base asset's liquidity, including blue-chip assets like BTC and ETH, that a protocol could employ; to stay on the conservative side, our default code limits the quote assets to the largest stablecoins.

Thanks to the create_json() function you can export the fully aggregated result by cryptocurrency, in a json format as shown below. You can choose to get this liquidity expressed in your assets unit or in USD thanks to a simple parameter. 

```python
df = kk.assets_depth(apikey='your_api_key_here', 
                     start_time='2023-02-05T00:00:00Z', 
                     end_time='2023-02-08T00:00:00Z',
                     assets=['eth', 'btc'],
                     exchanges=['cbse','krkn'] # default TOP 10 CEXs according to Kaiko Exchange Ranking : https://www.kaiko.com/pages/exchange-ranking exchanges=['krkn','cbse', 'stmp', 'bnus', 'binc', 'gmni', 'btrx', 'itbi', 'huob', 'btba']
                     instrument_class='spot', 
                     quote_assets=['usd','usdt','dai'] # default : quote_assets=['usd', 'usdt', 'usdc', 'dai', 'busd']
                     interval='1d')
                     
depth_results = kk.create_json(df, 'depth_results.json', usd=False)
```

```json
[{
	"btc": {
		"bid_volume0_1": 16.7482551735,
		"bid_volume0_2": 34.5501754382,
		"bid_volume0_3": 49.5365447891,
		"bid_volume0_4": 66.7045709444,
		"bid_volume0_5": 82.5017979636,
		"bid_volume0_6": 92.6392662523,
		"bid_volume0_7": 102.6195668302,
		"bid_volume0_8": 109.7169341836,
		"bid_volume0_9": 115.4954229915,
		"bid_volume1": 120.7994288127,
		"bid_volume1_5": 140.7090008651,
		"bid_volume2": 151.7659178899,
		"bid_volume4": 168.2382406089,
		"bid_volume6": 177.4832565466,
		"bid_volume8": 186.2163923501,
		"bid_volume10": 202.9063020315,
		"ask_volume0_1": 17.4204225631,
		"ask_volume0_2": 34.8038365497,
		"ask_volume0_3": 48.3797373838,
		"ask_volume0_4": 64.3110720726,
		"ask_volume0_5": 80.0302954201,
		"ask_volume0_6": 90.7202434723,
		"ask_volume0_7": 102.2947383194,
		"ask_volume0_8": 109.6534839299,
		"ask_volume0_9": 115.839209255,
		"ask_volume1": 121.9345856949,
		"ask_volume1_5": 136.4505837766,
		"ask_volume2": 144.6291733767,
		"ask_volume4": 157.7176369177,
		"ask_volume6": 168.7699670691,
		"ask_volume8": 185.640196348,
		"ask_volume10": 206.1208593042
	},
	"eth": {
		"bid_volume0_1": 126.8498307824,
		"bid_volume0_2": 278.2420115734,
		"bid_volume0_3": 416.4212087288,
		"bid_volume0_4": 567.9821557265,
		"bid_volume0_5": 714.5145193583,
		"bid_volume0_6": 814.8814396563,
		"bid_volume0_7": 899.495087891,
		"bid_volume0_8": 972.3278915629,
		"bid_volume0_9": 1027.0515507694,
		"bid_volume1": 1075.2486887086,
		"bid_volume1_5": 1251.0644402337,
		"bid_volume2": 1480.1523777707,
		"bid_volume4": 2156.9824906248,
		"bid_volume6": 2619.6091270626,
		"bid_volume8": 2749.8508791676,
		"bid_volume10": 2839.2753963512,
		"ask_volume0_1": 129.2197854587,
		"ask_volume0_2": 277.4135905273,
		"ask_volume0_3": 397.8959379245,
		"ask_volume0_4": 533.9342554196,
		"ask_volume0_5": 674.6145302331,
		"ask_volume0_6": 768.7896606936,
		"ask_volume0_7": 853.6979431363,
		"ask_volume0_8": 920.1093034535,
		"ask_volume0_9": 964.8815684735,
		"ask_volume1": 1000.4175172021,
		"ask_volume1_5": 1137.9688472657,
		"ask_volume2": 1325.6228715742,
		"ask_volume4": 1899.0836652647,
		"ask_volume6": 2240.8783479793,
		"ask_volume8": 2301.5578616548,
		"ask_volume10": 2358.6740544248
	}
}]
```
This module also provides you with tools to vizualize liquidity across assets or markets. For example, using the `asseets_heatmap()` function you can obtain a comparative view on how market depth is distributed for different price levels of each selected asset. For example, the heatmap below shows that BTC has higher liquidity than ETH on the top 10 most liquid cryptocurrency exchanges. It also shows that BTC's liquidity is spread across the widest range of price levels for both buy and sell orders, while ETH's liquidity is more concentrated. The liquidity of each asset is measured in USD in the heatmap for easy comparison.

![Alt text](https://github.com/anastmel/kaiko-cryptomarketdepth/blob/main/images/chart3.png)


For a more detailed example, see the included notebooks in the examples folder. This folder contains three examples, each for a precise granularity: 
- The first one called `instrument-kaiko-depth.ipynb`, explains how to get, chart, and analyze, the markets depth by instrument (pair+exchange)
- The second one called `asset-exchange-kaiko-depth.ipynb` explains how to get, chart, and analyze, the markets depth for one single asset, aggregated across a selection of exchanges. The view given is a comparative view by exchange. 
- The third one, called `asset-kaiko-depth.ipynb` explains how to get, chart, and analyze, the market depth for a list of selected assets. This one is the one used for the example above. 

For additional information regarding the Kaiko endpoint utilized in the repository and module, please refer to the Kaiko REST API documentation provided here : https://docs.kaiko.com/#order-book-aggregations-full. 

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


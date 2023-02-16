import pandas as pd
import requests
import matplotlib.pyplot as plt

# Instrument Level
# Carefull, the history available here is limited to one month (rolling)
def market_depth(apikey, start_time, end_time, instrument, exchanges, interval, instrument_class='spot'):
    headers = {'Accept': 'application/json',
               'X-Api-Key': apikey}
    df_list = []
    for exchange in exchanges:
        try:
            url = f'https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/{exchange}/{instrument_class}/{instrument}/ob_aggregations/full?start_time={start_time}&end_time={end_time}&interval={interval}'
            res = requests.get(url, headers=headers)
            df = pd.DataFrame(res.json()['data'])
            df['pair'] = (instrument)
            df['exchange'] = (exchange)
            while 'next_url' in res.json():
                res = requests.get(res.json()['next_url'], headers=headers)
                data =  pd.DataFrame(res.json()['data'])
                data['pair'] = (instrument)
                data['exchange'] = (exchange)
                df = pd.concat([df,data], ignore_index=True)
        except:
            print('not available: ' + str(exchange) + ' / ' +str(instrument))
        df_list.append(df)
    final_df = pd.concat(df_list)
    final_df['poll_date'] = pd.to_datetime(final_df['poll_timestamp'], unit='ms')
    return final_df


def market_depth_chart(df, values):
    # Combine the exchange and pair columns to create a new label column
    df['label'] = df['exchange'] + '-' + df['pair']
    # Pivot the dataframe to aggregate the 'values'
    pivot_df = df.pivot_table(values=values, index='poll_date', columns='label')
    # Interpolate missing values
    pivot_df.interpolate(method='linear', axis=0, inplace=True)
    # Create a new figure and axis
    plt.figure(figsize=(10,6))
    ax = plt.gca()
    # Plot the line chart
    pivot_df.plot(ax=ax)
    # Add title and labels
    plt.title(values.capitalize() + " depth by pair & exchange")
    plt.xlabel("Date")
    plt.ylabel(values)
    plt.xticks(rotation=60)
    plt.legend()
    # Show the chart
    plt.show()

def market_heatmap(df, file_name):
    # Combine the exchange and pair columns to create a new label column
    df['label'] = df['exchange'] + '-' + df['pair']
    cols = ['bid_volume0_1','bid_volume0_2', 'bid_volume0_3', 'bid_volume0_4', 'bid_volume0_5',
           'bid_volume0_6', 'bid_volume0_7', 'bid_volume0_8', 'bid_volume0_9',
           'bid_volume1', 'bid_volume1_5', 'bid_volume2', 'bid_volume4',
           'bid_volume6', 'bid_volume8', 'bid_volume10', 'ask_volume0_1',
           'ask_volume0_2', 'ask_volume0_3', 'ask_volume0_4', 'ask_volume0_5',
           'ask_volume0_6', 'ask_volume0_7', 'ask_volume0_8', 'ask_volume0_9',
           'ask_volume1', 'ask_volume1_5', 'ask_volume2', 'ask_volume4',
           'ask_volume6', 'ask_volume8', 'ask_volume10']
    # convert columns to numeric
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    # group by exchange and compute the mean
    df = df.groupby('label')[cols].mean()
    # Transpose the dataframe
    df = df.T
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    # Create a heatmap of the dataframe values
    im = ax.imshow(df, cmap='YlGnBu')
    # Add a colorbar
    fig.colorbar(im)
    # Add labels to the x and y axis
    ax.set_xticks(range(df.shape[1]))
    ax.set_yticks(range(df.shape[0]))
    ax.set_xticklabels(df.columns)
    ax.set_yticklabels(df.index)
    # Add a title to the heatmap
    plt.title("market depth by pair & exchange")
    # Rotate the x-axis labels
    plt.xticks(rotation=70)
    # Save the plot
    plt.savefig(file_name, format='jpeg')
    # Show the plot
    plt.show()







# Asset Level / exchange granularity

def asset_depth(apikey, start_time, end_time, base_asset, exchanges, interval, quote_assets=['usd', 'usdt', 'usdc', 'dai', 'busd'], instrument_class='spot'):
    headers = {'Accept': 'application/json',
               'X-Api-Key': apikey}
    df_list = []
    for quote_asset in quote_assets:
        instrument = f"{base_asset}-{quote_asset}"
        for exchange in exchanges:
            try:
                url = f'https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/{exchange}/{instrument_class}/{instrument}/ob_aggregations/full?start_time={start_time}&end_time={end_time}&interval={interval}'
                res = requests.get(url, headers=headers)
                df = pd.DataFrame(res.json()['data'])
                df['pair'] = (instrument)
                df['exchange'] = (exchange)
                while 'next_url' in res.json():
                    res = requests.get(res.json()['next_url'], headers=headers)
                    data =  pd.DataFrame(res.json()['data'])
                    data['pair'] = (instrument)
                    data['exchange'] = (exchange)
                    df = pd.concat([df,data], ignore_index=True)
            except:
                print('no instrument found')
            df_list.append(df)    
    final_df = pd.concat(df_list)
    final_df['poll_date'] = pd.to_datetime(final_df['poll_timestamp'], unit='ms')
    def convert_to_numeric(df, column_list):
        for column in column_list:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        return df
    columns_to_convert = ['bid_volume0_1','bid_volume0_2', 'bid_volume0_3', 'bid_volume0_4', 'bid_volume0_5',
           'bid_volume0_6', 'bid_volume0_7', 'bid_volume0_8', 'bid_volume0_9',
           'bid_volume1', 'bid_volume1_5', 'bid_volume2', 'bid_volume4',
           'bid_volume6', 'bid_volume8', 'bid_volume10', 'ask_volume0_1',
           'ask_volume0_2', 'ask_volume0_3', 'ask_volume0_4', 'ask_volume0_5',
           'ask_volume0_6', 'ask_volume0_7', 'ask_volume0_8', 'ask_volume0_9',
           'ask_volume1', 'ask_volume1_5', 'ask_volume2', 'ask_volume4',
           'ask_volume6', 'ask_volume8', 'ask_volume10']
    final_df = convert_to_numeric(final_df, columns_to_convert)
    return final_df


def asset_depth_chart(df, values):
    # Pivot the dataframe to aggregate the 'values'
    pivot_df = df.pivot_table(values=values, index='poll_date', columns='exchange')
    # Interpolate missing values
    pivot_df.interpolate(method='linear', axis=0, inplace=True)
    # Create a new figure and axis
    plt.figure(figsize=(15,6))
    ax = plt.gca()
    # Plot the line chart
    pivot_df.plot(ax=ax)
    # Add the sum line to the chart
    plt.plot(pivot_df.sum(axis=1), label='Total', color='black')
    # Add title and labels
    plt.title(values.capitalize() + " depth by exchange")
    plt.xlabel("Date")
    plt.ylabel(values)
    plt.xticks(rotation=60)
    plt.legend()
    # Show the chart
    plt.show()

def asset_heatmap(df, file_name):
    
    cols = ['bid_volume0_1','bid_volume0_2', 'bid_volume0_3', 'bid_volume0_4', 'bid_volume0_5',
           'bid_volume0_6', 'bid_volume0_7', 'bid_volume0_8', 'bid_volume0_9',
           'bid_volume1', 'bid_volume1_5', 'bid_volume2', 'bid_volume4',
           'bid_volume6', 'bid_volume8', 'bid_volume10', 'ask_volume0_1',
           'ask_volume0_2', 'ask_volume0_3', 'ask_volume0_4', 'ask_volume0_5',
           'ask_volume0_6', 'ask_volume0_7', 'ask_volume0_8', 'ask_volume0_9',
           'ask_volume1', 'ask_volume1_5', 'ask_volume2', 'ask_volume4',
           'ask_volume6', 'ask_volume8', 'ask_volume10']
    # convert columns to numeric
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    # group by exchange and compute the average
    df = df.groupby('exchange')[cols].mean()
    # Transpose the dataframe
    df = df.T
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    # Create a heatmap of the dataframe values
    im = ax.imshow(df, cmap='YlGnBu')
    # Add a colorbar
    fig.colorbar(im)
    # Add labels to the x and y axis
    ax.set_xticks(range(df.shape[1]))
    ax.set_yticks(range(df.shape[0]))
    ax.set_xticklabels(df.columns)
    ax.set_yticklabels(df.index)
    # Add a title to the heatmap
    plt.title("Selected asset's market depth by exchange")
    # Rotate the x-axis labels
    plt.xticks(rotation=70)
    # Save the plot
    plt.savefig(file_name, format='jpeg')
    # Show the plot
    plt.show()









## BY ASSET only 

def assets_depth(apikey, start_time, end_time, assets, instrument_class, interval, exchanges=['krkn','cbse', 'stmp', 'bnus', 'binc', 'gmni', 'btrx', 'itbi', 'huob', 'btba'], quote_assets=['usd', 'usdt', 'usdc', 'dai', 'busd']):
    headers = {'Accept': 'application/json',
               'X-Api-Key': apikey}
    df_list = []
    for base_asset in assets:     
        for quote_asset in quote_assets:
            instrument = f"{base_asset}-{quote_asset}"
            for exchange in exchanges:
                try:
                    url = f'https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/{exchange}/{instrument_class}/{instrument}/ob_aggregations/full?start_time={start_time}&end_time={end_time}&interval={interval}'
                    res = requests.get(url, headers=headers)
                    df = pd.DataFrame(res.json()['data'])
                    df['pair'] = (instrument)
                    df['exchange'] = (exchange)
                    while 'next_url' in res.json():
                        res = requests.get(res.json()['next_url'], headers=headers)
                        data =  pd.DataFrame(res.json()['data'])
                        data['pair'] = (instrument)
                        data['exchange'] = (exchange)
                        df = pd.concat([df,data], ignore_index=True)
                except:
                    print('no instrument found')
                df_list.append(df)    
    final_df = pd.concat(df_list)
    final_df['poll_date'] = pd.to_datetime(final_df['poll_timestamp'], unit='ms')
    def convert_to_numeric(df, column_list):
        for column in column_list:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        return df
    columns_to_convert = ['bid_volume0_1','bid_volume0_2', 'bid_volume0_3', 'bid_volume0_4', 'bid_volume0_5',
           'bid_volume0_6', 'bid_volume0_7', 'bid_volume0_8', 'bid_volume0_9',
           'bid_volume1', 'bid_volume1_5', 'bid_volume2', 'bid_volume4',
           'bid_volume6', 'bid_volume8', 'bid_volume10', 'ask_volume0_1',
           'ask_volume0_2', 'ask_volume0_3', 'ask_volume0_4', 'ask_volume0_5',
           'ask_volume0_6', 'ask_volume0_7', 'ask_volume0_8', 'ask_volume0_9',
           'ask_volume1', 'ask_volume1_5', 'ask_volume2', 'ask_volume4',
           'ask_volume6', 'ask_volume8', 'ask_volume10', 'mid_price']
    final_df = convert_to_numeric(final_df, columns_to_convert)
    return final_df

def create_json(df, filename, usd=False):
    cols = ['bid_volume0_1','bid_volume0_2', 'bid_volume0_3', 'bid_volume0_4', 'bid_volume0_5',
               'bid_volume0_6', 'bid_volume0_7', 'bid_volume0_8', 'bid_volume0_9',
               'bid_volume1', 'bid_volume1_5', 'bid_volume2', 'bid_volume4',
               'bid_volume6', 'bid_volume8', 'bid_volume10', 'ask_volume0_1',
               'ask_volume0_2', 'ask_volume0_3', 'ask_volume0_4', 'ask_volume0_5',
               'ask_volume0_6', 'ask_volume0_7', 'ask_volume0_8', 'ask_volume0_9',
               'ask_volume1', 'ask_volume1_5', 'ask_volume2', 'ask_volume4',
               'ask_volume6', 'ask_volume8', 'ask_volume10']
    df[['base', 'quote']] = df['pair'].str.split("-", expand=True)
    if usd:
        df[cols] = df[cols].mul(df['mid_price'], axis=0)
    df = df.groupby('base')[cols].mean()
    data = df.to_json(orient="index")
    with open(filename, "w") as f:
        f.write(data)
    return data

def assets_heatmap(df, file_name):
    
    # multiply desired columns with mid_price
    cols = ['bid_volume0_1', 'bid_volume0_2', 'bid_volume0_3', 'bid_volume0_4', 'bid_volume0_5',
            'bid_volume0_6', 'bid_volume0_7', 'bid_volume0_8', 'bid_volume0_9',
            'bid_volume1', 'bid_volume1_5', 'bid_volume2', 'bid_volume4',
            'bid_volume6', 'bid_volume8', 'bid_volume10', 'ask_volume0_1',
            'ask_volume0_2', 'ask_volume0_3', 'ask_volume0_4', 'ask_volume0_5',
            'ask_volume0_6', 'ask_volume0_7', 'ask_volume0_8', 'ask_volume0_9',
            'ask_volume1', 'ask_volume1_5', 'ask_volume2', 'ask_volume4',
            'ask_volume6', 'ask_volume8', 'ask_volume10']
    df[cols] = df[cols].multiply(df['mid_price'], axis=0)

    # group by base and calculate the mean of the desired columns
    df = df.groupby('base')[cols].mean()
    
    # Transpose the dataframe
    df = df.T
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a heatmap of the dataframe values
    im = ax.imshow(df, cmap='YlGnBu')
    
    # Add a colorbar
    fig.colorbar(im)
    
    # Add labels to the x and y axis
    ax.set_xticks(range(df.shape[1]))
    ax.set_yticks(range(df.shape[0]))
    ax.set_xticklabels(df.columns)
    ax.set_yticklabels(df.index)
    
    # Add a title to the heatmap
    plt.title("Assets Market Depth")
    
    # Rotate the x-axis labels
    plt.xticks(rotation=70)
    
    # Save the plot
    plt.savefig(file_name, format='jpeg')
    
    # Show the plot
    plt.show()


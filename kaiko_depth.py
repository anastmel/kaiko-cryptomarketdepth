import pandas as pd
import requests
import matplotlib.pyplot as plt

# Instrument Level

def market_depth(apikey, start_time, end_time, instrument, exchanges, instrument_class):
    headers = {'Accept': 'application/json',
               'X-Api-Key': apikey}
    df_list = []
    for exchange in exchanges:
        url = f'https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/{exchange}/{instrument_class}/{instrument}/snapshots/full?start_time={start_time}&end_time={end_time}'
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f'Error: {res.status_code}')
            continue
        df = pd.DataFrame(res.json()['data'])
        df['pair'] = (instrument)
        df['exchange'] = (exchange)
        while 'next_url' in res.json():
            res = requests.get(res.json()['next_url'], headers=headers)
            if res.status_code != 200:
                print(f'Error: {res.status_code}')
                continue
            data =  pd.DataFrame(res.json()['data'])
            data['pair'] = (instrument)
            data['exchange'] = (exchange)
            df = pd.concat([df,data], ignore_index=True)
        df_list.append(df)
    final_df = pd.concat(df_list)
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
    # group by exchange and sum
    df = df.groupby('label')[cols].sum()
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
    
    
    
    
# Asset Level 

def asset_depth(apikey, start_time, end_time, base_asset, exchanges, instrument_class, quote_assets=['usd', 'usdt', 'usdc']):
    headers = {'Accept': 'application/json',
               'X-Api-Key': apikey}
    df_list = []
    for quote_asset in quote_assets:
        instrument = f"{base_asset}-{quote_asset}"
        for exchange in exchanges:
            try:
                url = f'https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/{exchange}/{instrument_class}/{instrument}/snapshots/full?start_time={start_time}&end_time={end_time}'
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
    # group by exchange and sum
    df = df.groupby('exchange')[cols].sum()
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
    plt.title("market depth by exchange")
    # Rotate the x-axis labels
    plt.xticks(rotation=70)
    # Save the plot
    plt.savefig(file_name, format='jpeg')
    # Show the plot
    plt.show()






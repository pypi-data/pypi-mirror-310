import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk, filedialog
from sklearn.cluster import KMeans
import time
import functools
import logging
from flexfillsapi import initialize, FlexfillsConnectException

# Initialize ccxt and fetch data
exchange = ccxt.deribit({'enableRateLimit': True})

calculated_bricks = []

max_tries = 5
retry_delay = 5  # Seconds between reconnection attempts

periods_map = {
    "1m": "ONE_MIN",
    "5m": "FIVE_MIN",
    "15m": "FIFTEEN_MIN",
    "30m": "THIRTY_MIN",
    "45m": "FORTY_FIVE_MIN",
    "1h": "ONE_HOUR",
    "2h": "TWO_HOUR",
    "4h": "FOUR_HOURS",
    "12h": "TWELVE_HOURS",
    "1d": "ONE_DAY"
}

# *************************************
# Decorator for handling Exceptions
# *************************************


def handleFlexfillsAPIException(max_retries=max_tries, delay=retry_delay):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0

            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except FlexfillsConnectException as e:
                    # Handling API connection error
                    attempts += 1
                    print(
                        f"Flexfills API connection was closed, retrying: {attempts}")
                    logging.warning(
                        f"Flexfills API connection was closed, retrying: {attempts}")

                    # Reset connection on FlexfillsConnectException and relogin

                    time.sleep(delay)
                    RealTimeFFTApp.login_flexfills()

                except Exception as e:
                    attempts += 1
                    print(f"Failed to execute {
                        func.__name__}, retrying: {attempts}")
                    logging.warning(f"Failed to execute {
                                    func.__name__}, retrying: {attempts}")

                    time.sleep(delay)

            # Reset connection after failure and start over instead of crashing
            print(
                f"Failed after {max_retries} attempts while executing {func.__name__}. Dropping connection and starting over.")
            logging.error(
                f"Failed after {max_retries} attempts while executing {func.__name__}. Dropping connection and starting over.")

            # Drop the connection and reinitialize
            RealTimeFFTApp.login_flexfills()

            # Start the process again
            return wrapper(*args, **kwargs)

        return wrapper

    return decorator_retry


# Function to fetch historical OHLCV data
def fetch_data(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(
        ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


# Function to calculate ATR
def calculate_atr(data, period=14):
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    tr = pd.Series(np.max([high_low, high_close, low_close], axis=0))
    atr = tr.rolling(window=period).mean()
    return atr.iloc[-1]
    print(atr.iloc[-1])


# Function to calculate Renko bricks based on ATR
def renko_calculate(data, atr, existing_bricks=[]):
    renko = existing_bricks.copy()  # Start with the existing bricks
    # Last known brick price or first close price
    prev_close = renko[-1][0] if renko else data['close'].iloc[0]
    timestamp = data.index[0] if not renko else renko[-1][2]  # Start timestamp

    for close, current_time in zip(data['close'], data.index):
        change = close - prev_close
        if abs(change) >= atr:
            while abs(change) >= atr:
                if change > 0:
                    renko.append((prev_close + atr, 'green', current_time))
                    prev_close += atr
                elif change < 0:
                    renko.append((prev_close - atr, 'red', current_time))
                    prev_close -= atr
                change = close - prev_close

    renko_df = pd.DataFrame(renko, columns=['price', 'color', 'timestamp'])
    return renko_df

# Function to create frequency-based "candles" from the combined frequency data


def create_frequency_candles(frequency_data, window_size=5):
    freq_candles = {
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'timestamp': []
    }
    for i in range(0, len(frequency_data) - window_size + 1, window_size):
        window = frequency_data[i:i + window_size]
        freq_candles['open'].append(window[0])
        freq_candles['high'].append(max(window))
        freq_candles['low'].append(min(window))
        freq_candles['close'].append(window[-1])
        freq_candles['timestamp'].append(i)  # Simple index as timestamp

    freq_candle_df = pd.DataFrame(freq_candles)
    freq_candle_df['timestamp'] = pd.to_datetime(
        freq_candle_df['timestamp'], unit='s')
    freq_candle_df.set_index('timestamp', inplace=True)
    return freq_candle_df


# Function to calculate Renko moving average
def calculate_renko_moving_average(renko_data, period):
    renko_data['ma'] = renko_data['price'].rolling(window=period).mean()
    return renko_data


# Function to apply FFT and generate dominant frequency waves
def compute_fft_and_dominant_waves(close_prices, time_series, dominant_threshold=10):
    fft_result = np.fft.fft(close_prices)
    dominant_wave_sum = np.zeros(len(close_prices))
    for i in range(1, dominant_threshold):
        freq = np.fft.fftfreq(len(close_prices), d=5 * 60)
        amplitude = np.abs(fft_result[i])
        phase = np.angle(fft_result[i])
        wave = amplitude * np.cos(2 * np.pi * freq[i] * time_series + phase)
        dominant_wave_sum += wave
    return dominant_wave_sum
    print(dominant_wave_sum)


# Function to add buy/sell signals with PnL calculation
def add_signals(renko_data, combined_frequency, use_frequency):
    signals = []
    in_position = None
    entry_price = None

    for i, row in renko_data.iterrows():
        price = row['price']
        color = row['color']
        ma = row['ma']
        freq_amp = combined_frequency[i] if use_frequency else 0

        # Buy Signal Logic
        if color == 'green' and price > ma and in_position != 'buy' and (freq_amp < 0 or not use_frequency):
            signals.append((row['timestamp'], price, 'buy',
                           color, ma, freq_amp, None))
            in_position = 'buy'
            entry_price = price

        # Close Buy Signal with PnL calculation
        elif color == 'red' and in_position == 'buy':
            pnl = price - entry_price
            signals.append(
                (row['timestamp'], price, 'close_buy', color, ma, freq_amp, pnl))
            in_position = None
            entry_price = None

        # Sell Signal Logic
        elif color == 'red' and price < ma and in_position != 'sell' and (freq_amp > 0 or not use_frequency):
            signals.append(
                (row['timestamp'], price, 'sell', color, ma, freq_amp, None))
            in_position = 'sell'
            entry_price = price

        # Close Sell Signal with PnL calculation
        elif color == 'green' and in_position == 'sell':
            pnl = entry_price - price
            signals.append(
                (row['timestamp'], price, 'close_sell', color, ma, freq_amp, pnl))
            in_position = None
            entry_price = None

    signals_df = pd.DataFrame(signals, columns=['timestamp', 'price', 'signal', 'entry_box_direction', 'moving_average',
                                                'combined_frequency', 'pnl'])
    return signals_df


# Function to perform split K-means clustering on combined frequency
def split_kmeans_frequency(combined_frequency, n_clusters=2):
    midpoint = np.median(combined_frequency)
    lower_freq = combined_frequency[combined_frequency <= midpoint]
    upper_freq = combined_frequency[combined_frequency > midpoint]

    kmeans_lower = KMeans(n_clusters=n_clusters, random_state=0).fit(
        lower_freq.reshape(-1, 1))
    kmeans_upper = KMeans(n_clusters=n_clusters, random_state=0).fit(
        upper_freq.reshape(-1, 1))

    lower_centers = kmeans_lower.cluster_centers_.flatten()
    upper_centers = kmeans_upper.cluster_centers_.flatten()

    cluster_centers = np.concatenate((lower_centers, upper_centers))
    labels = np.empty_like(combined_frequency, dtype=int)
    labels[combined_frequency <= midpoint] = kmeans_lower.predict(
        lower_freq.reshape(-1, 1))
    labels[combined_frequency > midpoint] = kmeans_upper.predict(
        upper_freq.reshape(-1, 1)) + n_clusters

    return cluster_centers, labels


# Tkinter GUI setup
class RealTimeFFTApp(tk.Tk):

    flexfills_api = None

    flexfills_username = '100000_renko1'
    flexfills_password = 'abc123'

    def __init__(self):
        super().__init__()

        # Prefetching Data
        RealTimeFFTApp.login_flexfills()

        self.exchanges = self.get_flexfills_exchanges()
        self.symbols = self.get_flexfills_symbols()

        self.title("Real-Time Crypto FFT & Renko Analysis")
        self.geometry("1000x1000")  # Adjusted for the additional pane

        # Start Control Panel Frame
        controls_frame = tk.Frame(self)
        controls_frame.pack(fill=tk.X)

        ttk.Label(controls_frame, text="Exchange:").pack(
            side=tk.LEFT, padx=5, pady=5)

        self.exchange_var = tk.StringVar(value="FLEXFILLS")
        self.exchange_dropdown = ttk.Combobox(controls_frame, textvariable=self.exchange_var,
                                              values=self.exchanges, state="readonly")
        self.exchange_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(controls_frame, text="Symbol:").pack(
            side=tk.LEFT, padx=5, pady=5)

        # self.symbol_var = tk.StringVar(value="BTC-PERPETUAL")
        # self.symbol_dropdown = ttk.Combobox(controls_frame, textvariable=self.symbol_var,
        #                                     values=["BTC-PERPETUAL", "ETH-PERPETUAL"], state="readonly")
        self.symbol_var = tk.StringVar(value="BTC/USDT")
        self.symbol_dropdown = ttk.Combobox(controls_frame, textvariable=self.symbol_var,
                                            values=self.symbols, state="readonly")
        self.symbol_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(controls_frame, text="Timeframe:").pack(
            side=tk.LEFT, padx=5, pady=5)
        self.timeframe_var = tk.StringVar(value="5m")
        self.timeframe_dropdown = ttk.Combobox(controls_frame, textvariable=self.timeframe_var,
                                               values=["1m", "5m", "15m", "30m", "45m", "1h", "2h", "4h", "12h", "1d"], state="readonly")
        self.timeframe_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(controls_frame, text="Number of Samples:").pack(
            side=tk.LEFT, padx=5, pady=5)
        self.sample_var = tk.IntVar(value=100)
        self.sample_dropdown = ttk.Combobox(controls_frame, textvariable=self.sample_var,
                                            values=[100, 200, 300, 500, 1000], state="readonly")
        self.sample_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        self.use_frequency = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Use Frequency for Signals", variable=self.use_frequency).pack(
            side=tk.LEFT, padx=5, pady=5)

        ttk.Button(controls_frame, text="Download Signals", command=self.download_signals).pack(side=tk.LEFT, padx=5,
                                                                                                pady=5)

        # End of Control Panel Frame

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add an extra pane for the frequency-based Renko chart
        self.fig, (self.ax_candle, self.ax_renko, self.ax_freq,
                   self.ax_freq_renko) = plt.subplots(4, 1, figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_data()
        self.ani = FuncAnimation(
            self.fig, self.update_plots, interval=15000, cache_frame_data=False)
        self.canvas.draw()

    @classmethod
    def login_flexfills(cls):
        # Initialize FlexfillsApi
        print("Initializing FlexfillsApi with provided credentials...")
        flexfills_api = initialize(
            cls.flexfills_username, cls.flexfills_password, is_test=True)
        cls.flexfills_api = flexfills_api
        print("FlexfillsApi initialized successfully!")

    def get_flexfills_exchanges(self):
        print("Fetching Flexfills Exchanges...")
        flexfills_exchanges_resp = self.flexfills_api.get_exchange_names()
        flexfills_exchanges = flexfills_exchanges_resp.get('rest', [])
        print("Flexfills Exchanges are fetched successfully!")

        return flexfills_exchanges

    def get_flexfills_symbols(self):
        print("Fetching Flexfills Symbols...")
        flexfills_symbols_resp = self.flexfills_api.get_instrument_list()
        flexfills_symbols_data = flexfills_symbols_resp.get('data', [])
        flexfills_symbols = [s.get('code') for s in flexfills_symbols_data]
        print("Flexfills Symbols are fetched successfully!")

        return flexfills_symbols

    def fetch_flexfills_data(self):
        _exchange = self.exchange_var.get()
        symbol = self.symbol_var.get()
        timeframe = self.timeframe_var.get()
        limit = int(self.sample_var.get())

        data = self.flexfills_api.trades_data_provider(
            _exchange, symbol, periods_map[timeframe], limit)

        dataframe = self.convert_flexfills_data_to_dataframe(data)

        return dataframe

    def convert_flexfills_data_to_dataframe(self, data):
        column_maps = {
            'openPrice': 'open',
            'maxPrice': 'high',
            'minPrice': 'low',
            'closePrice': 'close',
            'startPeriod': 'timestamp'
        }

        pd_frame = pd.DataFrame.from_dict(data, orient='columns')
        pd_frame.rename(columns=column_maps, inplace=True)
        # pd_frame['timestamp'] = pd_frame['timestamp'].apply(
        #     lambda x: datetime.fromtimestamp(x / 1000))
        pd_frame['timestamp'] = pd.to_datetime(
            pd_frame['timestamp'], unit='ms')
        pd_frame.set_index('timestamp', inplace=True)
        pd_frame['timestamp'] = pd.to_datetime(pd_frame.index, unit='ms')

        return pd_frame

    def fetch_data(self):
        symbol = self.symbol_var.get()
        timeframe = self.timeframe_var.get()
        limit = int(self.sample_var.get())
        data = fetch_data(symbol=symbol, timeframe=timeframe, limit=limit)
        data['timestamp'] = pd.to_datetime(data.index, unit='ms')
        return data

    def update_data(self):
        # self.window_data = self.fetch_data()
        print("Updating Data...")

    def update_plots(self, frame):
        # data = self.fetch_data()
        data = self.fetch_flexfills_data()
        atr = calculate_atr(data)
        renko_data = renko_calculate(data, atr)
        renko_data = calculate_renko_moving_average(renko_data, period=5)

        close_prices = data['close'].values
        time_series = np.arange(len(close_prices)) * 5 * 60
        dominant_wave_sum = compute_fft_and_dominant_waves(
            close_prices, time_series)

        # Create frequency-based candles from the combined frequency data
        freq_candle_data = create_frequency_candles(dominant_wave_sum)
        freq_renko_data = renko_calculate(freq_candle_data, atr)

        cluster_centers, labels = split_kmeans_frequency(dominant_wave_sum)
        self.signals_data = add_signals(
            renko_data, dominant_wave_sum, self.use_frequency.get())

        # Clear all axes
        self.ax_candle.cla()
        self.ax_renko.cla()
        self.ax_freq.cla()
        self.ax_freq_renko.cla()  # Clear the new frequency-based Renko pane

        # Plot the original candlestick data
        mpf.plot(data, type='candle', ax=self.ax_candle, style='charles')

        # Plot the ATR-based Renko bricks
        for _, row in renko_data.iterrows():
            color = row['color']
            self.ax_renko.bar(row['timestamp'], height=atr, bottom=row['price'] - (atr / 2),
                              width=0.01, color=color, edgecolor='black')
        self.ax_renko.plot(renko_data['timestamp'],
                           renko_data['ma'], color='blue')

        # Plot signals on the Renko chart
        for _, row in self.signals_data.iterrows():
            signal = row['signal']
            signal_price = row['price'] - atr * 0.2
            if signal == 'buy':
                self.ax_renko.plot(
                    row['timestamp'], signal_price, marker='^', color='green', markersize=10)
            elif signal == 'sell':
                self.ax_renko.plot(
                    row['timestamp'], signal_price, marker='v', color='red', markersize=10)
            elif signal == 'close_buy':
                self.ax_renko.plot(
                    row['timestamp'], signal_price, marker='x', color='red', markersize=10)
            elif signal == 'close_sell':
                self.ax_renko.plot(
                    row['timestamp'], signal_price, marker='x', color='green', markersize=10)

        # Plot the combined frequency data and clusters
        self.ax_freq.plot(data['timestamp'],
                          dominant_wave_sum, color='red', linewidth=2)
        midpoint = np.median(dominant_wave_sum)

        for center in cluster_centers:
            color = 'green' if center <= midpoint else 'red'
            self.ax_freq.axhline(y=center, color=color,
                                 linestyle='--', linewidth=1)

        self.ax_freq.set_title(
            "Sum of Dominant Frequencies with Split K-means Clusters")

        # Plot Renko bricks for the frequency-based candles on ax_freq_renko
        for _, row in freq_renko_data.iterrows():
            color = row['color']
            self.ax_freq_renko.bar(row.name, height=atr, bottom=row['price'] - (atr / 2),
                                   width=0.01, color=color, edgecolor='black')

        self.ax_freq_renko.set_title(
            "Renko Chart Based on Frequency-Based Candles")

        self.canvas.draw()

    def download_signals(self):
        if hasattr(self, 'signals_data') and not self.signals_data.empty:
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
            if file_path:
                self.signals_data.to_csv(file_path, index=False)
                print(f"Signals data saved to {file_path}")
        else:
            print("No signals data to download.")


# Start the Tkinter application
if __name__ == "__main__":
    app = RealTimeFFTApp()
    app.mainloop()

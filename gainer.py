import asyncio
import json
import websockets
import time
from datetime import datetime
import telegram
import winsound

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/!ticker@arr"
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"

MIN_VOLUME = 1800000
VOLUME_SURGE = 1.2
LOSER_RANGE = (-5.0, -1.0)
GAINER_RANGE = (1.0, 4.0)
TARGET_LOSER_GAIN = 3.0
TARGET_GAINER_GAIN = 5.5
MAX_GAIN = 50.0
CHECK_INTERVAL = 60  # Reduced to 15 seconds for faster updates
MIN_TREND_POINTS = 2
MIN_PRICE_INCREASE = 0.7
MAX_AGE = 86400

COINS=[

    '1000SATSUSDT',     'ACEUSDT',     'ACHUSDT',     'ACTUSDT',     'ACXUSDT','ADAUSDT',     'ADXUSDT',     'AERGOUSDT',     'AGLDUSDT',     'AIXBTUSDT',
    'ALGOUSDT','ALICEUSDT','ALPINEUSDT','ALTUSDT','AMPUSDT','ANIMEUSDT','ANKRUSDT', 'APEUSDT','API3USDT','APTUSDT','ARBUSDT','ARDRUSDT', 'ARKMUSDT','ARKUSDT','ARPAUSDT',
    'ARUSDT',     'ASTRUSDT',     'ATAUSDT',     'ATOMUSDT',     'AVAUSDT','AVAXUSDT',     'AXLUSDT',     'AXSUSDT',     'BANANAUSDT',     'BANDUSDT',
    'BATUSDT',     'BEAMXUSDT',     'BICOUSDT',     'BIOUSDT',     'BLURUSDT','CELOUSDT',     'CELRUSDT',     'CFXUSDT',     'CGPTUSDT',     'CHRUSDT',
    'CHZUSDT',     'COMBOUSDT',     'COOKIEUSDT',     'COSUSDT',     'CTSIUSDT','CTXCUSDT',     'CVCUSDT',     'CYBERUSDT',     'DASHUSDT',     'DATAUSDT',
    'DCRUSDT',     'DENTUSDT',     'DEXEUSDT',     'DGBUSDT',     'DIAUSDT','DOGEUSDT',     'DOTUSDT',     'DUSDT',     'DUSKUSDT',     'DYMUSDT',
    'EDUUSDT',     'EGLDUSDT',     'ELFUSDT',     'ENJUSDT',     'ENSUSDT','EOSUSDT',     'ETCUSDT',     'FETUSDT',     'FIDAUSDT',     'FILUSDT',
    'FIOUSDT',     'FIROUSDT',     'FLOWUSDT',     'FLUXUSDT',     'GALAUSDT','GASUSDT',     'GLMRUSDT',     'GLMUSDT',     'GMTUSDT',     'GNOUSDT',
    'GRTUSDT',     'GTCUSDT',     'GUSDT',     'HBARUSDT',     'HIGHUSDT','HIVEUSDT',     'HOOKUSDT',     'HOTUSDT',     'ICPUSDT',     'ICXUSDT',
    'IDUSDT',     'IOSTUSDT',     'IOTAUSDT',     'IOTXUSDT',     'IOUSDT','IQUSDT',     'JASMYUSDT',     'JTOUSDT',     'KAIAUSDT',     'KDAUSDT',
    'KMDUSDT',     'KSMUSDT',     'LINKUSDT',     'LPTUSDT',     'LRCUSDT','LSKUSDT',     'LTCUSDT',     'LTOUSDT',     'LUNAUSDT',     'MAGICUSDT',
    'MANAUSDT',     'MANTAUSDT',     'MASKUSDT',     'MDTUSDT',     'METISUSDT','MEUSDT',     'MINAUSDT',     'MOVEUSDT',     'MOVRUSDT',     'MTLUSDT',
    'NEARUSDT',     'NFPUSDT',     'NKNUSDT',     'NOTUSDT',     'NULSUSDT','OGNUSDT',     'OMNIUSDT',     'OMUSDT',     'ONEUSDT',     'ONGUSDT',
    'OPUSDT',     'ORDIUSDT',     'OXTUSDT',     'PAXGUSDT',     'PDAUSDT','PHAUSDT',     'PHBUSDT',     'PIVXUSDT',     'PIXELUSDT',     'POLYXUSDT',
    'PONDUSDT',     'PORTALUSDT',     'POWRUSDT',     'PROMUSDT',     'PUNDIXUSDT','PYRUSDT',     'PYTHUSDT',     'QKCUSDT',     'QNTUSDT',     'QTUMUSDT',
    'RADUSDT',     'RAREUSDT',     'REIUSDT',     'RENDERUSDT',     'REQUSDT','RIFUSDT',     'RLCUSDT',     'ROSEUSDT',     'RSRUSDT',     'RVNUSDT',
    'SAGAUSDT',     'SANDUSDT',     'SCRTUSDT',     'SCRUSDT',     'SCUSDT','SEIUSDT',     'SFPUSDT',     'SKLUSDT',     'SLFUSDT',     'SLPUSDT',
    'SNTUSDT',     'SOLUSDT',     'STEEMUSDT',     'STORJUSDT',     'STPTUSDT','STRAXUSDT',     'STRKUSDT',     'STXUSDT',     'SUIUSDT',     'SUSDT',
    'SXPUSDT',     'SYSUSDT',     'TAOUSDT',     'TFUELUSDT',     'THETAUSDT','THEUSDT',     'TIAUSDT',     'TLMUSDT',     'TNSRUSDT',     'TONUSDT',
    'TRBUSDT',     'TRXUSDT',     'TWTUSDT',     'UMAUSDT',     'UTKUSDT','VANAUSDT',     'VANRYUSDT',     'VETUSDT',     'VICUSDT',     'VIDTUSDT',
    'VOXELUSDT',     'VTHOUSDT',     'WAXPUSDT',     'WINUSDT',     'WLDUSDT','WUSDT',     'XAIUSDT',     'XECUSDT',     'XLMUSDT',     'XNOUSDT',
    'XRPUSDT',     'XTZUSDT',     'XVGUSDT',     'YGGUSDT',     'ZECUSDT','ZENUSDT',     'ZILUSDT',     'ZKUSDT',     'ZROUSDT'
    'ACMUSDT','ASRUSDT','ATMUSDT','BARUSDT','BCHUSDT', 'CITYUSDT','COTIUSDT',  'GPSUSDT','HEIUSDT','JUVUSDT',     'KAITOUSDT',    'LAYERUSDT', 'LAZIOUSDT', 
    'LOKAUSDT', 'OGUSDT',     'POLUSDT',     'PORTOUSDT',     'PSGUSDT','SANTOSUSDT','SHELLUSDT','STMXUSDT','IMXUSDT'
    
    
]


async def send_telegram_alert(bot, coin, price, percent_change, initial_change, volume, initial_volume, initial_price, trend_type, profit_target, entry_time):
    volume_surge = (volume / initial_volume) * 100 - 100
    volume_increase = volume - initial_volume
    confidence = "High" if volume_surge > 50 else "Moderate"
    transition_time = time.time() - entry_time
    hours, remainder = divmod(transition_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    transition_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    coin_status = "✅ Coin exists in COINS list ✅" if coin in COINS else "❌ Coin does not exist in COINS list ❌"
    
    message = (
        f"🔥 *{coin} {trend_type}* 🚀\n"
        f"📊 *{percent_change:.2f}% Now (from {initial_change:.2f}%)* | Confidence: {confidence} 🎯\n"
        f"💰 Price: ${price:.4f} (Started at ${initial_price:.4f}) 📈\n"
        f"📊 24H Volume: ${volume:,.0f} (+${volume_increase:.0f}) 📈\n"
        f"📈 Vol Surge: {volume_surge:.0f}% 🚀\n"
        f"💸 Profit Target: ${profit_target:.4f} (20% gain) 🎯\n"
        f"⏰ Transition Time: {transition_str} ⏳\n"
        f"⏰ Entered: {datetime.fromtimestamp(entry_time).strftime('%H:%M:%S')} 📅\n"
        f"⏰ Alerted: {datetime.now().strftime('%H:%M:%S')} 📅\n"
        f"{coin_status}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    print(f"Alert triggered for {coin} - Check Telegram!")

def is_uptrend(data_points):
    if len(data_points) < MIN_TREND_POINTS:
        return False
    changes = [d[1] for d in data_points]
    prices = [d[3] for d in data_points]
    for i in range(len(changes) - 1):
        if changes[i] >= changes[i + 1]:
            return False
        price_increase = ((prices[i + 1] - prices[i]) / prices[i]) * 100
        if price_increase < MIN_PRICE_INCREASE:
            return False
    return True

async def monitor_dynamic_pumps():
    print(f"Starting dynamic pump detector at {datetime.now().strftime('%H:%M:%S')}...")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    coin_data = {}
    alerted_coins = set()
    last_check = 0
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        while True:
            try:
                message = await websocket.recv()
                tickers = json.loads(message)
                current_time = time.time()
                
                for ticker in tickers:
                    symbol = ticker["s"]
                    if not symbol.endswith("USDT"):
                        continue
                    percent_change = float(ticker["P"])
                    volume = float(ticker["q"])
                    price = float(ticker["c"])
                    if volume < MIN_VOLUME:
                        continue
                    
                    if symbol not in coin_data and (LOSER_RANGE[0] <= percent_change <= LOSER_RANGE[1] or GAINER_RANGE[0] <= percent_change <= GAINER_RANGE[1]):
                        coin_data[symbol] = {
                            'entry_time': current_time,
                            'initial_change': percent_change,
                            'initial_volume': volume,
                            'initial_price': price,
                            'history': [(current_time, percent_change, volume, price)]
                        }
                        print(f"Added {symbol}: {percent_change:.2f}%, Vol: ${volume:,.0f}, Price: ${price:.4f} at {datetime.now().strftime('%H:%M:%S')}")
                        #print(f"Raw ticker for {symbol}: {ticker}")  # Debugging output
                    
                    elif symbol in coin_data:
                        data = coin_data[symbol]
                        data['history'].append((current_time, percent_change, volume, price))
                
                if current_time - last_check >= CHECK_INTERVAL:
                    last_check = current_time
                    to_remove = []
                    
                    for symbol, data in list(coin_data.items()):
                        ticker = next((t for t in tickers if t["s"] == symbol), None)
                        if not ticker:
                            continue
                        price = float(ticker["c"])
                        percent_change = float(ticker["P"])
                        volume = float(ticker["q"])
                        if volume < MIN_VOLUME or percent_change > MAX_GAIN:
                            to_remove.append(symbol)
                            continue
                        
                        initial_change = data['initial_change']
                        initial_volume = data['initial_volume']
                        initial_price = data['initial_price']
                        volume_surge = volume / initial_volume
                        profit_target = price * 1.2
                        uptrend = is_uptrend(data['history'][-MIN_TREND_POINTS:])
                        
                        if current_time - data['entry_time'] > MAX_AGE:
                            to_remove.append(symbol)
                            continue
                        
                        if (LOSER_RANGE[0] <= initial_change <= LOSER_RANGE[1] and
                            percent_change >= TARGET_LOSER_GAIN and
                            volume_surge >= VOLUME_SURGE and
                            uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Loser to Gainer")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Loser to Gainer", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                        
                        elif (GAINER_RANGE[0] <= initial_change <= GAINER_RANGE[1] and
                              percent_change >= TARGET_GAINER_GAIN and
                              volume_surge >= VOLUME_SURGE and
                              uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Gainer Climbing")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Gainer Climbing", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                    
                    for symbol in to_remove:
                        coin_data.pop(symbol, None)
            
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(monitor_dynamic_pumps())
'''
import asyncio
import json
import websockets
import time
from datetime import datetime
import telegram
import winsound

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/!ticker@arr"
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"

MIN_VOLUME = 1900000
VOLUME_SURGE = 1.2
LOSER_RANGE = (-5.0, -1.0)
GAINER_RANGE = (1.0, 4.0)
TARGET_LOSER_GAIN = 3.0
TARGET_GAINER_GAIN = 5.5
MAX_GAIN = 50.0
CHECK_INTERVAL = 120
MIN_TREND_POINTS = 2
MIN_PRICE_INCREASE = 0.77  # Minimum 0.77% price increase per step
MAX_AGE = 86400

async def send_telegram_alert(bot, coin, price, percent_change, initial_change, volume, initial_volume, initial_price, trend_type, profit_target, entry_time):
    volume_surge = (volume / initial_volume) * 100 - 100
    volume_increase = volume - initial_volume
    confidence = "High" if volume_surge > 50 else "Moderate"
    transition_time = time.time() - entry_time
    hours, remainder = divmod(transition_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    transition_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    message = (
        f"🔥 *{coin} {trend_type}*\n"
        f"*{percent_change:.2f}% Now (from {initial_change:.2f}%)* | Confidence: {confidence}\n"
        f"Price: ${price:.4f} (Started at ${initial_price:.4f})\n"
        f"24H Volume: ${volume:,.0f} (+${volume_increase:,.0f})\n"
        f"Vol Surge: {volume_surge:.0f}%\n"
        f"Profit Target: ${profit_target:.4f} (20% gain)\n"
        f"Transition Time: {transition_str}\n"
        f"Entered: {datetime.fromtimestamp(entry_time).strftime('%H:%M:%S')}\n"
        f"Alerted: {datetime.now().strftime('%H:%M:%S')}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    winsound.Beep(1500, 500)

def is_uptrend(data_points):
    if len(data_points) < MIN_TREND_POINTS:
        return False
    changes = [d[1] for d in data_points]  # 24H % changes
    prices = [d[2] for d in data_points]  # Prices
    for i in range(len(changes) - 1):
        if changes[i] >= changes[i + 1]:  # Ensure % change increases
            return False
        price_increase = ((prices[i + 1] - prices[i]) / prices[i]) * 100
        if price_increase < MIN_PRICE_INCREASE:
            return False
    return True

async def monitor_dynamic_pumps():
    print(f"Starting dynamic pump detector at {datetime.now().strftime('%H:%M:%S')}...")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    coin_data = {}
    alerted_coins = set()
    last_check = 0
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        while True:
            try:
                message = await websocket.recv()
                tickers = json.loads(message)
                current_time = time.time()
                
                for ticker in tickers:
                    symbol = ticker["s"]
                    if not symbol.endswith("USDT"):
                        continue
                    percent_change = float(ticker["P"])
                    volume = float(ticker["q"])
                    price = float(ticker["c"])
                    if volume < MIN_VOLUME:
                        continue
                    
                    if symbol not in coin_data and (LOSER_RANGE[0] <= percent_change <= LOSER_RANGE[1] or GAINER_RANGE[0] <= percent_change <= GAINER_RANGE[1]):
                        coin_data[symbol] = {
                            'entry_time': current_time,
                            'initial_change': percent_change,
                            'initial_volume': volume,
                            'initial_price': price,
                            'history': [(current_time, percent_change, volume, price)]
                        }
                        print(f"Added {symbol}: {percent_change:.2f}%, Vol: ${volume:,.0f}, Price: ${price:.4f} at {datetime.now().strftime('%H:%M:%S')}")
                
                if current_time - last_check >= CHECK_INTERVAL:
                    last_check = current_time
                    to_remove = []
                    
                    for symbol, data in list(coin_data.items()):
                        ticker = next((t for t in tickers if t["s"] == symbol), None)
                        if not ticker:
                            continue
                        price = float(ticker["c"])
                        percent_change = float(ticker["P"])
                        volume = float(ticker["q"])
                        if volume < MIN_VOLUME or percent_change > MAX_GAIN:
                            to_remove.append(symbol)
                            continue
                        
                        data['history'].append((current_time, percent_change, volume, price))
                        initial_change = data['initial_change']
                        initial_volume = data['initial_volume']
                        initial_price = data['initial_price']
                        volume_surge = volume / initial_volume
                        profit_target = price * 1.2
                        uptrend = is_uptrend(data['history'][-MIN_TREND_POINTS:])
                        
                        if current_time - data['entry_time'] > MAX_AGE:
                            to_remove.append(symbol)
                            continue
                        
                        if (LOSER_RANGE[0] <= initial_change <= LOSER_RANGE[1] and
                            percent_change >= TARGET_LOSER_GAIN and
                            volume_surge >= VOLUME_SURGE and
                            uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Loser to Gainer")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Loser to Gainer", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                        
                        elif (GAINER_RANGE[0] <= initial_change <= GAINER_RANGE[1] and
                              percent_change >= TARGET_GAINER_GAIN and
                              volume_surge >= VOLUME_SURGE and
                              uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Gainer Climbing")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Gainer Climbing", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                    
                    for symbol in to_remove:
                        coin_data.pop(symbol, None)
            
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(monitor_dynamic_pumps())

'''
'''


import asyncio
import json
import websockets
import time
from datetime import datetime
import telegram
import winsound

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/!ticker@arr"
TELEGRAM_BOT_TOKEN = "7669206577:AAFkCNJGkclyHf1w3x82DdLOAQDXUZ1Zzp4"
TELEGRAM_CHAT_ID = "5959819558"

MIN_VOLUME = 1900000
VOLUME_SURGE = 1.2
LOSER_RANGE = (-5.0, -1.0)
GAINER_RANGE = (1.0, 5.0)
TARGET_LOSER_GAIN = 3.0
TARGET_GAINER_GAIN = 6.0
MAX_GAIN = 50.0
CHECK_INTERVAL = 30
MIN_TREND_POINTS = 2
MAX_AGE = 86400

async def send_telegram_alert(bot, coin, price, percent_change, initial_change, volume, initial_volume, initial_price, trend_type, profit_target, entry_time):
    volume_surge = (volume / initial_volume) * 100 - 100
    volume_increase = volume - initial_volume
    confidence = "High" if volume_surge > 50 else "Moderate"
    transition_time = time.time() - entry_time
    hours, remainder = divmod(transition_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    transition_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    message = (
        f"🔥 *{coin} {trend_type}*\n"
        f"*{percent_change:.2f}% Now (from {initial_change:.2f}%)* | Confidence: {confidence}\n"
        f"Price: ${price:.4f} (Started at ${initial_price:.4f})\n"
        f"24H Volume: ${volume:,.0f} (+${volume_increase:,.0f})\n"
        f"Vol Surge: {volume_surge:.0f}%\n"
        f"Profit Target: ${profit_target:.4f} (20% gain)\n"
        f"Transition Time: {transition_str}\n"
        f"Entered: {datetime.fromtimestamp(entry_time).strftime('%H:%M:%S')}\n"
        f"Alerted: {datetime.now().strftime('%H:%M:%S')}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    winsound.Beep(1500, 500)

def is_uptrend(data_points):
    if len(data_points) < MIN_TREND_POINTS:
        return False
    changes = [d[1] for d in data_points]
    return all(changes[i] < changes[i + 1] for i in range(len(changes) - 1))

async def monitor_dynamic_pumps():
    print(f"Starting dynamic pump detector at {datetime.now().strftime('%H:%M:%S')}...")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    coin_data = {}
    alerted_coins = set()
    last_check = 0
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        while True:
            try:
                message = await websocket.recv()
                tickers = json.loads(message)
                current_time = time.time()
                
                for ticker in tickers:
                    symbol = ticker["s"]
                    if not symbol.endswith("USDT"):
                        continue
                    percent_change = float(ticker["P"])
                    volume = float(ticker["q"])
                    price = float(ticker["c"])
                    if volume < MIN_VOLUME:
                        continue
                    
                    if symbol not in coin_data and (LOSER_RANGE[0] <= percent_change <= LOSER_RANGE[1] or GAINER_RANGE[0] <= percent_change <= GAINER_RANGE[1]):
                        coin_data[symbol] = {
                            'entry_time': current_time,
                            'initial_change': percent_change,
                            'initial_volume': volume,
                            'initial_price': price,
                            'history': [(current_time, percent_change, volume)]
                        }
                        print(f"Added {symbol}: {percent_change:.2f}%, Vol: ${volume:,.0f} at {datetime.now().strftime('%H:%M:%S')}")
                
                if current_time - last_check >= CHECK_INTERVAL:
                    last_check = current_time
                    to_remove = []
                    
                    for symbol, data in list(coin_data.items()):
                        ticker = next((t for t in tickers if t["s"] == symbol), None)
                        if not ticker:
                            continue
                        price = float(ticker["c"])
                        percent_change = float(ticker["P"])
                        volume = float(ticker["q"])
                        if volume < MIN_VOLUME or percent_change > MAX_GAIN:
                            to_remove.append(symbol)
                            continue
                        
                        data['history'].append((current_time, percent_change, volume))
                        initial_change = data['initial_change']
                        initial_volume = data['initial_volume']
                        initial_price = data['initial_price']
                        volume_surge = volume / initial_volume
                        profit_target = price * 1.2
                        uptrend = is_uptrend(data['history'][-MIN_TREND_POINTS:])
                        
                        if current_time - data['entry_time'] > MAX_AGE:
                            to_remove.append(symbol)
                            continue
                        
                        if (LOSER_RANGE[0] <= initial_change <= LOSER_RANGE[1] and
                            percent_change >= TARGET_LOSER_GAIN and
                            volume_surge >= VOLUME_SURGE and
                            uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Loser to Gainer")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Loser to Gainer", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                        
                        elif (GAINER_RANGE[0] <= initial_change <= GAINER_RANGE[1] and
                              percent_change >= TARGET_GAINER_GAIN and
                              volume_surge >= VOLUME_SURGE and
                              uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Gainer Climbing")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Gainer Climbing", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                    
                    for symbol in to_remove:
                        coin_data.pop(symbol, None)
            
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(monitor_dynamic_pumps())
'''
'''
import asyncio
import json
import websockets
import time
from datetime import datetime
import telegram
import winsound  # Windows (Mac: os.system("afplay /path/to/sound.mp3"))

# Binance WebSocket endpoint
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/!ticker@arr"

# Telegram bot setup (replace with your values)
TELEGRAM_BOT_TOKEN = "7669206577:AAFkCNJGkclyHf1w3x82DdLOAQDXUZ1Zzp4"
TELEGRAM_CHAT_ID = "5959819558"

# Thresholds
MIN_VOLUME = 1900000
VOLUME_SURGE = 1.21
LOSER_RANGE = (-5.0, -1.0)    # Losers: -5% to -1%
GAINER_RANGE = (1.0, 4.0)     # Gainers: 1% to 5%
TARGET_LOSER_GAIN = 3       # Alert at +3%+ for Losers
TARGET_GAINER_GAIN = 6      # Alert at +6%+ for Gainers
MAX_GAIN = 50.0
CHECK_INTERVAL = 300
MIN_TREND_POINTS = 2
MAX_AGE = 86400

async def send_telegram_alert(bot, coin, price, percent_change, initial_change, volume, initial_volume, initial_price, trend_type, profit_target, entry_time):
    volume_surge = (volume / initial_volume) * 100 - 100
    volume_increase = volume - initial_volume
    confidence = "High" if volume_surge > 50 else "Moderate"
    transition_time = time.time() - entry_time
    hours, remainder = divmod(transition_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    transition_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    message = (
        f"🔥 *{coin} {trend_type}*\n"
        f"*{percent_change:.2f}% Now (from {initial_change:.2f}%)* | Confidence: {confidence}\n"
        f"Price: ${price:.4f} (Started at ${initial_price:.4f})\n"
        f"24H Volume: ${volume:,.0f} (+${volume_increase:,.0f})\n"
        f"Vol Surge: {volume_surge:.0f}%\n"
        f"Profit Target: ${profit_target:.4f} (20% gain)\n"
        f"Transition Time: {transition_str}\n"
        f"Entered: {datetime.fromtimestamp(entry_time).strftime('%H:%M:%S')}\n"
        f"Alerted: {datetime.now().strftime('%H:%M:%S')}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    
    winsound.Beep(1500, 500)

def is_uptrend(data_points):
    if len(data_points) < MIN_TREND_POINTS:
        return False
    changes = [d[1] for d in data_points]
    return all(changes[i] < changes[i + 1] for i in range(len(changes) - 1))

async def monitor_dynamic_pumps():
    print(f"Starting dynamic pump detector at {datetime.now().strftime('%H:%M:%S')}...")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    coin_data = {}  # {symbol: {'entry_time': t, 'initial_change': %, 'initial_volume': v, 'initial_price': p, 'history': [(t, %, v), ...]}}
    alerted_coins = set()
    last_check = 0
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        while True:
            try:
                message = await websocket.recv()
                tickers = json.loads(message)
                current_time = time.time()
                
                # Update coins every tick
                for ticker in tickers:
                    symbol = ticker["s"]
                    if not symbol.endswith("USDT"):
                        continue
                    percent_change = float(ticker["P"])
                    volume = float(ticker["q"])
                    price = float(ticker["c"])
                    if volume < MIN_VOLUME:
                        continue
                    
                    # Add new coins
                    if symbol not in coin_data and (LOSER_RANGE[0] <= percent_change <= LOSER_RANGE[1] or GAINER_RANGE[0] <= percent_change <= GAINER_RANGE[1]):
                        coin_data[symbol] = {
                            'entry_time': current_time,
                            'initial_change': percent_change,
                            'initial_volume': volume,
                            'initial_price': price,
                            'history': [(current_time, percent_change, volume)]
                        }
                        print(f"Added {symbol}: {percent_change:.2f}%, Vol: ${volume:,.0f} at {datetime.now().strftime('%H:%M:%S')}")
                
                # Check every 5 minutes
                if current_time - last_check >= CHECK_INTERVAL:
                    last_check = current_time
                    to_remove = []
                    
                    for symbol, data in list(coin_data.items()):
                        ticker = next((t for t in tickers if t["s"] == symbol), None)
                        if not ticker:
                            continue
                        price = float(ticker["c"])
                        percent_change = float(ticker["P"])
                        volume = float(ticker["q"])
                        if volume < MIN_VOLUME or percent_change > MAX_GAIN:
                            to_remove.append(symbol)
                            continue
                        
                        # Update history
                        data['history'].append((current_time, percent_change, volume))
                        initial_change = data['initial_change']
                        initial_volume = data['initial_volume']
                        initial_price = data['initial_price']
                        volume_surge = volume / initial_volume
                        profit_target = price * 1.2
                        uptrend = is_uptrend(data['history'][-MIN_TREND_POINTS:])
                        
                        # Clean up old coins
                        if current_time - data['entry_time'] > MAX_AGE:
                            to_remove.append(symbol)
                            continue
                        
                        # Loser to Gainer: -5% to -1% -> +3%+
                        if (LOSER_RANGE[0] <= initial_change <= LOSER_RANGE[1] and
                            percent_change >= TARGET_LOSER_GAIN and
                            volume_surge >= VOLUME_SURGE and
                            uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Loser to Gainer")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Loser to Gainer", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                        
                        # Gainer Climbing: 1% to 5% -> +6%+
                        elif (GAINER_RANGE[0] <= initial_change <= GAINER_RANGE[1] and
                              percent_change >= TARGET_GAINER_GAIN and
                              volume_surge >= VOLUME_SURGE and
                              uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Gainer Climbing")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Gainer Climbing", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                    
                    # Cleanup
                    for symbol in to_remove:
                        coin_data.pop(symbol, None)
            
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":

    asyncio.run(monitor_dynamic_pumps())
'''

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import calendar
import os
import requests
import json
import statistics
import pathlib # pathlib をインポート

# --- I. フォントごとの設定データ (JSON形式) ---
FONT_SETTINGS_JSON = """
{
    "Noto Sans JP": {
        "FONT_PATH": "ttf/NotoSansJP-Regular.ttf",
        "SPACE_PADDING_COUNT": 2,
        "DAY_NAME_PADDING_PIXELS": 0,
        "SINGLE_DIGIT_DATE_PADDING_PIXELS": 0
    },
    "Murecho": {
        "FONT_PATH": "ttf/Murecho-Regular.ttf",
        "SPACE_PADDING_COUNT": 2,
        "DAY_NAME_PADDING_PIXELS": 0,
        "SINGLE_DIGIT_DATE_PADDING_PIXELS": 0
    },
    "Kaisei Decol": {
        "FONT_PATH": "ttf/KaiseiDecol-Regular.ttf",
        "SPACE_PADDING_COUNT": 1,
        "DAY_NAME_PADDING_PIXELS": 0,
        "SINGLE_DIGIT_DATE_PADDING_PIXELS": 0
    },
    "Mochiy Pop One": {
        "FONT_PATH": "ttf/MochiyPopOne-Regular.ttf",
        "SPACE_PADDING_COUNT": 2,
        "DAY_NAME_PADDING_PIXELS": 0,
        "SINGLE_DIGIT_DATE_PADDING_PIXELS": 0
    },
    "Zen Kurenaido": {
        "FONT_PATH": "ttf/ZenKurenaido-Regular.ttf",
        "SPACE_PADDING_COUNT": 2,
        "DAY_NAME_PADDING_PIXELS": 6,
        "SINGLE_DIGIT_DATE_PADDING_PIXELS": 6
    }
}
"""
FONT_DEFINITIONS = json.loads(FONT_SETTINGS_JSON)


# --- II. 色設定プリセット ---
COLOR_PRESETS = {
    "black": {
        'TEXT_COLOR_DEFAULT': 'black',
        'TEXT_COLOR_SATURDAY': 'blue',
        'TEXT_COLOR_SUNDAY': 'red',
        'HOLIDAY_COLOR': 'red',
    },
    "white": {
        'TEXT_COLOR_DEFAULT': 'white',
        'TEXT_COLOR_SATURDAY': 'lightblue',
        'TEXT_COLOR_SUNDAY': 'pink',
        'HOLIDAY_COLOR': 'pink',
    }
}


# --- III. ユーティリティ関数（変更なし） ---

def get_text_size_for_pil(text, font):
    """Pillowの新しいバージョンに対応したテキストサイズ計算関数 (width, height)を返します。"""
    bbox = font.getmask(text).getbbox()
    if bbox is None:
        return 0, 0
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def fetch_holidays(year):
    """Web APIから指定された年の日本の祝日情報を取得します。"""
    HOLIDAY_API_URL = f"https://date.nager.at/api/v3/PublicHolidays/{year}/JP"
    holidays_set = set()
    
    try:
        response = requests.get(HOLIDAY_API_URL, timeout=10)
        response.raise_for_status()
        holiday_data = response.json()
        
        for item in holiday_data:
            try:
                holiday_date = datetime.strptime(item['date'], '%Y-%m-%d').date()
                holidays_set.add(holiday_date)
            except ValueError:
                continue
                
        print(f" {year}年の祝日情報 ({len(holidays_set)}件) をWeb APIから取得しました。")
        return holidays_set
        
    except requests.exceptions.RequestException as e:
        print(f" 祝日情報の取得に失敗しました（Web APIエラー）。{year}年のカレンダーは祝日なしで生成します。: {e}")
        return set()

def is_holiday(check_date, holidays_set, definitions):
    """指定された日付が祝日かどうかを判定します。"""
    if not definitions.get('ENABLE_HOLIDAY_COLOR', True):
        return False
        
    return check_date in holidays_set

# --- IV. 描画ロジック（変更なし） ---

def draw_month_calendar(draw, start_date, definitions, font, holidays_set):
    """単月分のカレンダーを描画します。"""
    year = start_date.year
    month = start_date.month
    cal = calendar.Calendar(firstweekday=6)
    
    coords = definitions
    
    # 共通パディング文字列（整数個のスペース）
    padding_spaces = ' ' * definitions['SPACE_PADDING_COUNT']
    
    # 1. 月名（算用数字）の描画
    month_text = f"{month:02}"
    text_width, text_height = get_text_size_for_pil(month_text, font)
    month_x = coords['MONTH_CENTER_X'] - text_width / 2
    month_y = coords['MONTH_CENTER_Y'] - text_height / 2
    draw.text((month_x, month_y), month_text, fill=definitions['TEXT_COLOR_DEFAULT'], font=font)

    # 2. 曜日の描画 (S, M, T, W, T, F, S)
    day_names_raw = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
    for i, day_name_raw in enumerate(day_names_raw):
        day_name = padding_spaces + day_name_raw
        day_x = coords['START_X_POS'] + i * coords['COL_WIDTH'] + definitions['DAY_NAME_PADDING_PIXELS']
        
        day_color = definitions['TEXT_COLOR_DEFAULT']
        if i == 0: # 日曜日
            day_color = definitions['TEXT_COLOR_SUNDAY']

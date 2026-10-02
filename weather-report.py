# feature/basic - 기본 날씨 리포트 구성
# weather-report.py
# GitHub: https://github.com/dreamingh07/python-weather-report
#
# Open-Meteo API를 이용한 3일 날씨 리포트 프로그램
# 오전 6시 / 오후 3시 기준 날씨를 출력합니다.

import requests
from datetime import datetime


# ----------------------------------------
# 지역 정보
# ----------------------------------------

# feature/location - 사용자가 조회할 지역을 선택할 수 있도록 구성
locations = {
    "서울": (37.5665, 126.9780),
    "수원": (37.2636, 127.0286),
    "대전": (36.3504, 127.3845),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014)
}


# ----------------------------------------
# 날씨 코드 → 한글 날씨
# ----------------------------------------

def weather_description(code):
    weather_codes = {
        0: "맑음",
        1: "대체로 맑음",
        2: "구름 조금",
        3: "흐림",
        45: "안개",
        48: "짙은 안개",
        51: "이슬비",
        53: "이슬비",
        55: "이슬비",
        61: "약한 비",
        63: "비",
        65: "강한 비",
        71: "약한 눈",
        73: "눈",
        75: "강한 눈",
        80: "소나기",
        81: "소나기",
        82: "강한 소나기",
        95: "천둥번개",
        96: "우박 동반 천둥번개",
        99: "강한 우박 동반 천둥번개"
    }

    return weather_codes.get(code, "알 수 없음")


# ----------------------------------------
# 날씨 API 가져오기
# ----------------------------------------

def get_weather(city):

    latitude, longitude = locations[city]

    # feature/api - Open-Meteo API를 이용하여 실시간 날씨 데이터 요청
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation_probability,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min"
        ),
        "forecast_days": 3,
        "timezone": "Asia/Seoul"
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    return response.json()


# ----------------------------------------
# 특정 시간의 데이터 찾기
# ----------------------------------------

def find_hour_data(data, target_time):

    times = data["hourly"]["time"]

    if target_time not in times:
        return None

    index = times.index(target_time)

    return {
        "temperature": data["hourly"]["temperature_2m"][index],
        "humidity": data["hourly"]["relative_humidity_2m"][index],
        "rain_probability": data["hourly"]["precipitation_probability"][index],
        "weather_code": data["hourly"]["weather_code"][index],
        "wind_speed": data["hourly"]["wind_speed_10m"][index]
    }


# ----------------------------------------
# 날씨 출력
# ----------------------------------------

# feature/display - 날씨 정보를 보기 좋은 형식으로 출력
def print_weather(data, city):

    dates = data["daily"]["time"]

    max_temps = data["daily"]["temperature_2m_max"]
    min_temps = data["daily"]["temperature_2m_min"]

    print()
    print("=" * 60)
    print(f"        {city} 3일 날씨 리포트")
    print("=" * 60)

    for day_index, date in enumerate(dates):

        print()
        print(f"📅 {date}")
        print("-" * 50)

        morning_time = f"{date}T06:00"
        afternoon_time = f"{date}T15:00"

        morning = find_hour_data(data, morning_time)
        afternoon = find_hour_data(data, afternoon_time)

        if morning:
            print("🌅 오전 06:00")
            print(
                f"   날씨: "
                f"{weather_description(morning['weather_code'])}"
            )
            print(f"   기온: {morning['temperature']} °C")
            print(
                f"   강수확률: "
                f"{morning['rain_probability']} %"
            )
            print(f"   습도: {morning['humidity']} %")
            print(f"   풍속: {morning['wind_speed']} m/s")

        print()

        if afternoon:
            print("🌇 오후 15:00")
            print(
                f"   날씨: "
                f"{weather_description(afternoon['weather_code'])}"
            )
            print(f"   기온: {afternoon['temperature']} °C")
            print(
                f"   강수확률: "
                f"{afternoon['rain_probability']} %"
            )
            print(f"   습도: {afternoon['humidity']} %")
            print(f"   풍속: {afternoon['wind_speed']} m/s")

        print()

        print(
            f"🌡️ 일일 기온: "
            f"최저 {min_temps[day_index]} °C / "
            f"최고 {max_temps[day_index]} °C"
        )

        print("-" * 50)


# ----------------------------------------
# 메인 프로그램
# ----------------------------------------

def main():

    print("☀️ 날씨 예보 프로그램")
    print("3일간의 날씨를 제공합니다.")
    print()

    print("조회 가능한 지역:")
    print(", ".join(locations.keys()))

    city = input("날씨를 확인할 지역을 입력하세요 (기본값: 서울): ").strip()

    if city == "":
        city = "서울"

    if city not in locations:
        print("등록되지 않은 지역입니다.")
        print("기본 지역인 서울의 날씨를 표시합니다.")
        city = "서울"

    print()
    print(f"📍 {city}의 날씨 정보를 가져오는 중입니다...")

    # feature/error - API 요청 및 프로그램 실행 중 발생할 수 있는 오류 처리
    try:

        data = get_weather(city)

        print_weather(data, city)

        print()
        print("날씨 정보 조회가 완료되었습니다.")

    except requests.exceptions.RequestException as error:

        print()
        print("❌ 날씨 정보를 가져오는 중 오류가 발생했습니다.")
        print(f"오류 내용: {error}")


if __name__ == "__main__":
    main()
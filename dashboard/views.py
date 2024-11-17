from django.shortcuts import render
from .models import MonitoringLocation, WaterQualityMeasurement
import plotly.express as px
import numpy as np

def dashboard_view(request):
    location = request.GET.get('location')
    date_range = request.GET.get('date_range')
    characteristic = request.GET.get('characteristic', 'Temperature, water')
    year = request.GET.get('year')
    season = request.GET.get('season')

    measurements = WaterQualityMeasurement.objects.filter(characteristic_name=characteristic)

    # Apply location filter
    if location:
        measurements = measurements.filter(location__location_id=location)

    # Apply date range filter if valid
    if date_range:
        start_date, end_date = parse_date_range(date_range)
        if start_date and end_date:
            measurements = measurements.filter(date__range=[start_date, end_date])
        else:
            print("Invalid date range provided")
    elif year and season:
        season_start, season_end = get_season_dates(int(year), season)
        if season_start and season_end:
            measurements = measurements.filter(date__range=[season_start, season_end])
        else:
            print(f"Invalid season or year: {season}, {year}")

    print(f"Filtered measurements count: {measurements.count()}")

    # Anomaly Detection
    anomalies = detect_anomalies(measurements)

    # Plot data
    dates = [m.date for m in measurements]
    values = [m.result_value for m in measurements]
    fig = px.line(x=dates, y=values, title=f"{characteristic} Over Time")
    chart = fig.to_html()

    return render(request, 'dashboard/dashboard.html', {
        'chart': chart,
        'anomalies': anomalies,
        'selected_year': year,
        'selected_season': season,
    })


def parse_date_range(date_range):
    """Parse the date range from 'YYYY-MM-DD to YYYY-MM-DD'."""
    try:
        start_date, end_date = date_range.split(" to ")
        print(f"Parsed date range: Start Date = {start_date}, End Date = {end_date}")
        return start_date.strip(), end_date.strip()
    except ValueError:
        print("Error: Invalid date range format.")
        return None, None



def get_season_dates(year, season):
    """Get start and end dates for a specific season."""
    season_mapping = {
        'Winter': (f"{year - 1}-12-21", f"{year}-03-20"),
        'Spring': (f"{year}-03-21", f"{year}-06-20"),
        'Summer': (f"{year}-06-21", f"{year}-09-22"),
        'Fall': (f"{year}-09-23", f"{year}-12-20"),
    }
    return season_mapping.get(season, (None, None))

def detect_anomalies(measurements):
  anomalies = []
  if measurements.exists():
    values = [m.result_value for m in measurements if m.result_value is not None]
    if values:
      mean_value = np.mean(values)
      std_dev = np.std(values)
      for m in measurements:
        if m.result_value and (m.result_value < mean_value - 2 * std_dev or m.result_value > mean_value + 2 * std_dev):
          anomalies.append(m)
  return anomalies

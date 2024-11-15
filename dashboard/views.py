from django.shortcuts import render
from .models import MonitoringLocation, WaterQualityMeasurement
import plotly.express as px
import numpy as np

def dashboard_view(request):
  location = request.GET.get('location')
  start_date = request.GET.get('start_date')
  end_date = request.GET.get('end_date')
  characteristic = request.GET.get('characteristic', 'Temperature, water')

  # Filter measurements based on the provided query parameters
  measurements = WaterQualityMeasurement.objects.filter(characteristic_name=characteristic)
  
  if location:
    measurements = measurements.filter(location__location_id=location)
  if start_date and end_date:
    measurements = measurements.filter(date__range=[start_date, end_date])

  # Anomaly Detection
  anomalies = detect_anomalies(measurements)

  # Prepare data for Plotly chart
  dates = [m.date for m in measurements]
  values = [m.result_value for m in measurements]
  
  fig = px.line(x=dates, y=values, title=f"{characteristic} Over Time")
  chart = fig.to_html()

  # Render the template with the chart and anomalies
  return render(request, 'dashboard/dashboard.html', {'chart': chart, 'anomalies': anomalies})

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

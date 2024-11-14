import pandas as pd
from dashboard.models import MonitoringLocation, WaterQualityMeasurement

def run():
  data = pd.read_csv('Data/Surface_Water_Quality_Monitoring_Network_Grab_Sample_Water_Quality_Data.csv')
  data = data.fillna('')  # Replace NaN values for easy handling

  for _, row in data.iterrows():
    # Get or create the monitoring location
    location, _ = MonitoringLocation.objects.get_or_create(
      location_id=row['MonitoringLocationID'],
      location_name=row['MonitoringLocationName'],
      location_type=row['MonitoringLocationType'],
      waterbody=row['MonitoringLocationWaterbody']
    )

    # Create a water quality measurement entry
    WaterQualityMeasurement.objects.create(
      location=location,
      date=pd.to_datetime(row['ActivityStartDate']).date(),
      time=pd.to_datetime(row['ActivityStartTime']).time(),
      depth=row['ActivityDepthHeightMeasure'] if row['ActivityDepthHeightMeasure'] != '' else None,
      characteristic_name=row['CharacteristicName'],
      result_value=row['ResultValue'] if row['ResultValue'] != '' else None,
      result_unit=row['ResultUnit']
    )

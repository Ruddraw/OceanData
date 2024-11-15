import pandas as pd
from dashboard.models import MonitoringLocation, WaterQualityMeasurement

def run():
    """
    Import ocean data from a CSV file, creating or updating monitoring locations 
    and storing water quality measurements.

    The function reads data from 'source/oceanData.csv' and processes each row:
    - If a monitoring location with the specified location ID exists, it retrieves it; otherwise, it creates a new location.
    - It then creates a new water quality measurement entry linked to the monitoring location.
    - Missing values in the CSV are filled with an empty string ('') for easier handling within the code.
    """
    
    # Read the CSV file into a DataFrame and fill NaN values with an empty string
    data = pd.read_csv('source/oceanData.csv')
    data = data.fillna('')  # Replace NaN values with empty strings for easy handling

    # Loop through each row in the DataFrame
    for _, row in data.iterrows():
        # Retrieve or create the monitoring location entry based on location ID and details
        location, _ = MonitoringLocation.objects.get_or_create(
            location_id=row['MonitoringLocationID'],  # Unique ID for monitoring location
            location_name=row['MonitoringLocationName'],  # Name of the monitoring location
            location_type=row['MonitoringLocationType'],  # Type of the location (e.g., river, ocean)
            waterbody=row['MonitoringLocationWaterbody']  # Name of the waterbody associated with the location
        )

        # Create a new water quality measurement entry associated with the monitoring location
        WaterQualityMeasurement.objects.create(
            location=location,  # Reference to the monitoring location
            date=pd.to_datetime(row['ActivityStartDate']).date(),  # Start date of the measurement activity
            time=pd.to_datetime(row['ActivityStartTime']).time(),  # Start time of the measurement activity
            depth=row['ActivityDepthHeightMeasure'] if row['ActivityDepthHeightMeasure'] != '' else None,  # Measurement depth, if available
            characteristic_name=row['CharacteristicName'],  # Name of the characteristic measured (e.g., temperature)
            result_value=row['ResultValue'] if row['ResultValue'] != '' else None,  # Measurement result value, if available
            result_unit=row['ResultUnit']  # Unit of the measurement result
        )

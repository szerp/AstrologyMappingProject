from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from pathlib import Path
from datetime import datetime, timezone
import logging

# Set up logging
log_file_path = "kerykeion.log"
logging.basicConfig(level=logging.DEBUG, filename=log_file_path, filemode='a')

def get_location_info(city_name, state_name, country_name):
    """Fetch latitude, longitude, and timezone for the given location."""
    geolocator = Nominatim(user_agent="astrology_app")
    location_query = f"{city_name}, {state_name}, {country_name}" if state_name else f"{city_name}, {country_name}"
    location = geolocator.geocode(location_query)
    if location:
        latitude, longitude = location.latitude, location.longitude
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
        return latitude, longitude, timezone_str
    else:
        raise ValueError(f"Location '{location_query}' not found.")

def generate_astrology_charts():
    print("Enter the following details for the natal chart:")
    name = input("Name: ").strip()
    year = int(input("Year of birth (e.g., 1991): "))
    month = int(input("Month of birth (1-12): "))
    day = int(input("Day of birth (1-31): "))
    hour = int(input("Hour of birth (0-23): "))
    minute = int(input("Minute of birth (0-59): "))
    city = input("City of birth: ").strip()
    state = input("State of birth (if applicable, otherwise leave blank): ").strip()
    country = input("Country of birth: ").strip()

    try:
        # Get location data
        latitude, longitude, tz = get_location_info(city, state, country)
        print(f"Location found for {name}: Latitude {latitude}, Longitude {longitude}, Timezone {tz}")

        # Create Natal Subject
        natal_subject = AstrologicalSubject(
            name, year, month, day, hour, minute,
            lng=longitude, lat=latitude, tz_str=tz
        )

        # Define output directory
        output_dir = Path.cwd() / "generated_charts"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate Natal Chart
        print(f"Generating natal chart for {name}...")
        natal_chart = KerykeionChartSVG(natal_subject, chart_type="Natal", new_output_directory=str(output_dir))
        natal_chart.makeSVG()

        natal_chart_file = output_dir / f"{name} - Natal Chart.svg"
        if natal_chart_file.exists():
            print(f"Natal chart successfully saved at: {natal_chart_file}")
        else:
            print(f"Failed to save natal chart at: {natal_chart_file}")

        # Generate Transit Chart
        print(f"Generating transit chart for {name}...")
        current_time = datetime.now(timezone.utc)  # Use timezone-aware datetime for accuracy
        transit_subject = AstrologicalSubject(
            "Current Planetary Positions",
            current_time.year, current_time.month, current_time.day,
            current_time.hour, current_time.minute,
            lng=0.0, lat=0.0, tz_str="UTC"
        )

        transit_chart = KerykeionChartSVG(natal_subject, "Transit", transit_subject, new_output_directory=str(output_dir))
        transit_chart.makeSVG()

        transit_chart_file = output_dir / f"{name} - Transit Chart.svg"
        if transit_chart_file.exists():
            print(f"Transit chart successfully saved at: {transit_chart_file}")
        else:
            print(f"Failed to save transit chart at: {transit_chart_file}")

        # Check if Synastry Chart is needed
        synastry_choice = input("Do you want to generate a synastry chart? (yes/no): ").strip().lower()
        if synastry_choice == "yes":
            print("\nEnter the following details for the second person:")
            second_name = input("Second person's name: ").strip()
            second_year = int(input("Year of birth (e.g., 1991): "))
            second_month = int(input("Month of birth (1-12): "))
            second_day = int(input("Day of birth (1-31): "))
            second_hour = int(input("Hour of birth (0-23): "))
            second_minute = int(input("Minute of birth (0-59): "))
            second_city = input("Second person's city of birth: ").strip()
            second_state = input("Second person's state of birth (if applicable, otherwise leave blank): ").strip()
            second_country = input("Second person's country of birth: ").strip()

            second_lat, second_lng, second_tz = get_location_info(second_city, second_state, second_country)
            print(f"Location found for {second_name}: Latitude {second_lat}, Longitude {second_lng}, Timezone {second_tz}")

            second_subject = AstrologicalSubject(
                second_name, second_year, second_month, second_day, second_hour, second_minute,
                lng=second_lng, lat=second_lat, tz_str=second_tz
            )

            # Generate Synastry Chart
            print(f"Generating synastry chart for {name} and {second_name}...")
            synastry_chart = KerykeionChartSVG(
                natal_subject, "Synastry", second_subject, new_output_directory=str(output_dir)
            )
            synastry_chart.makeSVG()

            synastry_chart_file = output_dir / f"{name} and {second_name} - Synastry Chart.svg"
            if synastry_chart_file.exists():
                print(f"Synastry chart successfully saved at: {synastry_chart_file}")
            else:
                print(f"Failed to save synastry chart at: {synastry_chart_file}")

    except Exception as e:
        print(f"Error generating charts: {e}")
        logging.error(f"Error generating charts: {e}")

# Run the function
generate_astrology_charts()

# Notify where logs are saved
print(f"Logs written to: {log_file_path}")

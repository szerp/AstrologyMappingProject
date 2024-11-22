import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from pathlib import Path
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import os


class AstrologyChartGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astrology Chart Generator")
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()
        self.preview_window = None

    def init_ui(self):
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        # Create input groups for Main and Second Person
        self.main_person = self.create_input_group("Main Person", "#ffffe0")
        self.second_person = self.create_input_group("Second Person", "#ffe6f7")

        input_layout.addLayout(self.main_person["layout"])
        input_layout.addLayout(self.second_person["layout"])
        main_layout.addLayout(input_layout)

        # Buttons for generating charts
        button_layout_1 = QHBoxLayout()
        button_layout_2 = QHBoxLayout()

        # Buttons for main person
        buttons_1 = [
            ("Generate Natal Chart (1st)", lambda: self.generate_chart("Natal", self.main_person["entries"]), "#ffcccc"),
            ("Generate Transit Chart (1st)", lambda: self.generate_chart("Transit", self.main_person["entries"]), "#ccffcc"),
            ("Clear Main Person", self.main_person["clear"], "#ffccee"),
        ]

        # Buttons for second person and synastry
        buttons_2 = [
            ("Generate Natal Chart (2nd)", lambda: self.generate_chart("Natal", self.second_person["entries"]), "#ccccff"),
            ("Generate Transit Chart (2nd)", lambda: self.generate_chart("Transit", self.second_person["entries"]), "#ffffcc"),
            ("Clear Second Person", self.second_person["clear"], "#ccffee"),
            ("Generate Synastry Chart", lambda: self.generate_chart("Synastry", None), "#ffccff"),
        ]

        # Add buttons to the layouts
        for text, func, color in buttons_1:
            btn = self.create_button(text, func, color)
            button_layout_1.addWidget(btn)
        for text, func, color in buttons_2:
            btn = self.create_button(text, func, color)
            button_layout_2.addWidget(btn)

        main_layout.addLayout(button_layout_1)
        main_layout.addLayout(button_layout_2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_input_group(self, title, color):
        layout = QVBoxLayout()
        frame = QWidget()
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        frame.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        entries = {}
        for field in ["Name", "Year", "Month", "Day", "Hour", "Minute", "City", "State", "Country"]:
            row = QHBoxLayout()
            label = QLabel(field)
            entry = QLineEdit()
            entries[field.lower()] = entry
            row.addWidget(label)
            row.addWidget(entry)
            frame_layout.addLayout(row)

        layout.addWidget(frame)

        def clear_entries():
            for entry in entries.values():
                entry.clear()

        return {"layout": layout, "entries": entries, "clear": clear_entries}

    def create_button(self, text, func, color):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10, QFont.Bold))
        button.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")
        button.clicked.connect(func)
        return button

    def get_location_info(self, city, state, country):
        geolocator = Nominatim(user_agent="astrology_app")
        location_query = f"{city}, {state}, {country}" if state else f"{city}, {country}"
        location = geolocator.geocode(location_query)
        if location:
            tf = TimezoneFinder()
            return location.latitude, location.longitude, tf.timezone_at(lat=location.latitude, lng=location.longitude)
        raise ValueError(f"Location '{location_query}' not found.")

    def get_person_data(self, entries):
        try:
            name = entries["name"].text().strip()
            if not name:
                raise ValueError("Name is required.")

            year = int(entries["year"].text().strip())
            month = int(entries["month"].text().strip())
            day = int(entries["day"].text().strip())
            hour = int(entries["hour"].text().strip())
            minute = int(entries["minute"].text().strip())

            city = entries["city"].text().strip()
            state = entries["state"].text().strip() or ""
            country = entries["country"].text().strip()

            if not city or not country:
                raise ValueError("City and Country are required.")

            latitude, longitude, timezone = self.get_location_info(city, state, country)

            return {
                "name": name,
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
            }
        except ValueError as ve:
            raise ValueError(f"Invalid input: {ve}")
        except Exception as e:
            raise ValueError(f"Error retrieving location: {e}")

    def generate_chart(self, chart_type, entries=None):
        try:
            # Define the output directory
            output_dir = Path.cwd() / "generated_charts"
            output_dir.mkdir(parents=True, exist_ok=True)

            if chart_type in ["Natal", "Transit"]:
                person_data = self.get_person_data(entries)

            if chart_type == "Synastry":
                # Fetch both person details
                main_person_data = self.get_person_data(self.main_person["entries"])
                second_person_data = self.get_person_data(self.second_person["entries"])

                # Define the output directory
                output_dir = Path.cwd() / "generated_charts"
                output_dir.mkdir(parents=True, exist_ok=True)

                # Define custom file name
                file_name = f"{main_person_data['name']} and {second_person_data['name']} - Synastry Chart.svg"
                custom_file_path = output_dir / file_name

                # Create the Synastry chart
                chart = KerykeionChartSVG(
                    AstrologicalSubject(
                        name=main_person_data["name"],
                        year=main_person_data["year"],
                        month=main_person_data["month"],
                        day=main_person_data["day"],
                        hour=main_person_data["hour"],
                        minute=main_person_data["minute"],
                        lng=main_person_data["longitude"],
                        lat=main_person_data["latitude"],
                        tz_str=main_person_data["timezone"]
                    ),
                    "Synastry",
                    AstrologicalSubject(
                        name=second_person_data["name"],
                        year=second_person_data["year"],
                        month=second_person_data["month"],
                        day=second_person_data["day"],
                        hour=second_person_data["hour"],
                        minute=second_person_data["minute"],
                        lng=second_person_data["longitude"],
                        lat=second_person_data["latitude"],
                        tz_str=second_person_data["timezone"]
                    ),
                    new_output_directory=str(output_dir),
                )
                chart.makeSVG()

                # Default file path created by Kerykeion
                default_file_path = output_dir / f"{main_person_data['name']} - Synastry Chart.svg"

                # Rename the file to match the desired format
                if default_file_path.exists():
                    default_file_path.rename(custom_file_path)

                # Verify if the renamed file exists
                if not custom_file_path.exists():
                    raise FileNotFoundError(f"The Synastry chart file was not found: {custom_file_path}")

                # Preview the chart
                self.preview_chart(custom_file_path)

            if chart_type == "Natal":
                subject = AstrologicalSubject(
                    person_data["name"],
                    person_data["year"],
                    person_data["month"],
                    person_data["day"],
                    person_data["hour"],
                    person_data["minute"],
                    lng=person_data["longitude"],
                    lat=person_data["latitude"],
                    tz_str=person_data["timezone"],
                )
                chart_file = output_dir / f"{subject.name} - Natal Chart.svg"
                chart = KerykeionChartSVG(subject, new_output_directory=str(output_dir))
                chart.makeSVG()
                QMessageBox.information(self, "Success", f"Natal chart saved at {chart_file}")
                self.preview_chart(chart_file)

            elif chart_type == "Transit":
                now = datetime.utcnow()
                natal_subject = AstrologicalSubject(
                    person_data["name"],
                    person_data["year"],
                    person_data["month"],
                    person_data["day"],
                    person_data["hour"],
                    person_data["minute"],
                    lng=person_data["longitude"],
                    lat=person_data["latitude"],
                    tz_str=person_data["timezone"],
                )
                transit_subject = AstrologicalSubject(
                    "Current Planetary Positions",
                    now.year,
                    now.month,
                    now.day,
                    now.hour,
                    now.minute,
                    lng=0.0,
                    lat=0.0,
                    tz_str="UTC",
                )
                chart_file = output_dir / f"{person_data['name']} - Transit Chart.svg"
                chart = KerykeionChartSVG(natal_subject, "Transit", transit_subject, new_output_directory=str(output_dir))
                chart.makeSVG()
                QMessageBox.information(self, "Success", f"Transit chart saved at {chart_file}")
                self.preview_chart(chart_file)

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def preview_chart(self, svg_path):
        try:
            # Ensure the file exists
            if not os.path.exists(svg_path):
                raise FileNotFoundError(f"The file {svg_path} does not exist.")

            # Close any existing preview window
            if self.preview_window:
                self.preview_window.close()
                self.preview_window = None

            # Create a new preview window
            self.preview_window = QMainWindow()
            self.preview_window.setWindowTitle("Chart Preview")
            self.preview_window.setGeometry(100, 100, 800, 600)

            # Load the SVG file into the browser
            browser = QWebEngineView()
            browser.setUrl(QUrl.fromLocalFile(os.path.abspath(svg_path)))

            # Setup the layout and display the preview window
            central_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(browser)
            central_widget.setLayout(layout)
            self.preview_window.setCentralWidget(central_widget)

            # Clear window reference when closed
            self.preview_window.destroyed.connect(lambda: setattr(self, "preview_window", None))
            self.preview_window.show()

        except FileNotFoundError as e:
            QMessageBox.critical(self, "File Not Found", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to preview chart: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AstrologyChartGenerator()
    window.show()
    sys.exit(app.exec_())

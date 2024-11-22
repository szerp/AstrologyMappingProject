import sys
import os  # Added for opening folders on Windows
import subprocess  # Added for opening folders on macOS/Linux
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QTabWidget,
    QFileDialog, QGridLayout  # Added QGridLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QIcon
from pathlib import Path
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime


def get_location_info(city, state, country):
    """Custom function to bypass Geonames."""
    geolocator = Nominatim(user_agent="astrology_app")
    location_query = f"{city}, {state}, {country}" if state else f"{city}, {country}"
    location = geolocator.geocode(location_query)
    if location:
        latitude, longitude = location.latitude, location.longitude
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=latitude, lng=longitude)
        if timezone is None:
            raise ValueError(f"Timezone not found for coordinates: {latitude}, {longitude}")
        return latitude, longitude, timezone
    else:
        raise ValueError(f"Location '{location_query}' not found.")

class AstrologyChartGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astrology Chart Generator")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("astrology_icon.png"))  # Custom icon
        self.init_ui()
        self.setStyleSheet(self.get_stylesheet())  # Apply custom stylesheet
        self.open_tabs = {}  # Track open tabs by file paths
        self.save_path = Path.cwd() / "generated_charts"  # Default save path

    def get_person_data(self, entries):
        """Retrieve and prepare person data."""
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
            
            # Use custom function to get location and timezone
            latitude, longitude, timezone = get_location_info(city, state, country)
            
            return {
                "name": name,
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
                "lat": latitude,   # Pass to AstrologicalSubject
                "lng": longitude,  # Pass to AstrologicalSubject
                "tz_str": timezone  # Pass to AstrologicalSubject
            }
        except ValueError as ve:
            raise ValueError(f"Invalid input: {ve}")
        except Exception as e:
            raise ValueError(f"Error retrieving location: {e}")

    # Other methods remain unchanged.

    def set_save_folder(self):
        """Open a dialog to set the save folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder", str(self.save_path))
        if folder:
            self.save_path = Path(folder)
            QMessageBox.information(self, "Save Folder", f"Save folder set to: {self.save_path}")
        else:
            QMessageBox.warning(self, "Set Save Folder", "No folder selected. Save folder not changed.")

    def open_save_folder(self):
        """Open the save folder in the system's file explorer."""
        try:
            if not self.save_path.exists():
                QMessageBox.warning(self, "Warning", f"The save folder does not exist: {self.save_path}")
                return

            # Cross-platform way to open a folder
            if sys.platform == "win32":
                os.startfile(self.save_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(self.save_path)], check=True)
            else:  # Linux and other platforms
                subprocess.run(["xdg-open", str(self.save_path)], check=True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open folder: {e}")

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left-side layout for input fields and buttons
        left_side_layout = QVBoxLayout()

        # Create input groups for Main and Second Person
        self.main_person = self.create_input_group("Main Person", "#ffffe0")
        self.second_person = self.create_input_group("Second Person", "#ffe6f7")

        # Add input groups vertically
        left_side_layout.addLayout(self.main_person["layout"])
        left_side_layout.addLayout(self.second_person["layout"])

        # Buttons for generating charts
        button_layout = QVBoxLayout()

        buttons = [
            ("Generate Natal Chart (1st)", lambda: self.generate_chart("Natal", self.main_person["entries"]), "#ffcccc"),
            ("Generate Transit Chart (1st)", lambda: self.generate_chart("Transit", self.main_person["entries"]), "#ccffcc"),
            ("Generate Natal Chart (2nd)", lambda: self.generate_chart("Natal", self.second_person["entries"]), "#ccccff"),
            ("Generate Transit Chart (2nd)", lambda: self.generate_chart("Transit", self.second_person["entries"]), "#ffffcc"),
            ("Generate Synastry Chart", lambda: self.generate_chart("Synastry", None), "#ffccff"),
            ("Clear Main Person", self.main_person["clear"], "#ffccee"),
            ("Clear Second Person", self.second_person["clear"], "#ccffee"),
        ]
        options_button = self.create_button("Set Save Folder", self.set_save_folder, "#d4d4d4")
        open_folder_button = self.create_button("Open Save Folder", self.open_save_folder, "#d4d4d4")
        button_layout.addWidget(options_button)
        button_layout.addWidget(open_folder_button)


        for text, func, color in buttons:
            btn = self.create_button(text, func, color)
            button_layout.addWidget(btn)

        left_side_layout.addLayout(button_layout)

        # Adjust proportions: Input on the left (20%), Preview on the right (80%)
        main_layout.addLayout(left_side_layout, 1)

        # Right-side layout for chart previews
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        main_layout.addWidget(self.tab_widget, 4)

        # Set the main layout
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
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        # Use a grid layout for aligned input fields
        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(1, 1)

        entries = {}
        for i, field in enumerate(["Name", "Year", "Month", "Day", "Hour", "Minute", "City", "State", "Country"]):
            label = QLabel(field)
            label.setFont(QFont("Arial", 11))
            entry = QLineEdit()
            entry.setFont(QFont("Arial", 11))
            entries[field.lower()] = entry

            grid_layout.addWidget(label, i, 0)  # Label in column 0
            grid_layout.addWidget(entry, i, 1)  # Input field in column 1

        frame_layout.addLayout(grid_layout)
        layout.addWidget(frame)

        def clear_entries():
            for entry in entries.values():
                entry.clear()

        return {"layout": layout, "entries": entries, "clear": clear_entries}

    def create_button(self, text, func, color):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 12, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 15px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.lighten_color(color)};
            }}
        """)
        button.clicked.connect(func)
        return button

    
    def darken_color(self, color):
        # Darken color for hover effect
        return color.replace("cc", "99").replace("ff", "cc")

    def lighten_color(self, color):
        # Lighten color for pressed effect
        return color.replace("cc", "ee").replace("ff", "ee")


    def get_location_info(self, city, state, country):
        geolocator = Nominatim(user_agent="astrology_app")
        location_query = f"{city}, {state}, {country}" if state else f"{city}, {country}"
        location = geolocator.geocode(location_query)
        if location:
            tf = TimezoneFinder()
            return location.latitude, location.longitude, tf.timezone_at(lat=location.latitude, lng=location.longitude)
        raise ValueError(f"Location '{location_query}' not found.")

        
    def generate_chart(self, chart_type, entries=None):
        try:
            output_dir = Path.cwd() / "generated_charts"
            output_dir.mkdir(parents=True, exist_ok=True)

            if chart_type == "Synastry":
                # Get data for both people
                main_person_data = self.get_person_data(self.main_person["entries"])
                second_person_data = self.get_person_data(self.second_person["entries"])

                # Define the filename with both names
                file_name = f"{main_person_data['name']} and {second_person_data['name']} - Synastry Chart.svg"
                chart_file = output_dir / file_name

                # Generate the Synastry chart
                chart = KerykeionChartSVG(
                    AstrologicalSubject(**main_person_data),
                    "Synastry",
                    AstrologicalSubject(**second_person_data),
                    new_output_directory=str(output_dir),
                )
                chart.makeSVG()

                # Default file path created by Kerykeion
                default_file_path = output_dir / f"{main_person_data['name']} - Synastry Chart.svg"

                # Rename the default file to match the desired format
                if default_file_path.exists() and not chart_file.exists():
                    default_file_path.rename(chart_file)

                # Verify if the renamed file exists
                if not chart_file.exists():
                    raise FileNotFoundError(f"The Synastry chart file was not found: {chart_file}")

                # Preview the generated chart
                self.preview_chart(chart_file)

            elif chart_type == "Transit":
                # Get data for the person
                person_data = self.get_person_data(entries)

                # Create a transit subject for current planetary positions
                now = datetime.utcnow()
                transit_subject = AstrologicalSubject(
                    name="Current Planetary Positions",
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=now.hour,
                    minute=now.minute,
                    lat=0.0,  # Default to Greenwich latitude
                    lng=0.0,  # Default to Greenwich longitude
                    tz_str="UTC",  # Default to UTC
                )

                # Define the filename for the transit chart
                file_name = f"{person_data['name']} - Transit Chart.svg"
                chart_file = output_dir / file_name

                # Generate the Transit chart
                natal_subject = AstrologicalSubject(**person_data)
                chart = KerykeionChartSVG(
                    natal_subject,
                    "Transit",
                    transit_subject,
                    new_output_directory=str(output_dir),
                )
                chart.makeSVG()

                # Preview the generated chart
                self.preview_chart(chart_file)

            else:  # For Natal charts
                person_data = self.get_person_data(entries)
                file_suffix = "Natal Chart"
                chart_file = output_dir / f"{person_data['name']} - {file_suffix}.svg"

                # Generate the Natal chart
                subject = AstrologicalSubject(**person_data)
                chart = KerykeionChartSVG(subject, new_output_directory=str(output_dir))
                chart.makeSVG()

                # Preview the generated chart
                self.preview_chart(chart_file)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def preview_chart(self, svg_path):
        try:
            for index in range(self.tab_widget.count()):
                if self.tab_widget.tabText(index) == Path(svg_path).stem:
                    self.tab_widget.setCurrentIndex(index)
                    return
            browser = QWebEngineView()
            browser.setUrl(QUrl.fromLocalFile(str(svg_path)))
            self.tab_widget.addTab(browser, Path(svg_path).stem)
            self.tab_widget.setCurrentWidget(browser)
        except Exception as e:  # Fixed indentation
            QMessageBox.critical(self, "Error", f"Failed to preview chart: {e}")

    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        for path, tab in self.open_tabs.items():
            if tab == widget:
                del self.open_tabs[path]
                break
        self.tab_widget.removeTab(index)

    def get_stylesheet(self):
        return """
        QWidget {
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(255, 182, 193, 255), stop:1 rgba(173, 216, 230, 255)
            );
            font-family: 'Arial';
        }
        QPushButton {
            border: 2px solid #fff;
            color: #333;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AstrologyChartGenerator()
    window.show()
    sys.exit(app.exec_())

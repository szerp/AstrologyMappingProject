import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QGridLayout, QTabWidget, QFileDialog
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
from PyQt5.QtGui import QFont, QIcon  # Add QIcon here


# Define the pastel magical girl color map
PASTEL_MAGICAL_GIRL_COLORS = {
    # General Text and Background
    "#000000": "#000000",  # Text → Black for sharp readability (used for all text)
    "#ffffff": "#ffffff",  # White → White (background color)

    # Wheel Colors
    "#0000ff": "#7FBFFF",  # Blue → Brighter pastel blue (used for Air signs)
    "#06537f": "#06537f",  # Dark teal → Dark teal (used for Water signs)
    "#124500": "#124500",  # Dark green → Dark green (used for Earth signs)
    "#150052": "#DB6EC0",  # Deep purple → Brighter pastel lavender (used for House lines)
    "#160": "#DB6EC0",     # Dark olive → Brighter blush pink (used for Fire signs)
    "#176": "#DB6EC0",     # Olive → Brighter blush pink (used for Fire signs)
    "#1f99b3": "#DB6EC0",  # Teal → Brighter pastel aqua (used for Water signs)
    "#26bbcf": "#8FD3FF",  # Cyan → Brighter pastel sky blue (used for Air signs)
    "#2b4972": "#A7CFFF",  # Navy → Brighter pastel periwinkle (used for Water elements)

    # Earth Element (Greens)
    "#36d100": "#387038",  # Bright green → Forest green (used for Earth symbols)
    "#666f06": "#387038",  # Olive green → Forest green (used for Earth-related signs)
    "#6a2d04": "#387038",  # Reddish-brown → Forest green (used for Earth elements)
    "#6b3d00": "#387038",  # Dark orange → Forest green (used for Earth signs)
    "#713f04": "#387038",  # Deep orange → Forest green (used for Earth-related aspects)
    "#7a9810": "#387038",  # Olive → Forest green (used for Earth signs)
    "#984b00": "#387038",  # Orange-brown → Forest green (used for Earth aspects)
    "#985a10": "#387038",  # Burnt orange → Forest green (used for Earth symbols)

    # Air Element (Purples)
    "#6f0766": "#A080FF",  # Dark magenta → Vibrant pastel purple (used for Air symbols)
    "#6f76d1": "#A080FF",  # Blue-purple → Vibrant pastel purple (used for Air-related signs)
    "#810757": "#A080FF",  # Deep magenta → Vibrant pastel purple (used for Air aspects)
    "#510060": "#A080FF",  # Deep purple → Vibrant pastel purple (used for Air symbols)
    "#5757e2": "#A080FF",  # Bright blue → Vibrant pastel purple (used for Air-related elements)
    "#630e73": "#A080FF",  # Dark purple → Vibrant pastel purple (used for Air aspects)

    # Fire Element (Reds)
    "#F00": "#DB6EC0",     # Bright red → Darker Brick Red (used for Fire symbols)
    "#FF0000": "#DB6EC0",  # Red → Brighter peachy pink (used for Fire-related elements)
    "#ff7200": "#DB6EC0",  # Bright orange → Brighter coral pink (used for Fire signs)
    "#ff7e00": "#DB6EC0",  # Deep orange → Brighter coral pink (used for Fire aspects)
    "#ff6600": "#DB6EC0",  # Orange → Brighter coral pink (used for Fire symbols)

    # Water Element (Blues)
    "#8FD3FF": "#375B73",  # Cyan → Deep Ocean Blue (used for Water symbols)
    "#2b4972": "#375B73",  # Navy → Deep Ocean Blue (used for Water-related signs)

    # House Dividing Lines (Neutral Gray)
    "#404040": "#000000",  # Pure Black for sharp contrast (used for house dividing lines)

    # Miscellaneous (Signs, Points, Aspects)
    "#b14e58": "#DB6EC0",  # Rosewood → Brighter salmon pink (used for Venus and similar aspects)
    "#d59e28": "#d59e28",  # Gold → Brighter pastel coral (used for Sun-related aspects)
    "#dc0000": "#DB6EC0",  # Bright red → Brighter peachy pink (used for Mars and similar aspects)
    "#520800": "#DB6EC0",  # Brownish red → Brighter dusty rose (used for Saturn aspects)
    "#400052": "#DB6EC0",  # Deep violet → Brighter pastel lavender (used for Neptune aspects)
    "#47133d": "#DB6EC0",  # Wine → Brighter pastel coral (used for Pluto aspects)
}







def change_svg_colors(svg_path, output_path, color_map):
    import xml.etree.ElementTree as ET
    import re

    # Normalize color_map to handle case insensitivity
    color_map = {k.lower(): v for k, v in color_map.items()}

    try:
        # Parse the SVG file
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Namespace handling
        namespaces = {'svg': 'http://www.w3.org/2000/svg'}
        ET.register_namespace('', namespaces['svg'])

        # Track whether changes were made
        changes_made = False

        # Find the <style> block
        for style_elem in root.findall(".//{http://www.w3.org/2000/svg}style"):
            css_content = style_elem.text
            if css_content:
                # Match CSS variables
                css_variable_regex = re.compile(r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,6});")
                updated_css_content = css_content

                # Replace CSS variables with pastel colors
                for match in css_variable_regex.finditer(css_content):
                    css_var, original_color = match.groups()
                    if original_color.lower() in color_map:
                        updated_color = color_map[original_color.lower()]
                        updated_css_content = updated_css_content.replace(
                            f"{css_var}: {original_color}", f"{css_var}: {updated_color}"
                        )
                        changes_made = True

                # Update the <style> block
                style_elem.text = updated_css_content

        # Update inline `fill`, `stroke`, and `style` attributes
        for elem in root.iter():
            # Check for `fill` and `stroke`
            if 'fill' in elem.attrib:
                original_fill = elem.attrib['fill'].lower()
                if original_fill in color_map:
                    elem.attrib['fill'] = color_map[original_fill]
                    changes_made = True
            if 'stroke' in elem.attrib:
                original_stroke = elem.attrib['stroke'].lower()
                if original_stroke in color_map:
                    elem.attrib['stroke'] = color_map[original_stroke]
                    changes_made = True

            # Check for `style` attribute
            if 'style' in elem.attrib:
                style = elem.attrib['style']
                updated_style = style
                color_regex = re.compile(r"(fill|stroke):\s*(#[0-9a-fA-F]{3,6})")
                for attr, color in color_regex.findall(style):
                    lower_color = color.lower()
                    if lower_color in color_map:
                        updated_style = updated_style.replace(color, color_map[lower_color])
                        changes_made = True
                elem.attrib['style'] = updated_style

        # Save changes to the output SVG file
        if changes_made:
            tree.write(output_path)
            print(f"Modified SVG written to: {output_path}")
        else:
            print("No changes made to the SVG.")

    except Exception as e:
        print(f"Error processing SVG file: {e}")


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
                "latitude": latitude,  # Updated key
                "longitude": longitude,  # Updated key
                "timezone": timezone  # Updated key
            }
        except ValueError as ve:
            raise ValueError(f"Invalid input: {ve}")
        except Exception as e:
            raise ValueError(f"Error retrieving location: {e}")


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

            if chart_type in ["Natal", "Transit"]:
                person_data = self.get_person_data(entries)

            if chart_type == "Synastry":
                main_person_data = self.get_person_data(self.main_person["entries"])
                second_person_data = self.get_person_data(self.second_person["entries"])

                file_name = f"{main_person_data['name']} and {second_person_data['name']} - Synastry Chart.svg"
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

                # Apply pastel colors to the generated SVG
                default_file_path = output_dir / f"{main_person_data['name']} - Synastry Chart.svg"
                pastel_file_path = output_dir / file_name
                change_svg_colors(default_file_path, pastel_file_path, PASTEL_MAGICAL_GIRL_COLORS)

                # Preview the pastel chart
                self.preview_chart(pastel_file_path)

            elif chart_type == "Natal":
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
                pastel_chart_file = output_dir / f"{subject.name} - Natal Chart (Pastel).svg"
                chart = KerykeionChartSVG(subject, new_output_directory=str(output_dir))
                chart.makeSVG()

                # Apply pastel colors to the generated SVG
                change_svg_colors(chart_file, pastel_chart_file, PASTEL_MAGICAL_GIRL_COLORS)

                # Preview the pastel chart
                self.preview_chart(pastel_chart_file)

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
                pastel_chart_file = output_dir / f"{person_data['name']} - Transit Chart (Pastel).svg"
                chart = KerykeionChartSVG(natal_subject, "Transit", transit_subject, new_output_directory=str(output_dir))
                chart.makeSVG()

                # Apply pastel colors to the generated SVG
                change_svg_colors(chart_file, pastel_chart_file, PASTEL_MAGICAL_GIRL_COLORS)

                # Preview the pastel chart
                self.preview_chart(pastel_chart_file)

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


    def preview_chart(self, html_path):
        try:
            for index in range(self.tab_widget.count()):
                if self.tab_widget.tabText(index) == Path(html_path).stem:
                    self.tab_widget.setCurrentIndex(index)
                    return
            browser = QWebEngineView()
            browser.setUrl(QUrl.fromLocalFile(str(html_path)))
            self.tab_widget.addTab(browser, Path(html_path).stem)
            self.tab_widget.setCurrentWidget(browser)
        except Exception as e:
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

import os
from tkinter import messagebox, Tk, Canvas, PhotoImage, Frame, Label, Entry, Button
from PIL import Image, ImageTk
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pathlib import Path
from datetime import datetime
import webbrowser
import tkinter as tk

# Function to get latitude, longitude, and timezone
def get_location_info(city_name, state_name, country_name):
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

# Function to preview chart by opening the SVG in the default browser
def preview_chart(svg_path):
    try:
        webbrowser.open(svg_path.as_uri())
        messagebox.showinfo("Preview", f"SVG chart opened in your browser.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to preview chart: {e}")

# Function to generate charts
def generate_chart(chart_type, person):
    try:
        if person == "first":
            details = main_person_entries
        else:
            details = second_person_entries

        name = details["name"].get()
        year = int(details["year"].get())
        month = int(details["month"].get())
        day = int(details["day"].get())
        hour = int(details["hour"].get())
        minute = int(details["minute"].get())
        city = details["city"].get()
        state = details["state"].get()
        country = details["country"].get()

        latitude, longitude, timezone = get_location_info(city, state, country)

        natal_subject = AstrologicalSubject(
            name, year, month, day, hour, minute,
            lng=longitude, lat=latitude, tz_str=timezone, city=city
        )

        output_dir = Path.cwd() / "generated_charts"
        output_dir.mkdir(parents=True, exist_ok=True)

        if chart_type == "Natal":
            chart_file = output_dir / f"{name} - Natal Chart.svg"
            chart = KerykeionChartSVG(natal_subject, new_output_directory=str(output_dir))
            chart.makeSVG()
            messagebox.showinfo("Success", f"Natal chart saved at {chart_file}")
            preview_chart(chart_file)

        elif chart_type == "Transit":
            now = datetime.utcnow()
            transit_subject = AstrologicalSubject(
                "Current Planetary Positions", now.year, now.month, now.day,
                now.hour, now.minute, lng=0.0, lat=0.0, tz_str="UTC"
            )
            chart_file = output_dir / f"{name} - Transit Chart.svg"
            chart = KerykeionChartSVG(natal_subject, "Transit", transit_subject, new_output_directory=str(output_dir))
            chart.makeSVG()
            messagebox.showinfo("Success", f"Transit chart saved at {chart_file}")
            preview_chart(chart_file)

        elif chart_type == "Synastry":
            second_details = second_person_entries
            second_name = second_details["name"].get()
            second_year = int(second_details["year"].get())
            second_month = int(second_details["month"].get())
            second_day = int(second_details["day"].get())
            second_hour = int(second_details["hour"].get())
            second_minute = int(second_details["minute"].get())
            second_city = second_details["city"].get()
            second_state = second_details["state"].get()
            second_country = second_details["country"].get()

            second_lat, second_lng, second_tz = get_location_info(second_city, second_state, second_country)

            second_subject = AstrologicalSubject(
                second_name, second_year, second_month, second_day, second_hour, second_minute,
                lng=second_lng, lat=second_lat, tz_str=second_tz, city=second_city
            )

            chart_file = output_dir / f"{name} - Synastry Chart.svg"
            chart = KerykeionChartSVG(natal_subject, "Synastry", second_subject, new_output_directory=str(output_dir))
            chart.makeSVG()
            messagebox.showinfo("Success", f"Synastry chart saved at {chart_file}")
            preview_chart(chart_file)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_main_person():
    for entry in main_person_entries.values():
        entry.delete(0, 'end')

def clear_second_person():
    for entry in second_person_entries.values():
        entry.delete(0, 'end')

# Function to create gradient background
def create_gradient_image(width, height, start_color, end_color):
    image = PhotoImage(width=width, height=height)
    start_rgb = [int(start_color[i:i+2], 16) for i in (1, 3, 5)]
    end_rgb = [int(end_color[i:i+2], 16) for i in (1, 3, 5)]

    for y in range(height):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * y // height
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * y // height
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * y // height
        line_color = f'#{r:02x}{g:02x}{b:02x}'
        image.put(line_color, to=(0, y, width, y + 1))

    return image


# Function to calculate a darker shade of a hex color
def darken_color(hex_color, factor=0.7):
    rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
    darkened = [max(0, int(c * factor)) for c in rgb]
    return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

# Function to add hover effect
def add_hover_effect(button, bg_color):
    hover_color = darken_color(bg_color)

    def on_enter(event):
        button.config(bg=hover_color)

    def on_leave(event):
        button.config(bg=bg_color)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

#  GUI Setup
app = Tk()
app.title("Astrology Chart Generator")
app.geometry("1200x800")

canvas = Canvas(app, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Update gradient on resize
def on_resize(event):
    global gradient_image
    gradient_image = create_gradient_image(event.width, event.height, "#b3e5fc", "#f8bbd0")
    canvas.create_image(0, 0, anchor="nw", image=gradient_image)

gradient_image = create_gradient_image(1200, 800, "#b3e5fc", "#f8bbd0")
canvas.create_image(0, 0, anchor="nw", image=gradient_image)

canvas.bind("<Configure>", on_resize)

# Header Section
header_frame = Frame(canvas, bg="#ffe6f7")
header_frame.place(relx=0.5, rely=0.05, anchor="n")

original_icon = Image.open("astrology_icon.png").resize((100, 100), Image.Resampling.LANCZOS)
icon = ImageTk.PhotoImage(original_icon)

Label(header_frame, image=icon, bg="#ffe6f7").pack()
Label(
    header_frame,
    text="✨ Astrology Chart Generator ✨",
    font=("Comic Sans MS", 20),
    bg="#ffe6f7",
    fg="#d81b60",
).pack()

# Input Fields
input_frame = Frame(canvas, bg="#f0f8ff")
input_frame.place(relx=0.5, rely=0.3, anchor="n")

main_person_shadow = Frame(input_frame, bg="#d3d3d3")
main_person_shadow.grid(row=0, column=0, padx=16, pady=12)
main_person_frame = Frame(main_person_shadow, bg="#ffffe0", relief="ridge", borderwidth=2)
main_person_frame.pack(padx=2, pady=2)

second_person_shadow = Frame(input_frame, bg="#d3d3d3")
second_person_shadow.grid(row=0, column=1, padx=16, pady=12)
second_person_frame = Frame(second_person_shadow, bg="#ffe6f7", relief="ridge", borderwidth=2)
second_person_frame.pack(padx=2, pady=2)

fields = [("Name", "name"), ("Year", "year"), ("Month", "month"), ("Day", "day"),
          ("Hour", "hour"), ("Minute", "minute"), ("City", "city"), ("State", "state"),
          ("Country", "country")]

main_person_entries = {}
second_person_entries = {}

for idx, (label_text, var_name) in enumerate(fields):
    Label(main_person_frame, text=label_text, bg="#ffffe0", font=("Arial", 12)).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
    entry = Entry(main_person_frame, font=("Arial", 12), width=25)
    entry.grid(row=idx, column=1, padx=5, pady=5)
    main_person_entries[var_name] = entry

    Label(second_person_frame, text=label_text, bg="#ffe6f7", font=("Arial", 12)).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
    entry = Entry(second_person_frame, font=("Arial", 12), width=25)
    entry.grid(row=idx, column=1, padx=5, pady=5)
    second_person_entries[var_name] = entry

# Buttons Section
button_frame_1 = Frame(canvas, bg="#f0f8ff")
button_frame_1.place(relx=0.5, rely=0.775, anchor="n")

button_frame_2 = Frame(canvas, bg="#f0f8ff")
button_frame_2.place(relx=0.5, rely=0.85, anchor="n")

buttons_1 = [
    ("Generate Natal Chart (1st)", lambda: generate_chart("Natal", "first"), "#ffcccc"),
    ("Generate Transit Chart (1st)", lambda: generate_chart("Transit", "first"), "#ccffcc"),
    ("Clear Main Person", clear_main_person, "#ffccee"),
]

buttons_2 = [
    ("Generate Natal Chart (2nd)", lambda: generate_chart("Natal", "second"), "#ccccff"),
    ("Generate Transit Chart (2nd)", lambda: generate_chart("Transit", "second"), "#ffffcc"),
    ("Clear Second Person", clear_second_person, "#ccffee"),
    ("Generate Synastry Chart", lambda: generate_chart("Synastry", "both"), "#ffccff"),
]

# Add buttons for the 1st row
for text, command, color in buttons_1:
    btn = Button(
        button_frame_1, text=text, command=command, bg=color,
        fg="#000000", font=("Arial", 10, "bold"), relief="flat", width=25, height=2
    )
    btn.pack(side="left", padx=10, pady=5)
    add_hover_effect(btn, color)

# Add buttons for the 2nd row
for text, command, color in buttons_2:
    btn = Button(
        button_frame_2, text=text, command=command, bg=color,
        fg="#000000", font=("Arial", 10, "bold"), relief="flat", width=25, height=2
    )
    btn.pack(side="left", padx=10, pady=5)
    add_hover_effect(btn, color)

app.mainloop()
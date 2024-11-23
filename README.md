# 🌟 Astrology Chart Generator 🌙✨

Welcome to **Astrology Chart Generator**, a magical desktop application designed to create stunning, customizable astrology charts. Whether you're a seasoned astrologer or just curious about the stars, this app offers an intuitive interface to generate **Natal**, **Transit**, and **Synastry** charts, all styled with a **Magical and Feminine** aesthetic. 🌸💫

[💖 Support the Project on Ko-fi! 💖](https://ko-fi.com/nyahmii)

---

## 🌌 **Problem Statement**

Astrology enthusiasts often rely on web-based tools to create charts but face limitations in customization and aesthetics. This project bridges the gap by offering a **desktop application** that combines functionality with artistic charm, enabling users to generate personalized, visually captivating astrology charts. 🪄✨

---

## ✨ **Key Features**

🌟 **User-Friendly Interface**  
Designed for all skill levels, the app makes chart creation effortless and enjoyable.  

🎨 **Customizable Color Themes**  
Includes the unique color palette, blending whimsy with elegance for beautifully styled charts.  
Additionally the program will create a chart with the original Kerykeion style for readability or in case another color palette is desired. 

🪐 **Dynamic Chart Types**  
Generate **Natal**, **Transit**, and **Synastry** charts with ease, tailored to user input.  

📂 **Local Save Options**  
Save your charts directly to your computer, ensuring easy access anytime, anywhere.  

💾 **SVG Chart Customization**  
Modify chart elements using pre-defined color mappings to match your personal aesthetic.

---

## 🌟 **Methodologies**

### **Programming Frameworks and Libraries**
- 🖥️ **PyQt**: Crafted a responsive, interactive user interface.
- ✨ **Kerykeion**: Powered astrological calculations and SVG chart generation.
- 🌍 **Geopy & TimezoneFinder**: Ensured accurate location and timezone calculations based on user input.
- 🧙‍♀️ **XML Manipulation**: Applied custom color mappings to SVG charts for a magical touch.

### **Design and User Interaction**
- 💎 **Custom Styling**: Leveraged PyQt stylesheets to create an immersive, polished experience.
- 🛡️ **Input Validation**: Enhanced usability by ensuring all input fields are correctly filled before generating charts.
- 🌈 **Color Mapping**: Introduced fully customizable color themes to enhance chart readability and aesthetic.

---

## 🪄 **Key Results**

- 🌸 **Visual Aesthetics**: Generated enchanting astrology charts with a perfect balance of functionality and style.
- 🌍 **Accurate Location Integration**: Seamlessly calculated precise locations and timezones for reliable results.
- 🚀 **Robust Deployment**: Successfully packaged the app into a desktop executable for easy installation.

---

## 🌟 **How It Works**

1. 📝 **Enter Details**: Input your name, birth date, time, and location.  
2. 🔮 **Generate Chart**: Select the type of chart you want to create (Natal, Transit, or Synastry).  
3. 🌈 **Preview & Save**: View the chart styled with a magical theme and save it to your computer.  
4. 🎨 **Customize**: Edit SVG files for further personalization using pre-defined color mappings. (Would require modifiying the colors in the script)

---

## 📊 **Data Sources**

- 🌍 **Location Data**: [Nominatim API (Geopy)](https://nominatim.org/)  
- 🕰️ **Timezone Data**: [TimezoneFinder](https://pypi.org/project/timezonefinder/)
- Chart generation sources - Kerykeion
---

## 💻 **Technologies Used**

- **Python** 🐍  
- **PyQt** 🎨  
- **Kerykeion** 🪐  
- **Geopy & TimezoneFinder** 🌍  
- **HTML/CSS for SVG Styling** ✨  
- **ElementTree for XML Manipulation** 📜  

---

## 🎨 **Screenshots**

### 🌸 **Natal Chart Example**
![image](https://github.com/user-attachments/assets/81bfc6d7-6ace-4a11-a399-6b594b6aabb8)

### 🌙 **Transit Chart Example**
![image](https://github.com/user-attachments/assets/179c47cd-038d-4d10-abd0-e12cbbd2b883)


### 🌟 **Synastry Chart Example**
![image](https://github.com/user-attachments/assets/8238dca1-0fdb-448b-a201-bbe1df2b3cee)

---

## 👩‍💻 **Authors**

**Sarahit Zerpa (Nyahmii)**    
---

## **Powered by Kerykeion**
    AstroChart Generator uses Kerykeion as the primary library for astrological calculations and chart generation.
    Kerykeion is a Python library for astrology that provides robust functionalities for natal chart analysis, synastry, and other astrological features.

    Kerykeion also supports SVG chart outputs, which we customized further to match the magical aesthetic of our application. A huge thank you to the contributors of Kerykeion for making astrology programming accessible and enjoyable.

---

## 💖 **Support the Project**

If you loved this project and want to see more magical features or new projects, consider [buying me a coffee on Ko-fi](https://ko-fi.com/yourusername). Your support helps keep this project alive and ✨ magical! ✨

---

## 🌟 **License**

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to copy-paste this into your GitHub repository's README file and adjust as needed!

---
## 📖 **Instructions to Run the Astrology Chart Generator**

Follow these steps to download and run the Astrology Chart Generator from this repository:
Step 1: Install Python 3.9

    This project is only compatible with Python 3.9.
        Download and install Python 3.9 from the official Python website.
        Important: During installation, check the box for "Add Python to PATH" to ensure Python is available in your terminal/command prompt.

Step 2: Clone the Repository

    Clone this repository to your local machine using Git or download it as a ZIP file:
        Using Git:

        git clone https://github.com/AstrologyMappingProject.git
        cd AstrologyMappingProject

        Downloading as ZIP:
            Click the green "Code" button in the repository and select "Download ZIP".
            Extract the ZIP file to your desired folder.

Step 3: Install Required Dependencies

    Open a terminal or command prompt in the directory where the repository is located.
    Install the required Python libraries using pip:

    pip install -r requirements.txt

    This will install the necessary dependencies, including:

        PyQt5

        Kerykeion

        Geopy

        TimezoneFinder

        Any other required libraries

        Note: Ensure you are using Python 3.9 and not a different version.

Step 4: Run the Application

    Execute the main script to launch the application:

    python AstroCharter.py

    The app's graphical interface should appear. You can now start generating astrology charts!

Step 5: Save and Access Generated Charts

    Charts will be saved in the generated_charts folder by default.
    You can change the save folder in the app settings or browse the default folder.

🔧 Troubleshooting

If you encounter issues, here are some tips:

    Ensure all dependencies are installed. If pip install fails, ensure you are using Python 3.9 and try upgrading pip:

    python -m pip install --upgrade pip

    If location or timezone data fails, ensure you have a working internet connection.
    For Mac and Linux users, replace python with python3.9 in commands.

📦 Optional: Create a Virtual Environment

To avoid conflicts with other Python projects, use a virtual environment:

    Create a virtual environment:

python -m venv env

Activate the virtual environment:

    On Windows:

env\Scripts\activate

On macOS/Linux:

    source env/bin/activate

Install dependencies in the virtual environment:

    pip install -r requirements.txt

💻 Compiling into an Executable File (EXE)

If you are skilled in Python packaging and know how to compile Python into an executable file (EXE), I would be amazed and grateful if you could show me how to do it properly.

I have attempted methods such as PyInstaller and auto-py-to-exe, but I encountered errors related to missing dependencies. If you successfully compile the application, please share the steps so I can include them in this repository. Thank you in advance! 🙏✨
🌟 Feedback and Contributions

If you encounter issues, have suggestions for improvement, or successfully compile the app into an executable, feel free to:

    Open an issue
    Submit a pull request
    Share your experience or ideas

Happy charting! ✨

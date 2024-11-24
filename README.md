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
# Astrology Chart Generator: Instructions for Recreating and Building the App

This guide provides instructions for setting up the environment, running the application, and building both `default` and `onefile` executables using PyInstaller.

---
## **1️⃣ Setting Up the Python Environment**

### 🛠️ Steps:
1. **Install Anaconda or Miniconda**  
   - Download and install Anaconda/Miniconda from [conda.io](https://www.anaconda.com/).

2. **Create the Conda Environment**  
   Open Anaconda Prompt and run:
   ```bash
   conda create -n AstrologyMappingPython39 python=3.9

3. **Activate the Environment**

conda activate AstrologyMappingPython39

4. **Install Dependencies**
Install the required Python libraries:

pip install pyswisseph kerykeion PyQt5 geopy timezonefinder pyinstaller

5.**Verify Installation**
Run the following command to confirm all required libraries are installed:

pip show pyswisseph kerykeion PyQt5 geopy timezonefinder pyinstaller

---
## **2️⃣ Preparing the Code**
### 📂 Steps:

    Save the Python Code
        Save the AstroCharter.py file in your working directory:

        C:/Users/Nyahmii/Documents/AstrologyMappingProject/AstroCharter.py

    Place Supporting Files
        Ensure the astrology_icon.ico file is present in the same directory.

## **3️⃣ Building the Executables**
### Option A: Default Build (Folder Output)

    Save the Default Spec File
    Save the AstroCharter-default.spec file in your working directory.

    Run PyInstaller with the Default Spec

pyinstaller AstroCharter-default.spec --distpath builder_default --workpath build_default

Output
The executable will be located in:

    builder_default/AstroCharter/

### Option B: Onefile Build (Single Executable)

    Save the Onefile Spec File
    Save the AstroCharter-onefile.spec file in your working directory.

    Run PyInstaller with the Onefile Spec

pyinstaller AstroCharter-onefile.spec --distpath builder_onefile --workpath build_onefile

Output
The single executable will be located in:

    builder_onefile/

## **4️⃣ File Structure for Bundling Resources**

Ensure the datas section in both .spec files includes all necessary paths. For the kerykeion package, the required directories are:

    kerykeion/sweph
    kerykeion/settings

Example datas section in a .spec file:

datas=[
    ('C:/Users/<User_Name>/anaconda3/envs/AstrologyMappingPython39/lib/site-packages/kerykeion', 'kerykeion'),
],

## **5️⃣ Debugging and Improvements**
### 🛠️ Common Issues and Fixes:

    Error Handling for Missing Files
    If you encounter missing files like seas_18.se1, verify the paths in the datas section of the .spec file and ensure they are correctly included in the build.

    Runtime Issues
    If the app has runtime issues with the onefile build, consider using the --onedir build instead to keep files unpacked.

    Console vs. GUI
    Ensure console=False in the EXE section of the .spec file to avoid opening a console window for the GUI application.

## **6️⃣ Folder Structure After Builds**
### Default Build:

builder_default/
    AstroCharter/
        AstroCharter.exe

Onefile Build:

builder_onefile/
    AstroCharterApp.exe

## **7️⃣ Running the Application**
### 🚀 Steps to Run:

    Default Build:
    Navigate to:

builder_default/AstroCharter/AstroCharter.exe

Onefile Build:
Navigate to:

    builder_onefile/AstroCharterApp.exe

## **8️⃣ Final Notes**
### 📌 Recommendations:

    Test Both Executables
    Always test both default and onefile builds to ensure all dependencies are included and the application runs correctly.

    Preserve Spec Files
    Keep backups of .spec files in case of overwrites or future updates.

    Separate Builds
    Use distinct --distpath and --workpath values for different build types to avoid overwriting files.

## **🎉 Contributing and Feedback**

If you encounter issues, have suggestions for improvement, or successfully compile the app into an executable, feel free to:

    Open an issue 💬
    Submit a pull request 📂
    Share your experience or ideas 📝

Happy charting! ✨🌌

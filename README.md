# OCR-Driven UI Automation Framework
### *Robot Framework • Docker/Podman Tesseract • Python (OpenCV, PyAutoGUI) • Windows + Linux Support*

This repository contains a **cross-platform UI automation framework** for automating desktop interfaces using **OCR + image-based detection**, even when no DOM, accessibility tree, or automation interface exists.

---

## 🚀 Features

### 🔍 OCR Keyword Detection
- Captures screenshots (full-screen or window-only)  
- Runs Tesseract OCR **inside a Docker/Podman container**  
- Fuzzy matching via `difflib`  
- Supports wildcards (e.g., `* conflicts found`)  
- Returns bounding-box **center coordinates**  

### 🖼 Icon Detection Next to Text
- Slices screenshot horizontally along the target text row  
- OpenCV template matching  
- Custom similarity threshold  
- Ensures icons are aligned on the **same horizontal axis**  
- Avoids false matches elsewhere  

### 🪟 Cross-Platform Window Control

#### **Windows**
- PyGetWindow + RPA.Windows  
- Activate, bring-to-front, maximize  
- Accurate geometry for slicing screenshots  

#### **Linux (RHEL/Rocky/Ubuntu/etc.)**
- Uses `wmctrl` and `xwininfo`  
- Scaling-adjusted coordinates  
- Supports window-only screenshots  

### 📸 Window-Only Screenshots
- Detects active window  
- Extracts usable bounds  
- Captures only the window content (not the whole desktop)  

### 🐳 Containerized Tesseract
- Fully encapsulated OCR  
- Works with both Docker and Podman  
- Zero host dependencies  

---

## 📦 Project Structure
```
├── findKeyword.robot
├── Click_Icon_Next_To_Keyword.robot
├── parse_service.py
├── find_icon_pos.py
├── window_management.py
├── screenshot_window.py
├── mouse_actions.py
├── README.md
└── support/
├── docker_login.sh
├── docker_login.ps1
└── icons/
```

---

## 🔧 Requirements

### **Windows**
- Python 3.9+  
- Robot Framework  
- Podman (recommended) or Docker  
- Required Python modules:
  - pyautogui  
  - pillow  
  - opencv-python  
  - bs4  
  - difflib (built-in)  
  - RPA.Windows  
  - PyGetWindow  

---

### **Linux (RHEL/Rocky/CentOS)**

Install system dependencies:
```bash
sudo yum install wmctrl xdotool xorg-x11-server-utils
````

Install Python modules:

```bash
pip install robotframework pyautogui pillow opencv-python bs4 difflib
```

For headless mode (CI-friendly):

```bash
sudo yum install xorg-x11-server-Xvfb
Xvfb :99 &
export DISPLAY=:99
```

---

## 🐳 Docker/Podman Setup

### 1) Login to registry
Linux:

```bash
./support/docker_login.sh
```

Windows:

```powershell
.\support\docker_login.ps1
```

### 2) Pull the OCR image
```bash
podman pull tesseract-ocr:latest --tls-verify=false
```

---

## 🤖 Core Robot Usage

### OCR Keyword Lookup
```robot
${center_x}    ${center_y}=    Select_Keyword    * conflicts found
pyautogui.click    ${center_x}    ${center_y}
```

### Click Icon Next to Keyword
```robot
Click_Icon_Next_To_Keyword    support/icons/gear.png    * settings
```

This performs:

1. OCR keyword detection
2. Bounding box extraction
3. Horizontal row slicing
4. Template matching
5. Clicking the correct icon

---

## 🧠 Python Module Overview

### **parse_service.py**
* Parses HOCR XML
* Reconstructs multi-word strings
* Fuzzy matching
* Wildcard support (`*`)

### **find_icon_pos.py**
* OpenCV template match
* Row-based region slicing
* Adjustable similarity threshold
* Returns icon center coordinates

### **window_management.py**
* Windows: PyGetWindow + RPA.Windows
* Linux: wmctrl + xwininfo
* Retrieves active window geometry
* Maximizes or focuses window

### **screenshot_window.py**
* Captures window-only screenshots
* Uses geometry from `window_management.py`

### **mouse_actions.py**
* Triple-click
* Right-click
* Drag & drop utilities

---

## ▶️ Running Tests

### Windows:
```powershell
robot findKeyword.robot
```

### Linux:
```bash
export DISPLAY=:1
robot findKeyword.robot
```

---

## 🧪 Example Test Case
```robot
*** Test Cases ***
Open Settings Via OCR
    ${x}    ${y}=    Select_Keyword    * settings
    Click_Icon_Next_To_Keyword    icons/gear.png    * settings
```

---

## 📁 Support Scripts

### **docker_login.sh**
Authenticates Podman/Docker using a JSON credentials file.

### **docker_login.ps1**
PowerShell version for Windows authentication.

---

## 🐞 Troubleshooting

### Incorrect Linux Coordinates
* `xwininfo` is used as fallback automatically

### Podman TLS Errors
```bash
podman pull --tls-verify=false ...
```

### Linux Screenshot Flash
* Disable screen-flash animation in GNOME settings

### PyAutoGUI Typing Wrong Characters (Linux)
```bash
export XKB_DEFAULT_OPTIONS=""
```

---

## 🤝 Contributing
Pull requests are welcome — improvements to template matching, OCR parsing, and cross-platform window handling are especially appreciated.

---

## 📄 License
MIT License — open for commercial and personal use.

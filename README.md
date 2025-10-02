# Facial Recognition System for Classrooms

Facial recognition system developed for automated attendance management in educational environments. The application uses computer vision technology to authenticate teachers through facial biometrics, automatically recording attendance when a scheduled class matches the time and day of the week.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to Use](#how-to-use)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)

## About the Project

The system was designed to automate teacher attendance control in classrooms through facial recognition. Instead of traditional methods like signature sheets or access cards, the teacher simply positions themselves in front of the camera and is automatically authenticated.

### How It Works

1. User selects a classroom in the system
2. Camera is automatically activated and displays scheduled classes for that room
3. When a teacher positions themselves in front of the camera, the system:
   - Detects and recognizes the face through computer vision algorithms
   - Validates identity by comparing with the facial encodings database
   - Verifies if there is a scheduled class at that time and day of the week
   - Automatically registers access with timestamp in the database
4. Immediate visual feedback is displayed confirming authentication

### Use Cases

- Educational institutions that want to automate teacher attendance control
- Schools that need classroom access auditing
- Environments requiring biometric security for access
- Management of schedules and recurring class grids

## Features

- Biometric Authentication
- Teacher Management
- Classroom Management
- Recurring Class System
- Responsive window

## System Requirements

### Software

- Operating System: Linux (tested on Arch Linux)
- Python: Version 3.13 or higher
- GTK4: For graphical interface
- System libraries: dlib, cmake, libopenblas

## Installation

### 1. Install System Dependencies

#### Arch Linux / Manjaro

```bash
sudo pacman -S python python-pip python-virtualenv cmake base-devel openblas gtk4
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv cmake build-essential libopenblas-dev libgtk-4-dev
```

#### Fedora

```bash
sudo dnf install python3 python3-pip cmake gcc gcc-c++ openblas-devel gtk4-devel
```

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** Installing `dlib` may take several minutes as it compiles native code.

### 5. Directory Structure

The system will automatically create the necessary directories on first run:

```
data/
├── classroom.db      # Main database
├── users.db          # User database (if applicable)
└── faces/            # Teacher facial photos
```

## Configuration

### Initial Setup

On first run, the system:

1. Automatically creates the SQLite database
2. Initializes necessary tables (teachers, rooms, classes, access_logs)
3. Creates the `data/faces/` directory for photo storage

### Camera Configuration

By default, the system uses the system's default camera (index 0). To change:

```python
# In src/controllers/room_controller.py
self.cap = cv2.VideoCapture(0)  # Change index if needed
```

To list available cameras:

```bash
v4l2-ctl --list-devices  # Linux
```

### Performance Configuration

Adjust camera FPS in `src/views/main_window.py`:

```python
GLib.timeout_add(66, self.update_frame)  # 66ms = ~15 FPS
# For 30 FPS: GLib.timeout_add(33, self.update_frame)
```

## How to Use

### Run the System

```bash
source venv/bin/activate
python main.py
```

### First Access

1. **Register Teachers**
   - Click "Cadastrar Professor"
   - Fill in name, email and phone (optional)
   - Position face in front of camera
   - Click "Capturar Foto"
   - Save registration

2. **Register Rooms**
   - Click "Cadastrar Sala"
   - Enter room name/number
   - Add description if needed
   - Save registration

3. **Register Classes**
   - Click "Cadastrar Aula"
   - Select room in dropdown
   - Select responsible teacher
   - Choose day of week (Monday to Saturday)
   - Set start time (HH:MM format)
   - Set end time (HH:MM format)
   - Enter subject (optional)
   - Save registration

### Facial Authentication

1. On main screen, select classroom in dropdown
2. System will display:
   - Real-time camera video
   - List of scheduled classes for that room
3. Position yourself in front of camera
4. Recognition is automatic:
   - **Green:** Successful authentication
   - **Red:** Teacher not recognized or no scheduled class
5. Confirmation message will appear on screen

### Management

1. Click "Gerenciar"
2. Use tabs to navigate:
   - **Professores:** View and delete teachers
   - **Salas:** View and delete rooms
   - **Aulas:** View and delete classes

3. To delete:
   - Check the checkboxes of desired items
   - Click "Excluir Selecionados"
   - Confirm operation

### Common Operations

**Edit records:** Currently there is no edit function. Delete and re-register if necessary.

**Database backup:**
```bash
cp data/classroom.db data/classroom.db.backup
```

**Clear data:**
```bash
rm -rf data/*.db data/faces/*.jpg
```

## Technologies Used

### Frontend

- **GTK4 (PyGObject)** - Framework for native graphical interface
  - [Official Documentation](https://docs.gtk.org/gtk4/)
  - [PyGObject Docs](https://pygobject.readthedocs.io/)

### Backend

- **Python 3.13+** - Main programming language
  - [Download Python](https://www.python.org/downloads/)

### Computer Vision

- **face_recognition** - Facial recognition library
  - [GitHub Repository](https://github.com/ageitgey/face_recognition)
  - Based on dlib and offers simplified API

- **dlib** - C++ library for machine learning
  - [Official Site](http://dlib.net/)
  - Provides face detection and recognition algorithms

- **OpenCV (cv2)** - Library for image and video processing
  - [Documentation](https://docs.opencv.org/)
  - Used for camera video capture

### Database

- **SQLite3** - Embedded relational database
  - [Documentation](https://www.sqlite.org/docs.html)
  - No separate server needed

### Other Libraries

- **Pillow (PIL)** - Python image processing
- **NumPy** - Numerical operations and arrays

## Architecture

### MVC Pattern (Model-View-Controller)

```
┌─────────────┐
│    Views    │  Graphical interface (GTK4)
│  (GTK4 UI)  │  - main_window.py
└──────┬──────┘  - register_*.py
       │         - manage_window.py
       │
       ▼
┌─────────────┐
│ Controllers │  Business logic
│  (Business) │  - teacher_controller.py
└──────┬──────┘  - room_controller.py
       │
       │
       ▼
┌─────────────┐
│   Models    │  Data access
│  (Database) │  - database.py
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SQLite    │  Persistence
│  (Storage)  │  - classroom.db
└─────────────┘
```

### Data Flow

1. **View** captures user input (clicks, selections)
2. **View** calls **Controller** methods
3. **Controller** executes validations and business logic
4. **Controller** calls **Model** (database) methods
5. **Model** executes SQL queries and returns data
6. **Controller** processes data and returns to **View**
7. **View** updates interface with received data

### Camera not working

**Problem:** "Cannot open camera" error or black screen

**Solutions:**
```bash
# Check if camera is available
ls /dev/video*

# Test camera with OpenCV
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'ERROR')"

# Check permissions
sudo usermod -a -G video $USER  # Add user to video group
# Logout and login again
```

### Error installing dlib

**Problem:** dlib compilation failure

**Solutions:**
```bash
# Install compilation dependencies
sudo apt install cmake build-essential  # Ubuntu/Debian
sudo pacman -S cmake base-devel         # Arch Linux

# Install with conda (alternative)
conda install -c conda-forge dlib
```

### Inaccurate facial recognition

**Problem:** System does not recognize teacher or recognizes wrong person

**Solutions:**
- Improve environment lighting
- Re-register facial photo with better quality
- Make sure face is visible and frontal
- Clean camera lens
- Adjust recognition tolerance (default 0.6):

```python
# In room_controller.py
matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
# Lower value = more strict
```

### Corrupted database

**Problem:** Error opening or saving data

**Solutions:**
```bash
# Check integrity
sqlite3 data/classroom.db "PRAGMA integrity_check;"

# Restore backup
cp data/classroom.db.backup data/classroom.db

# Recreate database (WARNING: loses all data)
rm data/classroom.db
python main.py  # Recreates automatically
```

### Slow performance

**Problem:** Interface freezing or video lagging

**Solutions:**
- Reduce camera FPS (default 15 FPS)
- Close other heavy programs
- Check CPU usage:
```bash
top
# Press 'q' to exit
```

### GTK4 dependencies error

**Problem:** `gi.repository.Gtk` not found

**Solutions:**
```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0

# Arch Linux
sudo pacman -S python-gobject gtk4

# Fedora
sudo dnf install python3-gobject gtk4
```

---

**Version:** 0.5-beta
**Last update:** October 2025
**Built with:** Python, GTK4, OpenCV and face_recognition

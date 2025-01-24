# ink_area
Python program for area calculations based on images
# Ink Area Analysis Tool

## Overview

The **ink_area_tool** is a Python-based program designed to analyze ink-stained areas on images. The tool allows users to select, crop, and annotate specific regions of interest, measure dimensions, calculate areas, and generate detailed reports. It is interactive and user-friendly based on `OpenCV` for image processing tasks.

---

## Features

1. **User-Friendly Interface**:

2. **Image Operations**:

3. **Measurement and Analysis**:
   - Select a rectangle around the region of interest.
   - Define real-world dimensions for scaling (mm per pixel).
   - Measure and calculate areas in both pixels and square millimeters.

4. **Annotations**:
   - Annotate images with calculated dimensions and area.
   - Visualize and save results with overlaid annotations.

5. **Data Export**:
   - Save original, cropped, and processed images in organized folders.
   - Generate a CSV file (`ink_area.csv`) containing detailed data:
     - Name
     - Length
     - Width
     - Total Area
     - Mask Area (in both pixels and mm²)
     - Pixel-to-mm scale
---

## Installation

### Prerequisites

Ensure the following are installed on your system:

- Python 3.8+
- Required Python libraries:
  - `easygui`
  - `opencv-python`
  - `numpy`


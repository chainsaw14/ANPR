# Automatic Number Plate Recognition (ANPR) System

This repository contains the code for an Automatic Number Plate Recognition (ANPR) system.

## Getting Started

To get started with using this ANPR system, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/chainsaw14/ANPR.git
```
1. Traverse to directory:

```bash
cd ANPR
```

3. Install the required dependencies by running:
```bash
pip install -r requirements.txt
```
4. Run the ANPR system by executing the main.py file and providing the path to the video file you want to analyze:
```bash
python main.py --video_path /path/to/your/video/file.mp4
```

##Structure
The repository has the following structure:

data/: Directory for storing data related to the ANPR system.

model/: Directory for storing machine learning models.

sample/: Directory for storing sample data or results

sort/: Directory for SORT (Simple Online and Realtime Tracking) algorithm implementation.

database.py: Python file for handling database operations.

main.py: Main Python file for running the ANPR system.

requirements.txt: Text file listing all the required dependencies.

util.py: Utility functions for the ANPR system.

yolov8n.pt: YOLOv8 model weights file.

This README provides a basic guide to getting started with the ANPR system, outlines the directory structure, encourages contributions, and mentions the project's license. Let me know if you need further details or modifications!

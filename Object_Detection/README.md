## Introduction
This branch is for an A.I project focusing on object detection using Yolov8m model. The script is designed to detect objects appearing in videos such as vehicles and person, record the appearance and disappearance time of the objects and write to a json file.

## Some Example
### Before
<p align="center">
    <img src="https://github.com/vlu-lantran/AI_project/blob/Object_Detection_Group2/GIF_Example/Example1_Before.gif?raw=true" width=350>
    <img src="https://github.com/vlu-lantran/AI_project/blob/Object_Detection_Group2/GIF_Example/Example2_Before.gif?raw=true" width=350>
</p>

### After
<p align="center">
    <img src="https://github.com/vlu-lantran/AI_project/blob/Object_Detection_Group2/GIF_Example/Example1_After.gif?raw=true" width=350>
    <img src="https://github.com/vlu-lantran/AI_project/blob/Object_Detection_Group2/GIF_Example/Example2_After.gif?raw=true" width=350>
</p>


## Installation
1. Download the source code from this branch in the repository.
2. If you want to change the Yolov8m model to another model, change at the line:

```python
model_path = 'YOUR MODEL'
#Example: model_path = 'yolov8m.pt'    
```
3. If you want to run the code with your input, change at line:

```python
video_path = 'YOUR_INPUT_VIDEO.mp4'
#video_path = 'video_test.mp4'   
```

## Features 
- Analyze vehicle and person objects appearing in the input video and number them in order. 
- Record the appearance and disappearance time of objects in json file.

## Libraries Used
1. **os**: Prevents potential errors related to loading libraries on some systems.
2. **cv2**: For image processing and computer vision.
3. **json**: For encoding and decoding JSON data.
4. **ultralytics.YOLO**: Used to deploy the YOLO object detection model.
5. **collections.defaultdict**: Class to create default dictionaries where a default value is provided if the key does not exist.

## Warning
1. The output of this code marks the objects that appear in English (Car 1, Person 1) and outputs the result in a Json file in Vietnamese at line

```python
ten_lop = {
            'person': 'Người',
            'car': 'Ô tô',
            'truck': 'Xe tải',
            'bus': 'Xe buýt',
            'motorcycle': 'Xe máy'
            }.get(info['Tên lớp'], info['Tên lớp']) 
```

You can keep it as is or change it as needed.

2. This code uses CPU, if your hardware is not guaranteed, please consider before using this code.

## Authors
- **Nguyen Phuoc Dai**
- **Nguyen Quoc Nhat**
- **Lai Ngoc Mai**

## License
Thank you for your interest and use of our project!
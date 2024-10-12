import os
import cv2
from ultralytics import YOLO
import json
from collections import defaultdict


def process_video(video_path, model_path, output_video_path, output_json_path):
    #Thêm hàm để đảm bảo sẽ chạy ổn trên cac nền tảng khác
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'true'

    #Định nghĩa model và capture
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    # Lấy các thuộc tính của video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Tạo đối tượng VideoWriter để lưu kết quả đầu ra
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Từ điển lưu trữ thông tin theo dõi đối tượng
    objects = defaultdict(lambda: {'count': 0, 'tracks': {}})

    frame_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Chạy yolov8 cho từng Frame
        results = model.track(frame, persist=True)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)
            confidences = results[0].boxes.conf.cpu().numpy()

            #Cho xét các đối tượng theo yêu cầu: Các loại xe và người
            for box, track_id, cls, confidence in zip(boxes, track_ids, classes, confidences):
                class_name = model.names[cls]
                #Nếu không phải người/xe thì bỏ qua
                if class_name not in ['person', 'car', 'truck', 'bus', 'motorcycle']:
                    continue

                # Mở tùy nhu cầu :D
                # if class_name in ['truck', 'bus', 'motorcycle']:
                #     class_name = 'car'

                #Xử lý đối tượng mới
                if track_id not in objects[class_name]['tracks']:
                    objects[class_name]['count'] += 1
                    count = objects[class_name]['count']
                    objects[class_name]['tracks'][track_id] = {
                        'ID vật thể': f"{class_name.capitalize()} {count}",
                        'Tên lớp': class_name,
                        'Thời điểm xuất hiện': frame_count / fps,
                        'Thời điểm biến mất': frame_count / fps,
                        'bounding_box': box.tolist(),
                        'Độ chính xác': float(confidence)
                    }
                #Cập nhật đối tượng hiện có
                else:
                    objects[class_name]['tracks'][track_id]['Thời điểm biến mất'] = frame_count / fps
                    objects[class_name]['tracks'][track_id]['bounding_box'] = box.tolist()
                    objects[class_name]['tracks'][track_id]['Độ chính xác'] = float(confidence)

                # Vẽ khung xung quanh vật thể
                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                label = objects[class_name]['tracks'][track_id]['ID vật thể']
                cv2.putText(frame, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0),
                            2)

        # xuất frame cho video đầu ra
        out.write(frame)

        # Cập nhật tiến trình để dễ theo dõi
        frame_count += 1
        progress = (frame_count / total_frames) * 100
        print(f"\rProcessing: {progress:.2f}% complete", end="")

    # Giải phóng tài nguyên các đối tượng ghi và quay video
    cap.release()
    out.release()

    print(f"\nProcessed video saved to {output_video_path}")

    # Chuyển đổi kết quả theo dõi sang định dạng mong muốn
    json_results = []
    for class_name, data in objects.items():
        for track_id, info in data['tracks'].items():
            # Chuyển đổi tên lớp sang tiếng Việt
            ten_lop = {
                'person': 'Người',
                'car': 'Ô tô',
                'truck': 'Xe tải',
                'bus': 'Xe buýt',
                'motorcycle': 'Xe máy'
            }.get(info['Tên lớp'], info['Tên lớp'])

            # Chuyển đổi thời gian sang định dạng "mm:ss"
            thoi_diem_xuat_hien = f"{int(info['Thời điểm xuất hiện'] // 60):02d}:{int(info['Thời điểm xuất hiện'] % 60):02d}"
            thoi_diem_bien_mat = f"{int(info['Thời điểm biến mất'] // 60):02d}:{int(info['Thời điểm biến mất'] % 60):02d}"

            json_results.append({
                "ID vật thể": info['ID vật thể'].replace(class_name.capitalize(), ten_lop),
                "Tên lớp": ten_lop,
                "Thời điểm xuất hiện": thoi_diem_xuat_hien,
                "Thời điểm biến mất": thoi_diem_bien_mat,
                "bounding_box": info['bounding_box'],
                "Độ chính xác": f"{info['Độ chính xác'] * 100:.2f}%"
            })

    # Viết kết quả dưới dạng file Json
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, ensure_ascii=False, indent=4)

    print(f"Tracking results saved to {output_json_path}")


# Hàm Main
if __name__ == "__main__":
    video_path = 'video_test.mp4'
    model_path = 'yolov8m.pt'
    output_video_path = 'output_video.mp4'
    output_json_path = 'tracking_results.json'

    process_video(video_path, model_path, output_video_path, output_json_path)
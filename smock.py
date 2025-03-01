#coding:utf-8
import cv2
import pygame
import os
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import time

# 加载模型
model_path = './best.pt'
#model_path = 'D:\\BaiduNetdiskDownload\\Yolov7-CCPD.pt'
model = YOLO(model_path)  # 加载自定义模型权

# 初始化Pygame
pygame.init()

class FireDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("吸烟识别系统V2.0 by Miss小远")
        self.root.geometry("1200x800")  # 设置窗口大小

        # 设置标题
        self.title_label = tk.Label(root, text="吸烟识别系统V2.0 by Miss小远", font=("Helvetica", 16))
        self.title_label.pack(side=tk.TOP, pady=10)

        # 设置布局
        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(side=tk.TOP, fill=tk.X)

        self.frame_video = tk.Frame(root)
        self.frame_video.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_results = tk.Frame(root)
        self.frame_results.pack(side=tk.RIGHT, fill=tk.Y)

        # 添加按钮
        self.start_cam_btn = tk.Button(self.frame_buttons, text="开启摄像头", command=self.start_camera)
        self.start_cam_btn.pack(side=tk.LEFT)

        self.stop_cam_btn = tk.Button(self.frame_buttons, text="关闭摄像�??", command=self.stop_camera)
        self.stop_cam_btn.pack(side=tk.LEFT)

        self.upload_image_btn = tk.Button(self.frame_buttons, text="上传图片", command=self.upload_image)
        self.upload_image_btn.pack(side=tk.LEFT)

        self.upload_video_btn = tk.Button(self.frame_buttons, text="上传视频", command=self.upload_video)
        self.upload_video_btn.pack(side=tk.LEFT)

        # 添加摄像头选择下拉菜单
        self.camera_var = tk.StringVar(value="选择摄像�??")
        self.camera_menu = tk.OptionMenu(self.frame_buttons, self.camera_var, "选择摄像�??")
        self.camera_menu.pack(side=tk.LEFT)

        # 设置表格
        columns = ("file", "coordinates", "confidence")
        self.treeview = ttk.Treeview(self.frame_results, columns=columns, show='headings')
        self.treeview.heading("file", text="视频\\图片信息")
        self.treeview.heading("coordinates", text="识别坐标位置")
        self.treeview.heading("confidence", text="可信�??")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.screen = None
        self.running = False

        # 初始化摄像头列表
        self.camera_list = self.get_camera_list()
        if self.camera_list:
            self.camera_var.set(self.camera_list[0])
            self.camera_menu['menu'].delete(0, 'end')
            for camera in self.camera_list:
                self.camera_menu['menu'].add_command(label=camera, command=tk._setit(self.camera_var, camera))

    def get_camera_list(self):
        """获取可用摄像头列�??"""
        camera_list = []
        for i in range(4):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(f"Camera {i}")
                cap.release()
        return camera_list

    def start_camera(self):
        """启动摄像头并开始处理视频流"""
        if self.running:
            self.running = False
            self.cap.release()

        camera_index = int(self.camera_var.get().split()[1])
        self.cap = cv2.VideoCapture(camera_index)  # 选择的摄像头
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot open camera")
            return
        self.running = True
        self.process_camera()

    def stop_camera(self):
        """停止摄像�??"""
        self.running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.screen.fill((0, 0, 0))  # 清空Pygame屏幕
        pygame.display.flip()

    def process_camera(self):
        """处理摄像头视频流"""
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                self.process_frame(frame)
                self.root.after(10, self.process_camera)  # �??10毫秒处理一�??
            else:
                messagebox.showerror("Error", "Cannot read frame")
                self.running = False

    def upload_image(self):
        #上传并处理图�??
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            frame = cv2.imread(file_path)
            frame = self.resize_image(frame, self.frame_video.winfo_width(), self.frame_video.winfo_height())
            self.process_frame(frame, file_path)

    def upload_video(self):
        #上传并处理视�??
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if file_path:
            cap = cv2.VideoCapture(file_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                self.process_frame(frame, file_path)
            cap.release()

    def resize_image(self, frame, max_width, max_height):
        #调整图像大小以适应指定的最大宽度和高度
        h, w = frame.shape[:2]
        scale = min(max_width / w, max_height / h)
        return cv2.resize(frame, (int(w * scale), int(h * scale)))

    def process_frame(self, frame, file_path=None):
        #处理视频帧并进行目标检�??
        results = model(frame)
        smoking_conf = 0
        for result in results:
            for box in result.boxes:
                coords = box.xyxy.tolist()
                if len(coords) == 1 and len(coords[0]) == 4:
                    x1, y1, x2, y2 = coords[0]
                    conf = box.conf.item()
                    cls = box.cls.item()
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # 检查检测到的类别是smocking并更新置信度
                    if model.names[int(cls)] == "smoking":
                        smoking_conf = max(smoking_conf, conf)
                        self.treeview.insert("", 0, values=(file_path or "Camera", f"({x1}, {y1}), ({x2}, {y2})", f"{conf:.2f}"))
                        if smoking_conf >= 0.7 and not pygame.mixer.music.get_busy():
                            self.play_alert_sound()
        

        # 将帧从BGR转换为RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 将帧转换为Pygame图像
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # 如果尚未创建Pygame窗口，则创建窗口
        if self.screen is None:
            os.environ['SDL_WINDOWID'] = str(self.frame_video.winfo_id())
            os.environ['SDL_VIDEODRIVER'] = 'windib'
            self.screen = pygame.display.set_mode((self.frame_video.winfo_width(), self.frame_video.winfo_height()))

        # 显示�??
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()

    def play_alert_sound(self):
        """播放警报声音"""
        alert_sound_path = 'smock.mp3'
        if os.path.exists(alert_sound_path):
            pygame.mixer.music.load(alert_sound_path)
            pygame.mixer.music.play()

    def on_close(self):
        """关闭窗口时执行的操作"""
        self.running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        pygame.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FireDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

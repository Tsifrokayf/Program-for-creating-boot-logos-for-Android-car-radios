import os
import shutil
import zipfile
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
    from PIL import Image, ImageSequence, ImageTk
except ImportError:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", "Библиотеки Pillow или customtkinter не установлены.\nПожалуйста, запустите run.bat для их установки.")
    exit()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BootAnimApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Android Boot Animation Creator")
        self.geometry("720x750")
        self.resizable(False, False)
        
        # Переменные
        self.gif_path = ctk.StringVar()
        self.width_var = ctk.StringVar(value="1024")
        self.height_var = ctk.StringVar(value="600")
        self.fps_var = ctk.StringVar(value="30")
        self.mode_var = ctk.StringVar(value="contain (вписать)")
        self.loop_var = ctk.StringVar(value="cyclic") 
        self.color_depth_var = ctk.StringVar(value="RGB (24-bit)") # Важно для некоторых ГУ
        
        # Для предпросмотра
        self.preview_frames = []
        self.preview_idx = 0
        self.is_animating = False
        
        self.create_widgets()
        
    def create_widgets(self):
        header = ctk.CTkLabel(self, text="Boot Animation Creator Pro", font=ctk.CTkFont(size=24, weight="bold"))
        header.pack(pady=(15, 10))

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        left_col = ctk.CTkFrame(main_frame, corner_radius=15)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_col = ctk.CTkFrame(main_frame, corner_radius=15, width=260)
        right_col.pack(side="right", fill="both", padx=(10, 0))
        right_col.pack_propagate(False)

        # --- ЛЕВАЯ КОЛОНКА ---
        
        ctk.CTkLabel(left_col, text="1. Выберите GIF файл", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        file_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        file_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.gif_entry = ctk.CTkEntry(file_frame, textvariable=self.gif_path, state="disabled")
        self.gif_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_browse = ctk.CTkButton(file_frame, text="Обзор...", width=80, command=self.browse_gif)
        self.btn_browse.pack(side="right")
        
        ctk.CTkLabel(left_col, text="2. Разрешение экрана", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(5, 5))
        res_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        res_frame.pack(fill="x", padx=20, pady=(0, 5))
        
        ctk.CTkLabel(res_frame, text="Ширина:").pack(side="left", padx=(0, 5))
        self.entry_w = ctk.CTkEntry(res_frame, textvariable=self.width_var, width=60)
        self.entry_w.pack(side="left", padx=(0, 15))
        self.entry_w.bind("<KeyRelease>", self.update_preview_from_settings)
        
        ctk.CTkLabel(res_frame, text="Высота:").pack(side="left", padx=(0, 5))
        self.entry_h = ctk.CTkEntry(res_frame, textvariable=self.height_var, width=60)
        self.entry_h.pack(side="left")
        self.entry_h.bind("<KeyRelease>", self.update_preview_from_settings)
        
        preset_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        preset_frame.pack(fill="x", padx=20, pady=(0, 15))
        for res in [("1024", "600"), ("1280", "720"), ("800", "480")]:
            btn = ctk.CTkButton(preset_frame, text=f"{res[0]}x{res[1]}", width=60, height=24, 
                                command=lambda w=res[0], h=res[1]: self.set_res(w, h))
            btn.pack(side="left", padx=3)

        ctk.CTkLabel(left_col, text="3. Тонкая настройка", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(5, 5))
        
        set_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        set_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(set_frame, text="FPS:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_fps = ctk.CTkEntry(set_frame, textvariable=self.fps_var, width=60)
        self.entry_fps.grid(row=0, column=1, sticky="w", padx=(10, 20), pady=5)
        self.entry_fps.bind("<KeyRelease>", self.update_preview_from_settings)
        
        ctk.CTkLabel(set_frame, text="Масштаб:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_scale = ctk.CTkOptionMenu(set_frame, variable=self.mode_var, width=150,
                                         values=["contain (вписать)", "cover (заполнить)", "stretch (растянуть)"],
                                         command=self.update_preview_from_settings)
        self.combo_scale.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=5)
        
        ctk.CTkLabel(set_frame, text="Цвет:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_color = ctk.CTkOptionMenu(set_frame, variable=self.color_depth_var, width=150,
                                         values=["RGB (24-bit)", "RGBA (32-bit)"])
        self.combo_color.grid(row=2, column=1, sticky="w", padx=(10, 20), pady=5)

        ctk.CTkLabel(set_frame, text="Цикл:").grid(row=3, column=0, sticky="w", pady=5)
        radio_frame = ctk.CTkFrame(set_frame, fg_color="transparent")
        radio_frame.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.radio_cyclic = ctk.CTkRadioButton(radio_frame, text="Бесконечно", variable=self.loop_var, value="cyclic")
        self.radio_cyclic.pack(side="left", padx=(0, 10))
        self.radio_once = ctk.CTkRadioButton(radio_frame, text="1 раз", variable=self.loop_var, value="once")
        self.radio_once.pack(side="left")

        ctk.CTkLabel(left_col, text="4. Имя файла", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(5, 5))
        save_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        save_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.out_name_var = ctk.StringVar(value="bootanimation")
        ctk.CTkEntry(save_frame, textvariable=self.out_name_var, width=160).pack(side="left")
        ctk.CTkLabel(save_frame, text=".zip", text_color="gray").pack(side="left", padx=(5, 0))

        # --- ПРАВАЯ КОЛОНКА ---
        ctk.CTkLabel(right_col, text="Предпросмотр GIF", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        self.preview_canvas = ctk.CTkLabel(right_col, text="Нет изображения", fg_color="gray20", width=200, height=200, corner_radius=10)
        self.preview_canvas.pack(pady=10, padx=25)
        
        self.info_lbl = ctk.CTkLabel(right_col, text="Оригинал: - \nКадров: -", text_color="gray", justify="center")
        self.info_lbl.pack(pady=5)

        author_lbl = ctk.CTkLabel(right_col, text="Created by Tsifrokayf ", font=ctk.CTkFont(size=11, slant="italic"), text_color="gray40")
        author_lbl.pack(pady=(15, 0))

        # --- НИЖНЯЯ ЧАСТЬ ---
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.status_label = ctk.CTkLabel(bottom_frame, text="Ожидание...", text_color="gray")
        self.status_label.pack(pady=(0, 5))

        self.progress = ctk.CTkProgressBar(bottom_frame, mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=(0, 15))
        self.progress.set(0)

        self.btn_generate = ctk.CTkButton(bottom_frame, text="СОЗДАТЬ BOOTANIMATION.ZIP", height=45, 
                                          font=ctk.CTkFont(size=14, weight="bold"), command=self.start_generation)
        self.btn_generate.pack(fill="x", padx=20)

    def set_res(self, w, h):
        self.width_var.set(w)
        self.height_var.set(h)
        self.update_preview_from_settings()

    def browse_gif(self):
        path = filedialog.askopenfilename(filetypes=[("GIF Files", "*.gif")])
        if path:
            self.gif_path.set(path)
            self.gif_entry.configure(state="normal")
            self.gif_entry.delete(0, 'end')
            self.gif_entry.insert(0, path)
            self.gif_entry.configure(state="disabled")
            self.update_preview_from_settings()

    def update_preview_from_settings(self, *args):
        path = self.gif_path.get()
        if not path or not os.path.exists(path):
            return
        try:
            target_w = int(self.width_var.get())
            target_h = int(self.height_var.get())
        except ValueError:
            return
        raw_mode = self.mode_var.get()
        mode = "contain"
        if "cover" in raw_mode: mode = "cover"
        elif "stretch" in raw_mode: mode = "stretch"
        self.load_preview(path, target_w, target_h, mode)

    def load_preview(self, path, target_w, target_h, mode):
        try:
            self.is_animating = False
            if hasattr(self, 'anim_job'):
                self.after_cancel(self.anim_job)
            self.preview_frames.clear()
            
            gif = Image.open(path)
            frames_count = getattr(gif, "n_frames", 1)
            orig_w, orig_h = gif.size
            max_preview = min(frames_count, 30)
            preview_box_size = 200
            scale_factor = min(preview_box_size / target_w, preview_box_size / target_h)
            display_w = int(target_w * scale_factor)
            display_h = int(target_h * scale_factor)
            
            for i, frame in enumerate(ImageSequence.Iterator(gif)):
                if i >= max_preview: break
                frame = frame.convert("RGBA")
                simulated_screen = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 255))
                if mode == "stretch":
                    resized = frame.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    simulated_screen.paste(resized, (0, 0))
                elif mode == "contain":
                    frame_copy = frame.copy()
                    frame_copy.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
                    x = (target_w - frame_copy.width) // 2
                    y = (target_h - frame_copy.height) // 2
                    simulated_screen.paste(frame_copy, (x, y))
                elif mode == "cover":
                    ratio = max(target_w/frame.width, target_h/frame.height)
                    new_w = int(frame.width * ratio)
                    new_h = int(frame.height * ratio)
                    resized = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    x = (target_w - new_w) // 2
                    y = (target_h - new_h) // 2
                    simulated_screen.paste(resized, (x, y))
                display_img = simulated_screen.resize((display_w, display_h), Image.Resampling.LANCZOS)
                bg = Image.new("RGBA", (200, 200), (40, 40, 40, 255))
                bx = (200 - display_w) // 2
                by = (200 - display_h) // 2
                bg.paste(display_img, (bx, by))
                photo = ctk.CTkImage(light_image=bg, dark_image=bg, size=(200, 200))
                self.preview_frames.append(photo)
            
            try:
                fps_val = int(self.fps_var.get())
                if fps_val <= 0: fps_val = 1
            except ValueError:
                fps_val = 30
            duration = frames_count / fps_val
            self.info_lbl.configure(text=f"Оригинал: {orig_w}x{orig_h}\nИтог: {target_w}x{target_h}\nКадров: ~{frames_count} | Скорость: {fps_val} FPS\nДлительность: {duration:.1f} сек")
            
            if self.preview_frames:
                self.is_animating = True
                self.preview_idx = 0
                self.animate_preview()
        except Exception as e:
            self.preview_canvas.configure(text="Ошибка загрузки\nпревью", image="")

    def animate_preview(self):
        if not self.is_animating or not self.preview_frames:
            return
        frame = self.preview_frames[self.preview_idx]
        self.preview_canvas.configure(image=frame, text="")
        self.preview_idx = (self.preview_idx + 1) % len(self.preview_frames)
        try:
            fps_val = int(self.fps_var.get())
            if fps_val <= 0: fps_val = 1
            if fps_val > 120: fps_val = 120
        except ValueError:
            fps_val = 30
        delay = 1000 // fps_val
        self.anim_job = self.after(delay, self.animate_preview)

    def toggle_ui(self, state_str):
        self.btn_browse.configure(state=state_str)
        self.entry_w.configure(state=state_str)
        self.entry_h.configure(state=state_str)
        self.entry_fps.configure(state=state_str)
        self.combo_scale.configure(state=state_str)
        self.combo_color.configure(state=state_str)
        self.radio_cyclic.configure(state=state_str)
        self.radio_once.configure(state=state_str)

    def start_generation(self):
        gif_file = self.gif_path.get()
        if not gif_file or not os.path.exists(gif_file):
            messagebox.showerror("Ошибка", "Пожалуйста, выберите существующий GIF файл.")
            return
        try:
            w = int(self.width_var.get())
            h = int(self.height_var.get())
            fps = int(self.fps_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Ширина, Высота и FPS должны быть числами.")
            return
        default_name = self.out_name_var.get().strip()
        if not default_name:
            default_name = "bootanimation"
        if not default_name.endswith(".zip"):
            default_name += ".zip"
        out_zip = filedialog.asksaveasfilename(defaultextension=".zip", initialfile=default_name, filetypes=[("ZIP Files", "*.zip")])
        if not out_zip:
            return
        self.is_animating = False
        if hasattr(self, 'anim_job'):
            self.after_cancel(self.anim_job)
        self.toggle_ui("disabled")
        self.btn_generate.configure(text="Обработка...", state="disabled")
        self.progress.set(0)
        raw_mode = self.mode_var.get()
        mode = "contain"
        if "cover" in raw_mode: mode = "cover"
        elif "stretch" in raw_mode: mode = "stretch"
        color_depth = "RGB" if "RGB" in self.color_depth_var.get() else "RGBA"
        loop = self.loop_var.get()
        threading.Thread(target=self.process, args=(gif_file, out_zip, w, h, fps, mode, loop, color_depth), daemon=True).start()

    def process(self, gif_path, out_zip, target_w, target_h, fps, mode, loop, color_depth):
        temp_dir = tempfile.mkdtemp()
        part_dir = os.path.join(temp_dir, "part0")
        os.makedirs(part_dir)
        try:
            self.update_status("Чтение GIF...")
            gif = Image.open(gif_path)
            frame_count = getattr(gif, "n_frames", 0)
            if frame_count == 0:
                frame_count = len(list(ImageSequence.Iterator(gif)))
                gif.seek(0)
            frame_idx = 0
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                bg = Image.new(color_depth, (target_w, target_h), (0, 0, 0))
                if mode == "stretch":
                    resized = frame.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    if color_depth == "RGB": resized = resized.convert("RGB")
                    bg.paste(resized, (0, 0))
                elif mode == "contain":
                    frame.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
                    x = (target_w - frame.width) // 2
                    y = (target_h - frame.height) // 2
                    if color_depth == "RGB": frame = frame.convert("RGB")
                    bg.paste(frame, (x, y))
                elif mode == "cover":
                    ratio = max(target_w/frame.width, target_h/frame.height)
                    new_w = int(frame.width * ratio)
                    new_h = int(frame.height * ratio)
                    resized = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    x = (target_w - new_w) // 2
                    y = (target_h - new_h) // 2
                    if color_depth == "RGB": resized = resized.convert("RGB")
                    bg.paste(resized, (x, y))
                frame_name = f"{frame_idx:05d}.png"
                frame_path = os.path.join(part_dir, frame_name)
                bg.save(frame_path, "PNG", compress_level=1)
                frame_idx += 1
                if frame_count > 0:
                    prog = (frame_idx / frame_count) * 0.8
                    self.after(0, self.update_progress, prog, f"Кадр {frame_idx} из {frame_count} ({color_depth})")
            self.after(0, self.update_status, "Создание desc.txt...")
            desc_path = os.path.join(temp_dir, "desc.txt")
            with open(desc_path, "w", newline='\n') as f:
                f.write(f"{target_w} {target_h} {fps}\n")
                if loop == "cyclic":
                    f.write("p 0 0 part0\n")
                else:
                    f.write("p 1 0 part0\n")
            self.after(0, self.update_status, "Упаковка в bootanimation.zip (STORED)...")
            files_to_zip = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    files_to_zip.append(os.path.join(root, file))
            total_files = len(files_to_zip)
            with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_STORED) as zipf:
                for idx, file_path in enumerate(files_to_zip):
                    arcname = os.path.relpath(file_path, temp_dir)
                    arcname = arcname.replace('\\', '/')
                    zipf.write(file_path, arcname)
                    prog = 0.8 + ((idx + 1) / total_files) * 0.2
                    self.after(0, self.update_progress, prog, f"Архивация... {idx+1}/{total_files}")
            self.after(0, self.finish, True, "Готово!")
        except Exception as e:
            self.after(0, self.finish, False, str(e))
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def update_progress(self, val, text=None):
        self.progress.set(val)
        if text:
            self.status_label.configure(text=text)

    def update_status(self, text):
        self.status_label.configure(text=text)

    def finish(self, success, msg):
        self.progress.set(1.0 if success else 0)
        self.toggle_ui("normal")
        self.btn_generate.configure(text="СОЗДАТЬ BOOTANIMATION.ZIP", state="normal")
        self.status_label.configure(text=msg if success else "Ошибка!")
        if getattr(self, "preview_frames", None) and getattr(self, "btn_generate", None):
             self.is_animating = True
             self.animate_preview()
        if success:
            messagebox.showinfo("Идеально", "bootanimation.zip успешно создан!\nТеперь можно переносить на магнитолу.")
        else:
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{msg}")

if __name__ == "__main__":
    app = BootAnimApp()
    app.mainloop()

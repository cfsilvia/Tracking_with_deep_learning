import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from tkinter import messagebox
import yaml

class Gui_auxiliary_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select a File")
        self.geometry("500x200")
        self.resizable(False, False)
        
        tk.Label(self, text = "Choose the movie for tracking",  font=("Segoe UI", 12, "bold")).pack(pady = 10)
        frame = tk.Frame(self)
        frame.pack(pady=5)
        
        self.text_box = tk.Text(frame, height=2, width=50)
        self.text_box.pack(side = "right", padx=5)
        
        tk.Button(frame, text="Browse", command=self.browse_file,bg="lightblue", fg="black", font=("Segoe UI", 12, "bold")).pack(side = "right", padx=5)
        tk.Button(self, text="Continue", command=self.on_continue, bg="lightgreen", fg="black", font=("Segoe UI", 12, "bold")).pack()
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select the movie for tracking")
        if file_path:
            self.text_box.delete("1.0", tk.END)  # clear old text
            self.text_box.insert(tk.END, file_path)
            
    def on_continue(self):
        file_path = self.text_box.get("1.0", tk.END).strip()
        dir = os.path.dirname(file_path)
        self.selected_file =  os.path.join(dir, "object_detection.yaml") 
        if os.path.exists(self.selected_file):
            print(f"Selected file: {self.selected_file}")
            #open the file path in notepad
            messagebox.showinfo("Info", "Adapt the configuration to your needs.")
            subprocess.run(["notepad.exe", self.selected_file])
            
        else:
            #create yaml file
            Gui_auxiliary_app.create_dict_parameters(self.selected_file, file_path, dir)
            print(f"Selected file: {self.selected_file}")
            #open the file path in notepad
            messagebox.showinfo("Info", "Adapt the configuration to your needs.")
            subprocess.run(["notepad.exe",self.selected_file])
        self.destroy() #closes the window
        
    @staticmethod
    def create_dict_parameters(file, movie_path, dir):
      filename_with_ext = os.path.basename(movie_path)
      filename = os.path.splitext(filename_with_ext)[0]  
      video_output = os.path.join(dir, filename + "_with_landmarks.avi")
      config = {
        "type_experiment" : "Blind moles from the side", #options: Mice , Blind moles from the side , Blind moles from the top
        "file_model" : ["C:/LabSoftware/Tracking_with_deep_learning/models/yoloBMR_left_BMR_combined_videos_07.07.242/weights/best.pt","C:/LabSoftware/Tracking_with_deep_learning/models/yoloBMR_right_BMR_combined_videos_26.06.242/weights/best.pt"],
        "video_path" : movie_path,
        "video_output" : video_output 
    }
     # Save dictionary as YAML file
      with open(file, "w", encoding="utf-8") as f:
         yaml.safe_dump(config, f, sort_keys=False, allow_unicode=True)
    
        
        
def select_file_with_gui():
    app = Gui_auxiliary_app()
    app.mainloop()
    
    return app.selected_file
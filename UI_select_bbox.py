# create a UI to select a bounding box from an image
import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class BoundingBoxSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Bounding Box Selector")
        
        # Initialize variables
        self.image = None
        self.photo = None
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        self.bbox_coordinates = None
        self.video_path = None
        self.current_frame = None
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Create buttons frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Create input type selection
        self.input_type = ttk.Combobox(
            self.button_frame, 
            values=["Image", "Video"],
            state="readonly",
            width=10
        )
        self.input_type.set("Image")
        self.input_type.pack(side=tk.LEFT, padx=5)
        
        # Load button
        self.load_btn = tk.Button(self.button_frame, text="Load File", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Save coordinates button
        self.save_btn = tk.Button(self.button_frame, text="Save Coordinates", command=self.save_coordinates)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
    def load_file(self):
        if self.input_type.get() == "Image":
            self.load_image()
        else:
            self.load_video()

    def load_image(self):
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            # Load and display image
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.current_frame = self.image.copy()
            self.display_image()
            
    def load_video(self):
        # Open file dialog to select video
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        
        if self.video_path:
            # Open video and get first frame
            cap = cv2.VideoCapture(self.video_path)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame = self.image.copy()
                self.display_image()
            else:
                print("Error: Could not read video file")
            
    def display_image(self):
        if self.image is not None:
            # Convert OpenCV image to PIL format
            height, width = self.image.shape[:2]
            pil_image = Image.fromarray(self.image)
            
            # Resize window to fit image
            self.root.geometry(f"{width}x{height}")
            
            # Convert to PhotoImage format for canvas
            self.photo = ImageTk.PhotoImage(image=pil_image)
            
            # Update canvas
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_mouse_move(self, event):
        if self.start_x and self.start_y:
            # Remove previous rectangle if it exists
            if self.current_rect:
                self.canvas.delete(self.current_rect)
            
            # Draw new rectangle
            self.current_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=2
            )
            
    def on_mouse_up(self, event):
        if self.start_x and self.start_y:
            # Store final coordinates
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            self.bbox_coordinates = (x1, y1, x2, y2)
            
    def save_coordinates(self):
        if self.bbox_coordinates:
            # Get coordinates in x1,y1,x2,y2 format
            x1, y1, x2, y2 = self.bbox_coordinates
            
            # Convert to x,y,w,h format
            w = x2 - x1
            h = y2 - y1
            
            # Create default filename based on input type
            default_filename = "bbox_image.txt" if self.input_type.get() == "Image" else "bbox_video.txt"
            
            # Open file dialog to choose save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                initialfile=default_filename,
                title="Save Bounding Box Coordinates"
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    # Save x,y,w,h format
                    f.write(f"{x1},{y1},{w},{h}\n")
                    # Save x1,y1,x2,y2 format on next line
                    if 0:
                        f.write(f"{x1},{y1},{x2},{y2}")
                
                print(f"Saved coordinates to {file_path}")
                print(f"Format 1 (x,y,w,h): {x1},{y1},{w},{h}")
                print(f"Format 2 (x1,y1,x2,y2): {x1},{y1},{x2},{y2}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BoundingBoxSelector(root)
    root.mainloop()
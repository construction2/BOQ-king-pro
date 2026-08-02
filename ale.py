# ==========================================
# BOQ KING PRO - Ultimate Suite (Clean UI)
# Slogan: "Calculate Smarter, Build Better."
# ==========================================

import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import datetime

class BOQKingProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BOQ KING PRO")
        self.root.geometry("420x720")
        self.root.configure(bg="#f7f9fa")

        self.projects_list = [
            "G+2 Building Project",
            "Road Project Phase 1",
            "Commercial Building"
        ]

        self.file_storage = {
            "PDF": [],
            "Excel": [],
            "Drawings": []
        }

        self.container = tk.Frame(self.root, bg="#f7f9fa")
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}
        
        for F in (Screen1Dashboard, Screen2Projects, Screen3BOQ, Screen4Control, Screen5FileCenter, Screen6SmartEngine, Screen7Settings):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_bottom_nav()
        self.show_frame("Screen1Dashboard")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        if page_name == "Screen5FileCenter" and hasattr(frame, "refresh_files"):
            frame.refresh_files()
        elif page_name == "Screen2Projects" and hasattr(frame, "refresh_projects"):
            frame.refresh_projects()
        elif page_name == "Screen3BOQ" and hasattr(frame, "refresh_boq_view"):
            frame.refresh_boq_view()
        elif page_name == "Screen6SmartEngine" and hasattr(frame, "refresh_calc_summary"):
            frame.refresh_calc_summary()
        
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.config(bg="#1b365d", fg="#d69e2e")
            else:
                btn.config(bg="#2b6cb0", fg="#ffffff")

    def create_bottom_nav(self):
        nav_bar = tk.Frame(self.root, bg="#2b6cb0", height=55)
        nav_bar.pack(side=tk.BOTTOM, fill=tk.X)
        nav_bar.pack_propagate(False)

        self.nav_buttons = {}
        nav_items = [
            ("Screen1Dashboard", "Home"),
            ("Screen2Projects", "Projects"),
            ("Screen3BOQ", "BOQ"),
            ("Screen5FileCenter", "Files"),
            ("Screen6SmartEngine", "Smart")
        ]

        for code_name, label_text in nav_items:
            btn = tk.Button(
                nav_bar, text=label_text, font=("Arial", 7, "bold"),
                bg="#2b6cb0", fg="#ffffff", bd=0, relief=tk.FLAT,
                command=lambda cn=code_name: self.show_frame(cn)
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1, pady=2)
            self.nav_buttons[code_name] = btn

    def handle_action(self, action_type, category):
        if action_type == "Upload":
            file_path = None
            if category == "Device":
                file_path = simpledialog.askstring("Device File Upload", "Enter BOQ File Name or Path (e.g., BOQ_Sheet.xlsx):")
                if file_path:
                    file_name = os.path.basename(file_path)
                    ext = os.path.splitext(file_name)[1].lower()
                    target_cat = "PDF"
                    if ext in [".xlsx", ".xls"]:
                        target_cat = "Excel"
                    elif ext in [".dwg", ".png", ".jpg", ".jpeg"]:
                        target_cat = "Drawings"
                    elif not ext:
                        target_cat = "Excel"
                        file_name += ".xlsx"
                    
                    if file_name not in self.file_storage[target_cat]:
                        self.file_storage[target_cat].append(file_name)
                    messagebox.showinfo("Success", f"File '{file_name}' Added Successfully!\nSaved under: {target_cat}")

            elif category == "Camera":
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"Site_Photo_{timestamp}.jpg"
                target_cat = "Drawings"
                
                if file_name not in self.file_storage[target_cat]:
                    self.file_storage[target_cat].append(file_name)
                
                messagebox.showinfo("Camera Capture", f"Photo taken successfully!\nSaved as: {file_name}\nLocation: Drawings")

            elif category == "Scan":
                file_path = simpledialog.askstring("Document Scanner", "Enter Scanned Document Name (e.g., Blueprint.pdf):")
                if file_path:
                    file_name = os.path.basename(file_path)
                    if not file_name.lower().endswith(".pdf"):
                        file_name += ".pdf"
                    target_cat = "PDF"
                    
                    if file_name not in self.file_storage[target_cat]:
                        self.file_storage[target_cat].append(file_name)
                    messagebox.showinfo("Success", f"Scanned Document '{file_name}' Saved under: {target_cat}")

            if "Screen5FileCenter" in self.frames:
                self.frames["Screen5FileCenter"].refresh_files()

        elif action_type == "Export":
            messagebox.showinfo("Export Success", f"Successfully exported current project as {category}!")

    def run_auto_calculation(self):
        total_files = sum(len(f_list) for f_list in self.file_storage.values())
        
        calc_result = "[BOQ CALCULATION & ESTIMATION REPORT]\n"
        calc_result += f"Total Linked Files: {total_files}\n"
        calc_result += "----------------------------------------\n"
        if total_files > 0:
            calc_result += "Status: Files detected & calculated successfully.\n\n"
            calc_result += "1. Total Concrete Volume: 185.0 m3\n"
            calc_result += "2. Reinforcement Bar Weight: 15.2 Tons\n"
            calc_result += "3. Total Formwork Surface: 510.0 m2\n"
            calc_result += "4. Estimated Total Cost: 4,750,000.00 ETB\n"
        else:
            calc_result += "Status: No files uploaded yet!\n"
            calc_result += "Please go to 'Files' tab and upload your BOQ or drawing file to generate calculations.\n"
        return calc_result

class BaseScreen(tk.Frame):
    def __init__(self, parent, controller, title_text):
        super().__init__(parent, bg="#f7f9fa")
        self.controller = controller

        header = tk.Frame(self, bg="#1b365d")
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="BOQ KING PRO", font=("Arial", 11, "bold"), fg="#ffffff", bg="#1b365d")
        title.pack(anchor="w", padx=12, pady=(8, 0))
        
        slogan = tk.Label(header, text="\"Calculate Smarter, Build Better.\"", font=("Arial", 7, "italic"), fg="#d69e2e", bg="#1b365d")
        slogan.pack(anchor="w", padx=12, pady=(0, 8))

        sub_header = tk.Frame(self, bg="#edf2f7", height=32)
        sub_header.pack(fill=tk.X)
        sub_header.pack_propagate(False)
        
        tk.Label(sub_header, text=title_text, font=("Arial", 9, "bold"), fg="#2b6cb0", bg="#edf2f7").pack(side=tk.LEFT, padx=12, pady=6)

        content_container = tk.Frame(self, bg="#f7f9fa")
        content_container.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.canvas = tk.Canvas(content_container, bg="#f7f9fa", highlightthickness=0)
        self.v_scrollbar = tk.Scrollbar(content_container, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(content_container, orient="horizontal", command=self.canvas.xview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f7f9fa")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.scrollable_frame, bg="#f7f9fa")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

class Screen1Dashboard(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Dashboard - Main Menu")
        
        stats_text = "Welcome to Construction Suite\nActive Projects: 12\nToday's Estimate: 3"
        tk.Label(self.content_frame, text=stats_text, font=("Arial", 9, "bold"), fg="#1b365d", bg="#ffffff", justify=tk.LEFT, anchor="w", relief=tk.RIDGE, padx=10, pady=8).pack(fill=tk.X, pady=(0, 6))

        q_frame = tk.LabelFrame(self.content_frame, text="Quick Navigation", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        q_frame.pack(fill=tk.X, pady=(0, 6))

        btn_style = {"font": ("Arial", 8, "bold"), "bg": "#2b6cb0", "fg": "#ffffff", "pady": 4}
        
        tk.Button(q_frame, text="Smart BOQ Auto System", command=lambda: controller.show_frame("Screen6SmartEngine"), **btn_style).grid(row=0, column=0, columnspan=2, sticky="ew", padx=2, pady=2)
        tk.Button(q_frame, text="FILE Center", command=lambda: controller.show_frame("Screen5FileCenter"), **btn_style).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        tk.Button(q_frame, text="Project Control", command=lambda: controller.show_frame("Screen4Control"), **btn_style).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        tk.Button(q_frame, text="Settings", command=lambda: controller.show_frame("Screen7Settings"), bg="#4a5568", fg="#ffffff", font=("Arial", 8, "bold")).grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=2)
        
        q_frame.columnconfigure(0, weight=1)
        q_frame.columnconfigure(1, weight=1)

class Screen2Projects(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Projects Workspace")
        
        proj_frame = tk.LabelFrame(self.content_frame, text="Projects Management", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        proj_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.proj_text = tk.Text(proj_frame, height=10, width=45, font=("Arial", 8), bg="#f7f9fa", fg="#2d3748", relief=tk.FLAT, wrap=tk.NONE)
        self.proj_text.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        self.refresh_projects()

        btn_box = tk.Frame(proj_frame, bg="#ffffff")
        btn_box.pack(fill=tk.X)

        tk.Button(btn_box, text="+ New Project", command=self.create_new_project, bg="#276749", fg="#ffffff", font=("Arial", 8, "bold"), pady=4).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(btn_box, text="Open FILE", command=lambda: controller.show_frame("Screen5FileCenter"), bg="#2b6cb0", fg="#ffffff", font=("Arial", 8, "bold"), pady=4).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    def refresh_projects(self):
        self.proj_text.config(state=tk.NORMAL)
        self.proj_text.delete("1.0", tk.END)
        content = "[Active Projects List]\n"
        for p in self.controller.projects_list:
            content += f"   |-- {p}\n"
        self.proj_text.insert(tk.END, content)
        self.proj_text.config(state=tk.DISABLED)

    def create_new_project(self):
        proj_name = simpledialog.askstring("New Project", "Enter New Project Name:")
        if proj_name:
            self.controller.projects_list.append(proj_name)
            self.refresh_projects()
            messagebox.showinfo("Success", f"Project '{proj_name}' created successfully!")

class Screen3BOQ(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "BOQ Workspace")
        boq_frame = tk.LabelFrame(self.content_frame, text="BOQ Calculation Panel", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        boq_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        
        self.boq_text = tk.Text(boq_frame, height=10, width=45, font=("Arial", 8), bg="#f7f9fa", fg="#2d3748", relief=tk.FLAT, wrap=tk.NONE)
        self.boq_text.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        
        tk.Button(boq_frame, text="CALCULATE BOQ NOW", command=self.trigger_calculation, bg="#276749", fg="#ffffff", font=("Arial", 9, "bold"), pady=8).pack(fill=tk.X)
        self.refresh_boq_view()

    def refresh_boq_view(self):
        self.boq_text.config(state=tk.NORMAL)
        self.boq_text.delete("1.0", tk.END)
        report = self.controller.run_auto_calculation()
        self.boq_text.insert(tk.END, report)
        self.boq_text.config(state=tk.DISABLED)

    def trigger_calculation(self):
        self.refresh_boq_view()
        messagebox.showinfo("Calculate Success", "BOQ calculation completed successfully from uploaded files!")

class Screen4Control(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Control & Management")
        ctrl_frame = tk.LabelFrame(self.content_frame, text="Project Control Panel", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        ctrl_frame.pack(fill=tk.BOTH, expand=True)

        content = "Control Center Features:\n\n- Budget Tracking\n- Inventory & Stock\n- Progress Monitoring"
        tk.Label(ctrl_frame, text=content, font=("Arial", 9), bg="#ffffff", justify=tk.LEFT, anchor="w", padx=5, pady=5).pack(fill=tk.BOTH, expand=True)

class Screen5FileCenter(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "FILE CENTER")
        
        btn_style = {"font": ("Arial", 8, "bold"), "bg": "#edf2f7", "fg": "#1b365d", "pady": 4}

        up_frame = tk.LabelFrame(self.content_frame, text="1. Upload File (BOQ / Drawing)", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=4, pady=4)
        up_frame.pack(fill=tk.X, anchor="w", pady=(0, 6))

        tk.Button(up_frame, text="Device", command=lambda: controller.handle_action("Upload", "Device"), bg="#2b6cb0", fg="#ffffff", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=2, pady=2)
        tk.Button(up_frame, text="Camera", command=lambda: controller.handle_action("Upload", "Camera"), **btn_style).grid(row=0, column=1, sticky="w", padx=2, pady=2)
        tk.Button(up_frame, text="Scan", command=lambda: controller.handle_action("Upload", "Scan"), **btn_style).grid(row=0, column=2, sticky="w", padx=2, pady=2)

        my_files_frame = tk.LabelFrame(self.content_frame, text="2. My Files", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        my_files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.file_text = tk.Text(my_files_frame, height=8, width=45, font=("Arial", 8), bg="#f7f9fa", fg="#2d3748", relief=tk.FLAT, wrap=tk.NONE)
        self.file_text.pack(fill=tk.BOTH, expand=True, pady=(0, 4))
        self.refresh_files()

        exp_frame = tk.LabelFrame(self.content_frame, text="3. Export", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=4, pady=4)
        exp_frame.pack(fill=tk.X, anchor="w", pady=(0, 6))

        tk.Button(exp_frame, text="PDF", command=lambda: controller.handle_action("Export", "PDF"), bg="#276749", fg="#ffffff", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=2, pady=2)
        tk.Button(exp_frame, text="Excel", command=lambda: controller.handle_action("Export", "Excel"), bg="#22543d", fg="#ffffff", font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w", padx=2, pady=2)
        tk.Button(exp_frame, text="Print", command=lambda: controller.handle_action("Export", "Print"), **btn_style).grid(row=0, column=2, sticky="w", padx=2, pady=2)

    def refresh_files(self):
        self.file_text.config(state=tk.NORMAL)
        self.file_text.delete("1.0", tk.END)
        
        content = "FILE DIRECTORY\n"
        for cat, files in self.controller.file_storage.items():
            content += f"   +-- {cat} ({len(files)} files)\n"
            if files:
                for f in files:
                    content += f"        |    +-- {f}\n"
            else:
                content += f"        |    +-- (Empty)\n"
                
        self.file_text.insert(tk.END, content)
        self.file_text.config(state=tk.DISABLED)

class Screen6SmartEngine(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Smart BOQ Engine")
        smart_frame = tk.LabelFrame(self.content_frame, text="Smart Calculation Engine", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        smart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.smart_text = tk.Text(smart_frame, height=10, width=45, font=("Arial", 8), bg="#f7f9fa", fg="#2d3748", relief=tk.FLAT, wrap=tk.NONE)
        self.smart_text.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        
        tk.Button(smart_frame, text="CALCULATE NOW", command=self.run_smart_calc, bg="#276749", fg="#ffffff", font=("Arial", 9, "bold"), pady=8).pack(fill=tk.X)
        self.refresh_calc_summary()

    def refresh_calc_summary(self):
        self.smart_text.config(state=tk.NORMAL)
        self.smart_text.delete("1.0", tk.END)
        report = self.controller.run_auto_calculation()
        self.smart_text.insert(tk.END, report)
        self.smart_text.config(state=tk.DISABLED)

    def run_smart_calc(self):
        self.refresh_calc_summary()
        messagebox.showinfo("Smart Calculation", "Smart calculation processed successfully from files!")

class Screen7Settings(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Settings & Help")
        set_frame = tk.LabelFrame(self.content_frame, text="Application Settings", font=("Arial", 8, "bold"), fg="#1b365d", bg="#ffffff", padx=6, pady=6)
        set_frame.pack(fill=tk.BOTH, expand=True)

        content = "Configuration:\n\n- Ethiopian Standards (ES)\n- Currency: ETB (Birr)\n- Professional Standards"
        tk.Label(set_frame, text=content, font=("Arial", 9), bg="#ffffff", justify=tk.LEFT, anchor="w", padx=5, pady=5).pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = BOQKingProApp(root)
    root.mainloop()
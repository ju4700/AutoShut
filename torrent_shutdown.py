import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psutil
import time
import threading
import os
import subprocess
import sys
import json
from pathlib import Path

class TorrentShutdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Shutdown - Torrent Monitor")
        self.root.geometry("445x340")
        self.root.resizable(False, False)
        
        self.monitoring = False
        self.monitor_thread = None
        self.download_path = tk.StringVar()
        self.check_interval = tk.IntVar(value=30)  
        self.shutdown_delay = tk.IntVar(value=60)  
        self.last_activity_time = time.time()
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        ttk.Label(main_frame, text="Download Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path, width=40)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=0, column=1, padx=(5, 0))
        
        path_frame.columnconfigure(0, weight=1)
        
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(settings_frame, text="Check Interval (seconds):").grid(row=0, column=0, sticky=tk.W)
        interval_spin = ttk.Spinbox(settings_frame, from_=10, to=300, textvariable=self.check_interval, width=10)
        interval_spin.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(settings_frame, text="Shutdown Delay (seconds):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        delay_spin = ttk.Spinbox(settings_frame, from_=0, to=600, textvariable=self.shutdown_delay, width=10)
        delay_spin.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))
        
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Status: Ready")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.activity_label = ttk.Label(status_frame, text="")
        self.activity_label.grid(row=1, column=0, sticky=tk.W)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.test_btn = ttk.Button(button_frame, text="Test Shutdown", command=self.test_shutdown)
        self.test_btn.grid(row=0, column=2, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(0, weight=1)
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)
            
    def load_settings(self):
        settings_file = Path("settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.download_path.set(settings.get('download_path', ''))
                    self.check_interval.set(settings.get('check_interval', 30))
                    self.shutdown_delay.set(settings.get('shutdown_delay', 60))
            except Exception:
                pass
                
    def save_settings(self):
        settings = {
            'download_path': self.download_path.get(),
            'check_interval': self.check_interval.get(),
            'shutdown_delay': self.shutdown_delay.get()
        }
        try:
            with open("settings.json", 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass
            
    def start_monitoring(self):
        if not self.download_path.get():
            messagebox.showerror("Error", "Please select a download folder!")
            return
            
        if not os.path.exists(self.download_path.get()):
            messagebox.showerror("Error", "Download folder does not exist!")
            return
            
        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        self.monitor_thread = threading.Thread(target=self.monitor_downloads, daemon=True)
        self.monitor_thread.start()
        
        self.save_settings()
        
    def stop_monitoring(self):
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.status_label.config(text="Status: Stopped")
        self.activity_label.config(text="")
        
    def monitor_downloads(self):
        self.status_label.config(text="Status: Monitoring...")
        inactive_count = 0
        
        while self.monitoring:
            try:
                # for active downloads by monitoring file activity
                current_activity = self.check_download_activity()
                
                if current_activity:
                    inactive_count = 0
                    self.activity_label.config(text="Download activity detected")
                    self.last_activity_time = time.time()
                else:
                    inactive_count += 1
                    time_since_activity = time.time() - self.last_activity_time
                    self.activity_label.config(text=f"No activity for {int(time_since_activity)} seconds")
                    
                    if inactive_count >= 3 and time_since_activity >= 120:
                        self.initiate_shutdown()
                        break
                        
                time.sleep(self.check_interval.get())
                
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
                break
                
    def check_download_activity(self):
        """Check for download activity by monitoring qBittorrent process and network activity"""
        try:
            # if qBittorrent is running and using network
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    if 'qbittorrent' in proc.info['name'].lower():
                        connections = proc.connections()
                        active_connections = [conn for conn in connections if conn.status == 'ESTABLISHED']
                        
                        if active_connections:
                            return True
                            
                        cpu_percent = proc.cpu_percent()
                        if cpu_percent > 1.0: 
                            return True
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            download_dir = Path(self.download_path.get())
            if download_dir.exists():
                current_time = time.time()
                for file_path in download_dir.rglob('*'):
                    if file_path.is_file():
                        if current_time - file_path.stat().st_mtime < self.check_interval.get() * 2:
                            return True
                            
        except Exception:
            pass
            
        return False
        
    def initiate_shutdown(self):
        self.monitoring = False
        self.progress.stop()
        
        countdown_window = tk.Toplevel(self.root)
        countdown_window.title("Shutdown Countdown")
        countdown_window.geometry("300x150")
        countdown_window.transient(self.root)
        countdown_window.grab_set()
        
        countdown_label = ttk.Label(countdown_window, text="", font=("Arial", 14))
        countdown_label.pack(pady=20)
        
        cancel_btn = ttk.Button(countdown_window, text="Cancel Shutdown", 
                               command=lambda: self.cancel_shutdown(countdown_window))
        cancel_btn.pack(pady=10)
        
        for i in range(self.shutdown_delay.get(), 0, -1):
            if not countdown_window.winfo_exists():
                return
                
            countdown_label.config(text=f"Download completed!\nShutting down in {i} seconds...")
            countdown_window.update()
            time.sleep(1)
            
        if countdown_window.winfo_exists():
            countdown_window.destroy()
            self.shutdown_system()
            
    def cancel_shutdown(self, countdown_window):
        countdown_window.destroy()
        self.stop_monitoring()
        
    def shutdown_system(self):
        """Shutdown the system"""
        try:
            if sys.platform == "win32":
                subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
            elif sys.platform == "darwin":  
                subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
            else:  
                subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        except Exception as e:
            messagebox.showerror("Shutdown Error", f"Failed to shutdown: {str(e)}")
            
    def test_shutdown(self):
        """Actually shut down the PC after 30 seconds when testing"""
        result = messagebox.askyesno("Test Shutdown", 
            "This will schedule a real shutdown in 30 seconds.\n\nAre you sure you want to proceed?")
        if result:
            import os
            messagebox.showinfo("Shutdown Scheduled", "Your PC will shut down in 30 seconds.")
            os.system("shutdown /s /t 30")

def main():
    root = tk.Tk()
    app = TorrentShutdownApp(root)
    
    def on_closing():
        if app.monitoring:
            if messagebox.askokcancel("Quit", "Monitoring is active. Do you want to quit?"):
                app.stop_monitoring()
                root.destroy()
        else:
            root.destroy()
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()

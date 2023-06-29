import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Pre-defined commands
commands = {
    "Ping Gateway": "ping {}",
    "Ping DNS": "ping {}",
    "Resolve Public IP": "curl ipinfo.io",
    "Active Ports": "netstat -ano"
}

dns_servers = {
    "1.1.1.1 (Cloudflare)": "1.1.1.1",
    "8.8.8.8 (Google)": "8.8.8.8",
    "208.67.220.123 (Family Safe)": "208.67.220.123",
    "9.9.9.9 (Quad9)": "9.9.9.9"
}

def run_command(command):
    # Run the command and capture the output
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Display the output in a message box
    messagebox.showinfo("Output", output)

    # Save the output to a log file
    with open(f"{file_path.get()}/log.txt", 'a') as file:
        file.write(output.decode('utf-8'))

def execute_predefined_command(command):
    if command == "Ping Gateway":
        ipconfig_output = subprocess.check_output("ipconfig /all", shell=True, stderr=subprocess.STDOUT)
        messagebox.showinfo("IP Configuration", ipconfig_output)
        gateway = simpledialog.askstring("Input", "Enter the default gateway:")
        command = commands[command].format(gateway)
    elif command == "Ping DNS":
        dns_server = dns_servers[selected_dns.get()]
        command = commands[command].format(dns_server)
    else:
        command = commands[command]
    run_command(command)

def execute_custom_command():
    command = custom_command_entry.get()
    run_command(command)

# Create the main window
window = tk.Tk()
window.title("Mr. A's 'I'm too lazy to open a command prompt' command runner and logger")
window.geometry("350x300")  # Set the window size

# Create a frame for the custom commands
custom_frame = tk.Frame(window)
custom_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a text field to enter custom commands
custom_command_entry = tk.Entry(custom_frame)
custom_command_entry.pack(pady=10)

# Create a button to execute the custom command
execute_custom_button = tk.Button(custom_frame, text="Execute Custom Command", command=execute_custom_command)
execute_custom_button.pack()

# Create a frame for the pre-defined commands
predefined_frame = tk.Frame(window)
predefined_frame.grid(row=0, column=1, padx=10, pady=10)

# Create a StringVar to store the selected DNS server
selected_dns = tk.StringVar(window)
selected_dns.set(list(dns_servers.keys())[0])  # Set the default DNS server

# Create a drop-down menu to select a DNS server
dns_menu = tk.OptionMenu(predefined_frame, selected_dns, *dns_servers.keys())
dns_menu.pack()

# Create buttons for the pre-defined commands
for command in commands.keys():
    button = tk.Button(predefined_frame,text=command, command=lambda cmd=command: execute_predefined_command(cmd))
    button.pack()

# Create a frame for the file path
file_path_frame = tk.Frame(window)
file_path_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a StringVar to store the file path
file_path = tk.StringVar(window)

# Create a label for the file path
file_path_label = tk.Label(file_path_frame, text="Log File Path:")
file_path_label.pack()

# Create a text field to display the selected file path
file_path_entry = tk.Entry(file_path_frame, textvariable=file_path)
file_path_entry.pack()

# Create a button to browse for the file path
browse_button = tk.Button(file_path_frame, text="Browse", command=lambda: file_path.set(filedialog.askdirectory()))
browse_button.pack()

# Run the main event loop
window.mainloop()

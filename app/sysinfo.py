import psutil
import multiprocessing

def get_html_system_state():
    result = "<h3><b>System Status</b></h3>\n"
    result += "<div style='width:100%'><div style='width:340px;display:inline-block;margin-bottom:20px;margin-right:40px'><h4>CPU</h4>\n"
    try:
        cpu_percent = psutil.cpu_percent()
        result += f"Percentage usage: {cpu_percent}% <br>\n"
        
        # CPU frequency
        cpu_info = psutil.cpu_freq()
        result += f"Current frequency: {cpu_info.current:.2f} Mhz <br>\n"
        result += f"Minimum frequency: {cpu_info.min:.2f} Mhz <br>\n"
        result += f"Maximum frequency: {cpu_info.max:.2f} Mhz <br>\n"

        max_threads = multiprocessing.cpu_count()
        result += f"<br>Maximum number of threads: {max_threads}<br>\n"
    
    except FileNotFoundError:
        result += "CPU info not available on this system <br>\n"

    result += "</div>"
    result += "<div style='width:340px;display:inline-block;vertical-align:top;margin-bottom:20px'><h4>Memory</h4>\n"
    try:
        ram_info = psutil.virtual_memory()
        result += f"Total: {ram_info.total / 1024 / 1024 / 1024:.2f} GB <br>\n"
        result += f"Available: {ram_info.available / 1024 / 1024 / 1024:.2f} GB <br>\n"
        result += f"Used: {ram_info.used / 1024 / 1024 / 1024:.2f} GB <br>\n"
        result += f"Percentage usage: {ram_info.percent}% <br>\n"
    except FileNotFoundError:
        result += "Memory info not available on this system <br>\n"
    result += "</div></div>"
    
    return result
        
if __name__ == "__main__":
    print(get_html_system_state())
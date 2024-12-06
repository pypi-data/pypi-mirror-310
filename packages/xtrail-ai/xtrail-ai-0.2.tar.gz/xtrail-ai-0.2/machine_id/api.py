import psutil
import subprocess

def execute_python_code(code):
    """
    Execute Python code dynamically.

    Args:
        code (str): Python code to execute.

    Returns:
        dict: Output or error from the execution.
    """
    try:
        exec_globals = {}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)
        return {"message": "Code executed successfully", "output": exec_locals}
    except Exception as e:
        return {"error": f"Failed to execute code: {str(e)}"}

def monitor_resources():
    """
    Monitor system resources like CPU, RAM, and disk usage.

    Returns:
        dict: A dictionary with CPU, RAM, and disk usage percentages.
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        return {
            "cpu_usage": f"{cpu_usage}%",
            "ram_usage": f"{ram_usage}%",
            "disk_usage": f"{disk_usage}%"
        }
    except Exception as e:
        raise RuntimeError(f"Error monitoring resources: {e}")

def start_job(command):
    """
    Start a job or script.

    Args:
        command (list): Command to execute (e.g., ["python", "train.py"]).

    Returns:
        str: Output from the executed command.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {"message": "Job started successfully", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": f"Job failed: {e.stderr}"}

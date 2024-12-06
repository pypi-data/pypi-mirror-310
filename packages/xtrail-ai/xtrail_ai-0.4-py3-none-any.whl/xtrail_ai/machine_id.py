import platform
import uuid
import psutil

def get_machine_id():
    """
    Retrieve a unique machine ID that works across all platforms.

    Returns:
        str: A unique identifier for the machine.
    """
    try:
        if platform.system() in ["Linux", "Darwin"]:
            return platform.node()
        elif platform.system() == "Windows":
            return str(uuid.UUID(int=uuid.getnode()))
        else:
            return f"unknown-{uuid.uuid4()}"
    except Exception as e:
        raise RuntimeError(f"Error retrieving machine ID: {e}")

def get_machine_details():
    """
    Retrieve machine details such as OS, architecture, RAM, and storage.

    Returns:
        dict: A dictionary with machine details.
    """
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        architecture = platform.architecture()[0]
        total_ram = round(psutil.virtual_memory().total / (1024**3), 2)
        disk_usage = psutil.disk_usage('/')
        total_storage = round(disk_usage.total / (1024**3), 2)
        used_storage = round(disk_usage.used / (1024**3), 2)
        free_storage = round(disk_usage.free / (1024**3), 2)
        return {
            "os": f"{system} {release} (Version: {version})",
            "architecture": architecture,
            "total_ram": f"{total_ram} GB",
            "total_storage": f"{total_storage} GB",
            "used_storage": f"{used_storage} GB",
            "free_storage": f"{free_storage} GB"
        }
    except Exception as e:
        raise RuntimeError(f"Error retrieving machine details: {e}")

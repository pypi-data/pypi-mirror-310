import platform
import uuid

def get_machine_id():
    """
    Retrieve a unique machine ID that works across all platforms.

    Returns:
        str: A unique identifier for the machine.
    """
    try:
        # For Linux and macOS, use the hostname
        if platform.system() in ["Linux", "Darwin"]:
            return platform.node()
        # For Windows, generate a hardware-based UUID
        elif platform.system() == "Windows":
            return str(uuid.UUID(int=uuid.getnode()))
        # Fallback: Generate a random UUID (not truly unique, but a placeholder)
        else:
            return f"unknown-{uuid.uuid4()}"
    except Exception as e:
        raise RuntimeError(f"Error retrieving machine ID: {e}")

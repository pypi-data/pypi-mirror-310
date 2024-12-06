import re

class PyANSI:
    # Define the colors
    COLORS = {
        "black": '\033[30m',
        "red": '\033[31m',
        "green": '\033[32m',
        "yellow": '\033[33m',
        "blue": '\033[34m',
        "magenta": '\033[35m',
        "cyan": '\033[36m',
        "white": '\033[37m',
        "reset": '\033[0m',
        "bold": '\033[1m',
        "underline": '\033[4m',
        "black_bg": '\033[40m',
        "red_bg": '\033[41m',
        "green_bg": '\033[42m',
        "yellow_bg": '\033[43m',
        "blue_bg": '\033[44m',
        "magenta_bg": '\033[45m',
        "cyan_bg": '\033[46m',
        "white_bg": '\033[47m',
    }

    @staticmethod
    def apply_colors(text):
        def replace_color(match):
            color_code = match.group(1).lower()
            return PyANSI.COLORS.get(color_code, PyANSI.COLORS['reset'])  # Default to 'reset' if color not found
        
        # Apply color codes and add reset code at the end
        return re.sub(r"\{(.*?)\}", replace_color, text) + PyANSI.COLORS['reset']

# Replace pyansi3.PyANSI.type with a direct print statement
def print_colored(text):
    print(PyANSI.apply_colors(text))
    
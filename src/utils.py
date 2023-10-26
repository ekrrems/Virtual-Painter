import cv2

def get_mouse_click(event, x, y, flags, param):
    """
    Handle mouse click events.
    
    Args:
        event (int): The type of mouse event.
        x (int): The x-coordinate of the mouse click.
        y (int): The y-coordinate of the mouse click.
        flags (int): Additional flags.
        param (object): Additional parameters (not used in this function).

    Returns:
        None
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at (x, y): ({x}, {y})")


def select_pen(coordinates):
    """
    Select the drawing pen based on the coordinates of the mouse click.

    Args:
        coordinates (tuple): A tuple containing x and y coordinates.

    Returns:
        Tuple[bool, int]: A tuple (change, color_id) indicating whether the pen should be changed and the selected color ID.
    """
    X, Y = coordinates
    x, y = 20, 0
    width, height = 100, 120
    if Y < 120 and  0 < X <= 120:
        return True, 1
    elif Y < 120 and  120 < X <= 220:
        return True, 2
    elif Y < 120 and  220 < X <= 320:
        return True, 3
    elif Y < 120 and  320 < X <= 420:
        return True, 4
    elif Y < 120 and  420 < X <= 520:
        return True, 5
    elif Y < 120 and  520 < X <= 620:
        return True, 6
    return False, 0


def choose_color(color_id, image):
    """
    Draw a rectangle on the image to indicate the selected color.

    Args:
        color_id (int): The ID of the selected color.
        image (numpy.ndarray): The image on which to draw the rectangle.

    Returns:
        None
    """
    x, y = 20, 0
    width, height = 100, 120
    if color_id == 1:
        cv2.rectangle(image, (20, 0), (120, 120), (99, 191, 0), 2)
    elif color_id == 2:
        cv2.rectangle(image, (120, 0), (220, 120), (81, 62, 26), 2)
    elif color_id == 3:
        cv2.rectangle(image, (220, 0), (320, 120), (49, 48, 255), 2)
    elif color_id == 4:
        cv2.rectangle(image, (320, 0), (420, 120), (77, 145, 255), 2)
    elif color_id == 5:
        cv2.rectangle(image, (420, 0), (540, 120), (178, 30, 161), 2)
    elif color_id == 6:
        cv2.rectangle(image, (520, 0), (638, 120), (0, 0, 0), 2)


def draw_color(color_id):
    """
    Get the color associated with a given color ID.

    Args:
        color_id (int): The ID of the color.

    Returns:
        Tuple[int, int, int]: The (B, G, R) values of the color.
    """
    if color_id == 1:
        return (99, 191, 0)
    elif color_id == 2:
        return (81, 62, 26)
    elif color_id == 3:
        return (49, 48, 255)
    elif color_id == 4:
        return (77, 145, 255)
    elif color_id == 5:
        return (178, 30, 161)
    elif color_id == 6:
        return (0, 0, 0)
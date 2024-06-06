def calculate_center(bbox: tuple) -> tuple:
    """
    Calculate the center point of a bounding box.

    Given a bounding box defined by its top-left corner coordinates (x, y), width (w), and height (h),
    this function calculates the center point of the bounding box.

    Args:
        bbox (tuple): A tuple containing four values (x, y, w, h) where:
                      x (int or float) - The x-coordinate of the top-left corner.
                      y (int or float) - The y-coordinate of the top-left corner.
                      w (int or float) - The width of the bounding box.
                      h (int or float) - The height of the bounding box.

    Returns:
        tuple: A tuple containing the x and y coordinates of the center point of the bounding box.

    Raises:
        ValueError: If the bbox does not contain exactly four elements.

    Examples:
        >>> calculate_center((0, 0, 10, 10))
        (5.0, 5.0)
    """
    
    if len(bbox) != 4:
        raise ValueError("Bounding box must contain exactly four elements (x, y, w, h).")
    
    x, y, w, h = bbox
    center_x = x + w / 2
    center_y = y + h / 2
    return (center_x, center_y)

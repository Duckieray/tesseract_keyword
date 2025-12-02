import sys
import cv2 as cv

def find_icon_position(icon_path: str, screenshot_path: str, threshold=0.8, word_coords=None, method_string="cv.TM_SQDIFF_NORMED"):
    """Find (x,y) location of an icon in a screenshot.
    Params:
        icon_path -- the filepath of the icon to locate
        screenshot_path -- the filepath of the screenshot in which to locate the icon
        method_string -- the method of template matching to use
        word_coords -- optional, tuple of coordinates to restrict the search area (min_x, min_y, width, height)
        threshold -- float, threshold for the template matching (default 0.8)
    Return:
        (x,y) int tuple, giving the screen coordinates of the located icon's center
    """
 
    icon = cv.imread(icon_path, cv.IMREAD_COLOR)
    screenshot = cv.imread(screenshot_path, cv.IMREAD_COLOR)
    method = eval(method_string)

    screenshot_height, screenshot_width = screenshot.shape[:2]
    icon_height, _ = icon.shape[:2]

    if word_coords:
        x = word_coords[0]
        y = word_coords[1] - 15
        w = screenshot_width
        h = icon_height + 5
        x = max(0, x)
        y = max(0, y)
        w = min(w, screenshot_width - x)
        h = min(h, screenshot_height - h)

        print(f"Word coordinates: {x}, {y}, {w}, {h}")

        if w <= 0 or h <= 0:
            raise ValueError("Adjusted word coordinates result in non-positive width or height")
        
        search_area = screenshot[y:y+h, x:w]
    else:
        search_area = screenshot

    screenshot_height, screenshot_width = search_area.shape[:2]
    print(f"Modified search area size: {screenshot_width}x{screenshot_height}")

    # Find the top left of the icon
    res = cv.matchTemplate(search_area, icon, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
        match_quality = 1 - min_val
    else:
        top_left = max_loc
        match_quality = max_val

    if match_quality < threshold:
        raise ValueError(f"Match quality {match_quality} did not meet the threshold {threshold}")

    if word_coords:
        top_left = top_left[0], top_left[1] + icon_height
        
    # Find the center of the icon
    icon_width, icon_height = icon.shape[:2]
    icon_center = (top_left[0] + icon_width / 2), (top_left[1] + icon_height / 2)
    return icon_center

if __name__ == "__main__":
    icon_path = sys.argv[1]
    screenshot_path = sys.argv[2]
    method_string = sys.argv[3]
    threshold = float(sys.argv[4])
    word_coords = None
    if len(sys.argv) > 5:
        word_coords = tuple(map(int, sys.argv[5:9]))
    result = find_icon_position(icon_path, screenshot_path, method_string, threshold, word_coords)
    print(result)
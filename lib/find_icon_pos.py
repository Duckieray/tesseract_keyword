import cv2 as cv
import subprocess

def find_icon_position(icon_path, screenshot_path, threshold=0.8, word_coords=None,
                       method_string="cv.TM_SQDIFF_NORMED"):
    icon = cv.imread(icon_path, cv.IMREAD_COLOR)
    screenshot = cv.imread(screenshot_path, cv.IMREAD_COLOR)

    method = eval(method_string)

    screenshot_h, screenshot_w = screenshot.shape[:2]
    icon_h, icon_w = icon.shape[:2]

    if word_coords:
        x, y, w, h = word_coords
        y = max(0, y - 15)
        h = icon_h + 10
        w = screenshot_w
        search_area = screenshot[y:y+h, x:x+w]
    else:
        search_area = screenshot

    res = cv.matchTemplate(search_area, icon, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        match_val = 1 - min_val
        top_left = min_loc
    else:
        match_val = max_val
        top_left = max_loc

    if match_val < threshold:
        raise ValueError(f"Match quality {match_val} < threshold {threshold}")

    center_x = top_left[0] + icon_w // 2
    center_y = top_left[1] + icon_h // 2

    return center_x, center_y

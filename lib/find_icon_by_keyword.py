from parse_service import parse_hocr
from find_icon_pos import find_icon_position

def find_icon_next_to_keyword(hocr_file_path, keywords, icon_path, screenshot_path):
    center_x, center_y = parse_hocr(hocr_file_path, keywords)
    if center_x is None or center_y is None:
        return None, None

    word_coords = (center_x - 50, center_y - 10, 100, 20)
    icon_x, icon_y = find_icon_position(icon_path, screenshot_path, 'cv.TM_SQDIFF_NORMED', word_coords)
    return icon_x, icon_y
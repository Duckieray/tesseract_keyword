from bs4 import BeautifulSoup
import difflib

def parse_hocr(hocr_file_path, keywords):
    with open(hocr_file_path, 'r', encoding='utf-8') as file:
        hocr_content = file.read()

    soup = BeautifulSoup(hocr_content, 'html.parser')
    word_elements = soup.find_all('span', class_='ocrx_word')

    keywords_list = keywords.lower().split()
    consecutive_bbox = None

    def is_similar(word1, word2, threshold=0.6):
        return difflib.SequenceMatcher(None, word1, word2).ratio() >= threshold

    for i in range(len(word_elements) - len(keywords_list) + 1):
        match = True
        for j, keyword in enumerate(keywords_list):
            current = word_elements[i + j].get_text(strip=True).lower()

            # wildcard support: keyword="*" matches anything
            if keyword == "*":
                continue

            if not is_similar(current, keyword):
                match = False
                break

        if match:
            bboxes = [parse_bbox(word_elements[i + j]['title']) for j in range(len(keywords_list))]
            consecutive_bbox = combine_bboxes(bboxes)
            break

    if consecutive_bbox:
        return calculate_center(consecutive_bbox)
    else:
        print("Consecutive keywords not found")
        return None, None

def parse_bbox(title):
    bbox_str = title.split('bbox ')[1].split(';')[0]
    return [int(x) for x in bbox_str.split()]

def combine_bboxes(bboxes):
    min_x = min(b[0] for b in bboxes)
    min_y = min(b[1] for b in bboxes)
    max_x = max(b[2] for b in bboxes)
    max_y = max(b[3] for b in bboxes)
    return min_x, min_y, max_x, max_y

def calculate_center(bbox):
    x1, y1, x2, y2 = bbox
    return (x1 + x2) // 2, (y1 + y2) // 2

def get_word_coords(center_x, center_y):
    # used later for icon alignment
    return (center_x - 50, center_y - 10, 100, 20)

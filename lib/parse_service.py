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
        ratio = difflib.SequenceMatcher(None, word1, word2).ratio()
        return ratio >= threshold
    
    for i in range(len(word_elements) - len(keywords_list) + 1):
        match = True
        for j, keyword in enumerate(keywords_list):
            current_word = word_elements[i + j].get_text(strip=True).lower()
            if keyword == "*":
                continue
            if not is_similar(current_word, keyword, 0.6):
                match = False
                break
        if match:
            bboxes = [parse_bbox(word_elements[i + j]['title']) for j in range(len(keywords_list))]
            consecutive_bbox = combine_bboxes(bboxes)
            break

    if consecutive_bbox:
        center_x, center_y = calculate_center(consecutive_bbox)
        return center_x, center_y
    else:
        print("Consecutive keywords not found")
        return None, None, None

# Parse bbox from title attribute
def parse_bbox(title):
    bbox_str = title.split('bbox ')[1].split(';')[0]
    bbox = [int(coord) for coord in bbox_str.split()]
    return bbox

# Combine multiple bounding boxes
def combine_bboxes(bboxes):
    min_x = min(bbox[0] for bbox in bboxes)
    min_y = min(bbox[1] for bbox in bboxes)
    max_x = max(bbox[2] for bbox in bboxes)
    max_y = max(bbox[3] for bbox in bboxes)
    return min_x, min_y, max_x, max_y

# Calculate center coordinates of a bounding box
def calculate_center(bbox):
    center_x = (bbox[0] + bbox[2]) // 2
    center_y = (bbox[1] + bbox[3]) // 2
    return center_x, center_y

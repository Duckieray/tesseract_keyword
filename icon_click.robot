*** Settings ***
Library    find_icon_pos.py
Library    parse_service.py
Library    pyautogui
Library    Screenshot

*** Keywords ***
Click_Icon_Next_To_Keyword
    [Arguments]    ${icon_path}    ${keywords}    ${threshold}=0.8
    ${center_x}    ${center_y}=    Select_Keyword    ${keywords}    no    yes

    ${word_coords}=    get_word_coords    ${center_x}    ${center_y}
    ${icon_x}    ${icon_y}=    find_icon_position    ${icon_path}    ${SCREENSHOT_NAME}    ${threshold}    ${word_coords}
    pyautogui.click    ${icon_x}    ${icon_y}

*** Settings ***
Resource    findKeyword.robot
Library     find_icon_pos.py
Library     parse_service.py
Library     pyautogui

*** Keywords ***
Click_Icon_Next_To_Keyword
    [Arguments]    ${icon_path}    ${keywords}    ${threshold}=0.8

    ${word_x}    ${word_y}=    Select_Keyword    ${keywords}    click=no    for_icon=yes
    ${coords}=    get_word_coords    ${word_x}    ${word_y}

    ${icon_x}    ${icon_y}=    find_icon_position
    ...          ${icon_path}
    ...          ${SCREENSHOT_NAME}
    ...          ${threshold}
    ...          ${coords}

    pyautogui.click    ${icon_x}    ${icon_y}

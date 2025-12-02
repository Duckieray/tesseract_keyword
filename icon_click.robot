*** Settings ***
Library    lib/find_icon_pos.py
Library    pyautogui
Library    Screenshot

*** Variables ***
${SCREENSHOT_NAME}    screenshot.jpg
${ICON}    ../test-data/icon.png

*** Test Cases ***
Find and Click icon
    Locate Icon    ${ICON}
    Click Icon On Screen    ${ICON}

*** Keywords ***
Locate Icon
    [Arguments]    ${icon}
    ${result}=    Find Icon Position    ${icon}    ${SCREENSHOT_NAME}    cv.TM_SQDIFF_NORMED
    Log To Console    ${result}
    Should Be Equal As Strings    ${result}    (303, 735)

Click Icon On Screen
    [Arguments]    ${icon}
    Take Screenshot    ${SCREENSHOT_NAME}
    ${result}=    Find Icon Position    ${icon}    ${SCREENSHOT_NAME}    cv.TM_SQDIFF_NORMED
    Log To Console    ${result}
    pyautogui.Click    ${result[0]}    ${result[1]}
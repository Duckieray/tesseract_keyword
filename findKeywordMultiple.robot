*** Settings ***
Library    Process
Library    pyautogui
Library    Screenshot
Library    lib/parse_service.py
Library    lib/find_icon_pos.py
Library    OperatingSystem

*** Variables ***
${APPLICATION_PATH}    C:\\PATH_TO_APPLICATION
${TESSERACT_PATH}    C:\\Program Files\\Tesseract-OCR\\tesseract.exe
${SCREENSHOT_NAME}    screenshot.jpg
${HOCR_FILENAME}    hocr_output

*** Test Cases ***
Open Application
    Find_Path
    Start Process    ${APPLICATION}    stdout=DEVNULL    stderr=DEVNULL
    Wait Until Keyword Succeeds    20 sec    2 sec    Select_Keyword    KEYWORD
Do Work
    Check_Failure_Flag
    #Put test case here
    #Select_Keyword    keyword

# Terminate
#     Terminate Process    ${handle}    kill=True
    
*** Keywords *** 
Select_Keyword
    [Arguments]    ${keywords}    ${click}=yes    ${for_icon}=no
    Set Global Variable    ${TEST_FAILED}    ${EMPTY}
    Take Screenshot    ${SCREENSHOT_NAME}
    Run Process    ${TESSERACT}    --psm    12    ${SCREENSHOT_NAME}    ${HOCR_FILENAME}    hocr
    ${center_x}    ${center_y}=    parse_hocr    ${HOCR_FILENAME}.hocr    ${keywords}
    Run Keyword If    '${center_x}' == 'None'    Set_Failure_Flag    Keyword not found
    Run Keyword If    '${TEST_FAILED}'    Fail    Keyword not found
    Run Keyword If    '${click}' == 'yes'    pyautogui.click    ${center_x}    ${center_y}
    IF    '${for_icon}' == 'yes'    RETURN    ${center_x}    ${center_y}    END

Click Icon On Screen
    [Arguments]    ${icon}    ${threshold}=0.8
    Take Screenshot    ${SCREENSHOT_NAME}
    ${result}=    Find Icon Position    ${icon}    ${SCREENSHOT_NAME}    ${threshold}
    Log To Console    ${result}
    pyautogui.Click    ${result[0]}    ${result[1]}
    
Click_Icon_Next_To_Keyword
    [Arguments]    ${icon_path}    ${keywords}    ${threshold}=0.8
    ${center_x}    ${center_y}=    Select_Keyword    ${keywords}    no
    ${word_coords}=    Get_Word_Coords    ${center_x}    ${center_y}
    ${result}=    Find Icon Position    ${icon_path}    ${SCREENSHOT_NAME}    ${threshold}    ${word_coords}
    pyautogui.click    ${result[0]}    ${result[1]}

Repeat_Press
    [Arguments]    ${button}    ${count}
    FOR    ${i}    IN RANGE    ${count}
        Press    ${button}
    END

Set_Failure_Flag
    [Arguments]    ${message}
    Set Global Variable    ${TEST_FAILED}    ${message}

Check_Failure_Flag
    Run Keyword If    '${TEST_FAILED}'    Fatal Error    Test Case Failed: ${TEST_FAILED}

Find_Path
    ${os_type}=    Get Environment Variable    OS
    ${if_windows}=    Run Keyword If    '${os_type}' == 'Windows_NT'    Set Variable    Windows
    IF    '${if_windows}' == 'Windows'
        ${home_directory}=    Get Environment Variable    USERPROFILE
        # ${appdata_directory}=    Get Environment Variable    APPDATA
    ELSE
        ${home_directory}=    Get Environment Variable    HOME
    END
    Set Global Variable    ${APPLICATION}    ${home_directory}${APPLICATION_PATH}
    Set Global Variable    ${TESSERACT}    ${home_directory}${TESSERACT_PATH}

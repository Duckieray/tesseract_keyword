*** Settings ***
Library           OperatingSystem
Library           Process
Library           Screenshot
Library           pyautogui
Library           parse_service.py
Library           find_icon_pos.py
Library           window_management.py

Suite Setup       Setup_Docker_Command

*** Variables ***
${SCREENSHOT_NAME}      screenshot.jpg
${HOCR_FILENAME}        output
${WORKDIR}              ${CURDIR}
${TESS_IMAGE}           tesseract-ocr:latest


*** Keywords ***
Setup_Docker_Command
    # Detect platform
    ${os}=    Get Operating System
    Run Keyword If    'Windows' in '${os}'    Set Global Variable    ${DOCKER_CMD}    docker.exe
    ...    ELSE    Set Global Variable    ${DOCKER_CMD}    docker

    # Verify container exists
    ${result}=    Run Process    ${DOCKER_CMD}    images    stdout=True
    Should Contain    ${result.stdout}    tesseract-ocr


Select_Keyword
    [Arguments]    ${keywords}    ${click}=yes    ${for_icon}=no

    # Take screenshot to local disk
    Take Screenshot    ${SCREENSHOT_NAME}

    # Run Tesseract *inside container*
    ${cmd}=    Create List
    ...        ${DOCKER_CMD}
    ...        run
    ...        --rm
    ...        -v    ${WORKDIR}:/data
    ...        ${TESS_IMAGE}
    ...        --psm    12
    ...        /data/${SCREENSHOT_NAME}
    ...        /data/${HOCR_FILENAME}
    ...        hocr

    Log To Console    Executing Tesseract in container:
    Log To Console    ${cmd}

    Run Process    @{cmd}    stdout=True    stderr=True    shell=False

    # Parse OCR results via Python
    ${center_x}    ${center_y}=    parse_hocr    ${HOCR_FILENAME}.hocr    ${keywords}

    # If parse failed
    Run Keyword If    '${center_x}' == 'None'    Fail    Keyword not found: ${keywords}

    # Perform click optionally
    Run Keyword If    '${click}' == 'yes'    pyautogui.click    ${center_x}    ${center_y}

    # For icon-finding keywords
    Run Keyword If    '${for_icon}' == 'yes'    [Return]    ${center_x}    ${center_y}

    [Return]    ${center_x}    ${center_y}

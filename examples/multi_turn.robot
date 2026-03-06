*** Settings ***
Library    RoboAssay

*** Test Cases ***
Test Conversation Consistency
    ${conv}=    Start Conversation
    ${conv}=    Add User Turn     ${conv}    What is the capital of France?
    ${conv}=    Add Assistant Turn    ${conv}    The capital of France is Paris.
    ${conv}=    Add User Turn     ${conv}    And what about Germany?
    ${conv}=    Add Assistant Turn    ${conv}    The capital of Germany is Berlin.
    Conversation Should Be Consistent    ${conv}

Test Last Response References Earlier Context
    ${conv}=    Start Conversation
    ${conv}=    Add User Turn     ${conv}    My favorite color is blue.
    ${conv}=    Add Assistant Turn    ${conv}    That's a great choice! Blue is a calming color.
    ${conv}=    Add User Turn     ${conv}    Can you remind me what I said my favorite color was?
    ${conv}=    Add Assistant Turn    ${conv}    You said your favorite color is blue.
    Last Response Should Reference    ${conv}    blue

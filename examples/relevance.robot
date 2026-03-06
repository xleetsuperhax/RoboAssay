*** Settings ***
Library    RoboAssay

*** Variables ***
${MY_LLM_RESPONSE}    Our refund policy allows returns within 30 days of purchase with a full refund.

*** Test Cases ***
Test Response Is Relevant
    Response Should Be Relevant To    ${MY_LLM_RESPONSE}    refund policy

Test Response Answers The Question
    Response Should Answer Question    ${MY_LLM_RESPONSE}    What is your refund policy?

Test Response Addresses All Parts
    Response Should Address All Parts    ${MY_LLM_RESPONSE}    What is the return window and what kind of refund is offered?

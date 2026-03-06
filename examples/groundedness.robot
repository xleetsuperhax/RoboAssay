*** Settings ***
Library    RoboAssay

*** Variables ***
${CONTEXT}       The company was founded in 2015 by Jane Smith. It has 500 employees and is headquartered in Austin, Texas.
${GROUNDED}      The company, founded in 2015, is based in Austin, Texas.
${HALLUCINATED}  The company was founded in 2015 by Jane Smith and has over 1000 employees across 5 offices worldwide.

*** Test Cases ***
Test Response Is Grounded
    Response Should Be Grounded In    ${GROUNDED}    ${CONTEXT}

Test Response Does Not Hallucinate
    Response Should Not Hallucinate    ${GROUNDED}    ${CONTEXT}

Test Hallucinated Response Fails
    [Documentation]    This test is expected to fail — the response contains hallucinated info.
    [Tags]    expected-fail
    Response Should Not Hallucinate    ${HALLUCINATED}    ${CONTEXT}

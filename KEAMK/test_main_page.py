# import re
import pytest
from playwright.sync_api import Page, expect

# CONFIG ##############################################################################################################x

URL = 'http://selenium.oktwebs.training360.com/react_form.html'

ALERT_ERROR_MESSAGES = {
    'name': 'A name field is empty.',
    'phone': 'Phone number is not long enough.',
    'email': 'Email is in the wrong format.',
}

# TESTS ##############################################################################################################x

def test_home_correct_title(page: Page):
    page.goto(URL)
    expect(page).to_have_title('CodePen - Simple React Form')


def test_home_submit_button_available(page: Page):
    page.goto(URL)
    # expect(page.get_by_text('Submit', exact=True)).to_be_enabled()
    expect(page.get_by_role('button', name='Submit')).to_be_enabled()


@pytest.mark.parametrize(
    'placeholder',
    ['First Name', 'Last Name', 'Phone Number', 'Email Address']
)
def test_home_inputs_available(page: Page, placeholder):
    page.goto(URL)
    input_element = page.get_by_placeholder(placeholder)
    expect(input_element).to_be_visible()


def check_dialog_message(dialog, error_key):
    """Event handler. Used by following test functions"""
    assert dialog.message == ALERT_ERROR_MESSAGES[error_key]
    dialog.accept() # Be kell zárni valahogy, mert különben megáll a tesztfuttatás


def test_form_send_as_empty(page: Page):
    """Example: how to handle alerts.
    Before triggering the alert we need to create an event handler for that.
    """
    page.goto(URL)
    button_submit = page.get_by_role('button', name='Submit')
    page.on('dialog', lambda dialog: check_dialog_message(dialog, 'name'))
    button_submit.click()


@pytest.mark.parametrize(
    'testdata, error_key',
    [
        ([('First Name', 'Elek'), ('Last Name', ''), ('Phone Number', ''), ('Email Address', '')], 'name'),
        ([('First Name', ''), ('Last Name', 'Teszt'), ('Phone Number', ''), ('Email Address', '')], 'name'),
        ([('First Name', 'Elek'), ('Last Name', 'Teszt'), ('Phone Number', ''), ('Email Address', '')], 'phone'),
        ([('First Name', 'Elek'), ('Last Name', 'Teszt'), ('Phone Number', '1111111111'), ('Email Address', '')], 'email')
    ],
    ids=["FirstName only", "LastName only", "FirstName,LastName", "All but Email"]
)
def test_form_error_messages(page: Page, testdata, error_key):
    page.goto(URL)

    # Input mezők feltöltése
    for input_data in testdata:
        element = page.get_by_placeholder(input_data[0])
        element.fill(input_data[1])

    page.on('dialog', lambda dialog: check_dialog_message(dialog, error_key))
    page.get_by_text('Submit').click()






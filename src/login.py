import logging
from random import randint
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

CREDENTIALS = {
    'email': 'admin@simulacontabil.com.br',
    'password': 'admin'
}


def login(page: Page) -> None:
    """
    Performs login on SimulaContábil.

    Navigates to the login page, fills in the credentials and confirms
    that the login was successful by checking a post-login element.

    Args:
        page: Playwright page instance already initialized.

    Raises:
        PlaywrightTimeoutError: If any element is not found
                                or login is not confirmed in time.
    """
    logger.info('Starting login process...')

    try:
        page.goto('https://simulacontabil.netlify.app', wait_until='domcontentloaded')

        # Fill in email
        page.get_by_role('textbox', name='Email').type(CREDENTIALS['email'], delay=randint(50, 200))

        # Fill in password
        page.get_by_role('textbox', name='Senha').type(CREDENTIALS['password'], delay=randint(50, 200))

        # Click login button
        page.get_by_role('button', name='Entrar').click()

        # Confirm login by waiting for a post-login element
        page.get_by_role('link', name='Lançamentos').wait_for(state='visible')

        logger.info('Login successful.')

    except PlaywrightTimeoutError as err:
        logger.error('Login failed: element not found or timeout. Details: %s', err)
        raise
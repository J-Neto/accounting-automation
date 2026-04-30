"""
Automates the entry of financial transactions into an accounting system.

The current system requires each transaction to be entered manually,
which is time-consuming and error-prone.

This script reads a spreadsheet containing the transactions and
automatically inserts them into the accounting system.
"""

import sys
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from src.login import login
from src.spreadsheet import read_spreadsheet
from src.transactions import run_transactions

logging.basicConfig(
    filename='logs/exec.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)


def main():

    # 1. Read the spreadsheet before opening the browser
    transactions = read_spreadsheet('data/lancamentos.xlsx')

    if not transactions:
        logger.critical('No transactions found in the spreadsheet. Exiting.')
        sys.exit(1)

    logger.info('%d transactions loaded from the spreadsheet.', len(transactions))

    # 2. Open the browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='pt-BR'
        )
        page = context.new_page()
        page.set_default_timeout(30000)            # 30s for actions/waits
        page.set_default_navigation_timeout(60000) # 60s for navigation

        # 3. Perform login
        try:
            login(page)
        except PlaywrightTimeoutError:
            logger.critical('Login failed. Exiting.')
            context.close()
            browser.close()
            sys.exit(1)

        # 4. Run transactions and receive the report
        report = run_transactions(page, transactions)

        context.close()
        browser.close()

    # 5. Exit code reflects the result
    if report['failure']:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
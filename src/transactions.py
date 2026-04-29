import logging
from dataclasses import dataclass
import re
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


@dataclass
class Transaction:
    """
    Represents a financial transaction read from the spreadsheet.
    The dataclass validates types at creation time and documents the expected structure.
    """
    description: str
    amount: str
    date: str
    type: str
    category: str
    status: str

    def __post_init__(self):
        """Validations applied right after object creation."""
        if not self.description or self.description is None:
            raise ValueError(f"Field 'description' is empty or invalid: {self.description!r}")

        if not self.amount or self.amount is None:
            raise ValueError(f"Field 'amount' is empty or invalid: {self.amount!r}")

        self.type = self.type.upper().strip()
        self.status = self.status.upper().strip()
        self.category = self.category.capitalize().strip()


def insert_transaction(page: Page, transaction: Transaction) -> None:
    """
    Fills and saves a single transaction in the accounting system.

    Receives the page already on the Transactions screen and a Transaction
    object with validated data. Raises an exception on failure so the
    caller can decide whether to continue or stop.

    Args:
        page:        Playwright page instance on the Transactions screen.
        transaction: Transaction object with the transaction data.

    Raises:
        PlaywrightTimeoutError: If any element is not found in time.
        Exception:              For unexpected errors during form filling.
    """
    logger.info("Inserting transaction: '%s' | Amount: %s", transaction.description, transaction.amount)

    try:
        # Open new transaction modal
        page.get_by_role('button', name='Novo Lançamento').click()

        # Wait for the modal to be visible before filling
        page.get_by_test_id('input-description').wait_for(state='visible')

        # Fill in the fields
        page.get_by_test_id('input-description').fill(transaction.description)
        page.get_by_test_id('input-amount').fill(transaction.amount)
        page.get_by_test_id('input-date').fill(transaction.date)
        page.get_by_test_id('select-type').select_option(transaction.type)
        page.get_by_test_id('select-category').select_option(transaction.category)
        page.locator("div").filter(has_text=re.compile(r"^StatusPendentePagoAtrasado$")).get_by_role("combobox").select_option(transaction.status)

        # Save and wait for the modal to close
        page.get_by_role('button', name='Salvar').click()
        page.get_by_test_id('input-description').wait_for(state='hidden')

        logger.info("Transaction '%s' saved successfully.", transaction.description)

    except PlaywrightTimeoutError as err:
        screenshot_path = f"error_{transaction.description.replace(' ', '_')}.png"
        page.screenshot(path=screenshot_path)
        logger.error(
            "Timeout inserting transaction '%s'. Screenshot saved at '%s'. Details: %s",
            transaction.description, screenshot_path, err
        )
        raise

    except Exception as err:
        screenshot_path = f"error_{transaction.description.replace(' ', '_')}.png"
        page.screenshot(path=screenshot_path)
        logger.error(
            "Unexpected error inserting '%s'. Screenshot saved at '%s'. Details: %s",
            transaction.description, screenshot_path, err
        )
        raise


def run_transactions(page: Page, transactions: list[Transaction]) -> dict:
    """
    Iterates over the transaction list and calls insert_transaction() for each one.

    Does not stop on individual failures — logs the error and continues
    to the next. Returns a report with the result of each item.

    Args:
        page:         Playwright page instance on the Transactions screen.
        transactions: List of Transaction objects from the spreadsheet.

    Returns:
        dict with two keys:
            'success': list of descriptions that were successfully inserted.
            'failure': list of dicts with 'description' and 'error' for failed ones.
    """
    report = {'success': [], 'failure': []}

    # Navigate to the transactions screen once before the loop
    page.get_by_role('link', name='Lançamentos').click()
    page.get_by_role('button', name='Novo Lançamento').wait_for(state='visible')

    for transaction in transactions:
        try:
            insert_transaction(page, transaction)
            report['success'].append(transaction.description)

        except (PlaywrightTimeoutError, Exception) as err:
            # Individual failure does not stop the loop — just log it
            report['failure'].append({
                'description': transaction.description,
                'error': str(err)
            })
            logger.warning(
                "Transaction '%s' marked as failed. Moving to the next one.",
                transaction.description
            )

    _display_report(report)
    return report


def _display_report(report: dict) -> None:
    """Logs an execution summary at the end of the process."""
    total = len(report['success']) + len(report['failure'])
    logger.info("=" * 50)
    logger.info("FINAL REPORT — %d transactions processed", total)
    logger.info("✅ Success: %d", len(report['success']))
    logger.info("❌ Failure: %d", len(report['failure']))

    for item in report['failure']:
        logger.info("  → '%s': %s", item['description'], item['error'])

    logger.info("=" * 50)
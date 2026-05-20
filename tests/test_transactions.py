import pytest
from unittest.mock import MagicMock
from src.transactions import Transaction, insert_transaction

def test_insert_transaction_calls_correct_locators():
  # Creates a false object that imitates a Playwright page
  page = MagicMock()

  transaction = Transaction(
    description="Product sale",
    amount="1500.00",
    date="10/01/2024",
    type="RECEITA",
    category="Vendas",
    status="PAGO"
  )
  
  insert_transaction(page, transaction)
  
  # Verifies if the 'novo lançamento' button was clicked
  page.get_by_role.assert_any_call('button', name='Novo Lançamento')
  
def test_insert_transaction_calls_save_button():
  page = MagicMock()

  transaction = Transaction(
      description="Product sale",
      amount="1500.00",
      date="10/01/2024",
      type="RECEITA",
      category="Vendas",
      status="PAGO"
  )

  insert_transaction(page, transaction)

  # Verifies if the 'Salvar' button was clicked
  page.get_by_role.assert_any_call('button', name='Salvar')
  
def test_insert_transaction_takes_screenshot_on_error():
  page = MagicMock()
  
  # Simulates an error when click a button
  page.get_by_role.return_value.click.side_effect = Exception("Unexpected error")
  
  transaction = Transaction(
    description="Product sale",
    amount="1500.00",
    date="10/01/2024",
    type="RECEITA",
    category="Vendas",
    status="PAGO"
  )
  
  with pytest.raises(Exception):
    insert_transaction(page, transaction)
    
  # Verifies if the screenshot was taken
  page.screenshot.assert_called_once()
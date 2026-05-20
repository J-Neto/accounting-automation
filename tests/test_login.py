import pytest
from unittest.mock import MagicMock
from src.login import login
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def test_login_fills_email():
  page = MagicMock()
  
  login(page)
  
  # Check if email field was filled
  page.get_by_role.assert_any_call('textbox', name='Email')
  
def test_login_fills_password():
  page = MagicMock()
  
  login(page)
  
  # Check if password field was filled
  page.get_by_role.assert_any_call('textbox', name='Senha')
  
def test_login_clicks_enter_button():
  page = MagicMock()
  
  login(page)
  
  # Check if Enter button was clicked
  page.get_by_role.assert_any_call('button', name='Entrar')
  
def test_login_raises_on_timeout():
  page = MagicMock()
  
  # Simulates a timeout when navigate to the page
  page.goto.side_effect = PlaywrightTimeoutError("Timeout")
  
  with pytest.raises(PlaywrightTimeoutError):
    login(page)
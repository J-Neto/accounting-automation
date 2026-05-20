import pytest
from src.spreadsheet import _convert_amount, _convert_date, _unpack_row
from datetime import datetime

def test_convert_amount_integer():
  result = _convert_amount(1500, row_number=2)
  assert result == "1500.00"
  
def test_convert_amount_float():
  result = _convert_amount(1500.5, row_number=2)
  assert result == "1500.50"
  
def test_convert_amount_string_with_comma():
  result = _convert_amount("1.500,50", row_number=2)
  assert result == "1500.50"
  
def test_convert_amount_negative_raises_error():
  with pytest.raises(ValueError):
    _convert_amount(-100, row_number=2)
    
def test_convert_amount_invalid_string_raises_error():
  with pytest.raises(ValueError):
    _convert_amount("abc", row_number=2)
    
def test_convert_date_from_datetime():
  result = _convert_date(datetime(2024, 1, 10), row_number=2)
  assert result == "10/01/2024"
  
def test_convert_date_from_string_br():
  result = _convert_date("10/01/2024", row_number=2)
  assert result == "10/01/2024"
  
def test_convert_date_from_string_iso():
  result = _convert_date("2024-01-10", row_number=2)
  assert result == "10/01/2024"
  
def test_convert_date_invalid_raises_error():
  with pytest.raises(ValueError):
    _convert_date("data-invalida", row_number=2)
    
def test_unpack_row_valid():
  row = ("Product sale", 1500.00, "2024-01-10", "receita", "vendas", "pago")
  result =  _unpack_row(row, row_number=2)
  assert result == ("Product sale", 1500.00, "2024-01-10", "receita", "vendas", "pago")
  
def test_unpack_row_missing_columns_raises_error():
  row = ("Product sale", 1500.00)
  with pytest.raises(ValueError):
    _unpack_row(row, row_number=2)
    
def test_pack_row_empty_field_raises_error():
  row = ("Product sale", 1500.00, "2024-01-10", None, "vendas", "pago")
  with pytest.raises(ValueError):
    _unpack_row(row, row_number=2)
import pytest
import pandas as pd
from datepulator import DateManager

def test_date_conversion():
    dm = DateManager()
    
    # Test basic conversion
    result = dm.convert("2023-12-25", from_format="%Y-%m-%d", to_format="%d/%m/%Y")
    assert result == "25/12/2023"
    
    # Test auto-format detection
    result = dm.convert("2023-12-25")
    assert result == "2023-12-25"

def test_extract_info():
    dm = DateManager()
    
    info = dm.extract_info("2023-12-25")
    assert info["year"] == 2023
    assert info["month"] == 12
    assert info["day"] == 25
    assert info["weekday"] == "Monday"
    assert info["is_weekend"] is False

def test_dataframe_processing():
    dm = DateManager()
    
    # Create test DataFrame
    df = pd.DataFrame({
        "dates": ["2023-12-25", "2023-12-26"]
    })
    
    # Test format conversion
    result_df = dm.process_dataframe(df, "dates", to_format="%d/%m/%Y")
    assert result_df["dates_formatted"].tolist() == ["25/12/2023", "26/12/2023"]
    
    # Test info extraction
    result_df = dm.process_dataframe(df, "dates", extract_info=True)
    assert result_df["dates_year"].tolist() == [2023, 2023]
    assert result_df["dates_month"].tolist() == [12, 12]

def test_date_validation():
    dm = DateManager()
    
    assert dm.validate_date("2023-12-25") is True
    assert dm.validate_date("2023-13-45") is False
    assert dm.validate_date("2023-12-25", format="%Y-%m-%d") is True
    assert dm.validate_date("25/12/2023", format="%Y-%m-%d") is False

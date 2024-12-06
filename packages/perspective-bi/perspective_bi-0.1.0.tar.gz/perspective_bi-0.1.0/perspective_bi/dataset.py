import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Union, Optional, Dict, Any

class DataSet:
    """A wrapper around pandas DataFrame with a declarative API."""
    
    def __init__(self, data: Union[str, pd.DataFrame, Dict[str, Any]]):
        """Initialize DataSet with various input types."""
        if isinstance(data, str):
            if data.endswith('.csv'):
                self.df = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(data)
            else:
                raise ValueError("Unsupported file format")
        elif isinstance(data, pd.DataFrame):
            self.df = data.copy()
        elif isinstance(data, dict):
            self.df = pd.DataFrame(data)
        else:
            raise ValueError("data must be a file path, DataFrame, or dictionary")
        
        # Automatically convert date columns
        self._convert_date_columns()
    
    def _convert_date_columns(self):
        """Automatically detect and convert date columns."""
        common_date_formats = [
            '%Y-%m-%d',           # 2023-12-31
            '%d/%m/%Y',           # 31/12/2023
            '%m/%d/%Y',           # 12/31/2023
            '%Y/%m/%d',           # 2023/12/31
            '%d-%m-%Y',           # 31-12-2023
            '%m-%d-%Y',           # 12-31-2023
            '%Y%m%d',             # 20231231
            '%d.%m.%Y',           # 31.12.2023
            '%Y.%m.%d',           # 2023.12.31
        ]
        
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # Try to detect the date format from a sample value
                sample = self.df[col].dropna().iloc[0] if not self.df[col].empty else None
                if sample:
                    # First try ISO8601 format
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], format='ISO8601')
                        continue
                    except ValueError:
                        pass

                    # Then try common date formats
                    format_found = False
                    for date_format in common_date_formats:
                        try:
                            # First try with the format on the sample
                            datetime.strptime(str(sample), date_format)
                            # If it works, apply to whole column
                            self.df[col] = pd.to_datetime(self.df[col], format=date_format)
                            format_found = True
                            break
                        except ValueError:
                            continue
                    
                    # If no common format works, try mixed format but warn the user
                    if not format_found:
                        try:
                            import warnings
                            warnings.warn(
                                f"Column '{col}' contains dates in mixed or unknown formats. "
                                "Using pandas mixed format parser. This may lead to unexpected results.",
                                UserWarning
                            )
                            self.df[col] = pd.to_datetime(self.df[col], format='mixed')
                        except (ValueError, TypeError):
                            continue
    
    def filter(self, **kwargs):
        """Filter the dataset based on column conditions."""
        df = self.df.copy()
        
        for col, condition in kwargs.items():
            if isinstance(condition, str):
                if condition == 'last_month':
                    today = datetime.now()
                    start_date = today.replace(day=1) - relativedelta(months=1)
                    end_date = today.replace(day=1) - timedelta(days=1)
                    df = df[(df[col] >= start_date) & (df[col] <= end_date)]
                elif condition == 'this_year':
                    year = datetime.now().year
                    df = df[df[col].dt.year == year]
                elif condition == 'last_year':
                    year = datetime.now().year - 1
                    df = df[df[col].dt.year == year]
                else:
                    df = df[df[col] == condition]
            elif isinstance(condition, (list, tuple)):
                df = df[df[col].isin(condition)]
            elif isinstance(condition, dict):
                if 'min' in condition:
                    df = df[df[col] >= condition['min']]
                if 'max' in condition:
                    df = df[df[col] <= condition['max']]
        
        return DataSet(df)
    
    def aggregate(self, group_by: Union[str, List[str]], metrics: Optional[Dict[str, str]] = None):
        """
        Aggregate the dataset by specified columns.
        
        Args:
            group_by: Column(s) to group by
            metrics: Dictionary mapping column names to aggregation functions
                    e.g., {'sales': 'sum', 'quantity': 'mean'}
        """
        if isinstance(group_by, str):
            group_by = [group_by]
            
        if metrics is None:
            # Auto-detect numeric columns and sum them
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            metrics = {col: 'sum' for col in numeric_cols if col not in group_by}
        
        df = self.df.groupby(group_by).agg(metrics).reset_index()
        return DataSet(df)
    
    def sort_values(self, by: Union[str, List[str]], ascending: bool = True):
        """Sort the dataset by specified columns."""
        df = self.df.sort_values(by=by, ascending=ascending)
        return DataSet(df)
    
    def save(self, filepath: str):
        """Save the dataset to a file."""
        if filepath.endswith('.csv'):
            self.df.to_csv(filepath, index=False)
        elif filepath.endswith(('.xls', '.xlsx')):
            self.df.to_excel(filepath, index=False)
        else:
            raise ValueError("Unsupported file format")
    
    def head(self, n: int = 5):
        """Return first n rows of the dataset."""
        return self.df.head(n)
    
    def __getitem__(self, key):
        """Allow accessing columns using square bracket notation."""
        return self.df[key]
    
    @property
    def columns(self):
        """Return list of column names."""
        return self.df.columns.tolist()
    
    @property
    def shape(self):
        """Return the shape of the dataset."""
        return self.df.shape

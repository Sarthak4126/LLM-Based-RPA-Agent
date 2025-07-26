# src/automation/office.py
import win32com.client as win32
from typing import Dict, Any

class OfficeAutomator:
    def __init__(self):
        self.apps: Dict[str, Any] = {}
        self.workbook = None
        self.excel = None

    def _get_or_create_excel(self):
        """Initializes or retrieves the Excel application instance."""
        if 'excel' not in self.apps:
            self.excel = win32.Dispatch("Excel.Application")
            self.excel.Visible = True
            self.apps['excel'] = self.excel
        return self.apps['excel']

    def excel_open(self, filepath: str) -> bool:
        """Opens an Excel workbook."""
        try:
            excel = self._get_or_create_excel()
            self.workbook = excel.Workbooks.Open(filepath)
            return True
        except Exception as e:
            raise Exception(f"Failed to open Excel file '{filepath}': {e}")

    def excel_save(self) -> bool:
        """Saves the active Excel workbook."""
        if not self.workbook:
            raise Exception("No workbook is currently open to save.")
        try:
            self.workbook.Save()
            return True
        except Exception as e:
            raise Exception(f"Failed to save workbook: {e}")

    def close(self):
        """Closes the workbook and quits the Excel application."""
        if self.workbook:
            try:
                self.workbook.Close(SaveChanges=False)
                self.workbook = None
            except Exception as e:
                print(f"Warning: Could not close workbook: {e}")

        if self.excel:
            try:
                self.excel.Quit()
                self.excel = None
                if 'excel' in self.apps:
                    del self.apps['excel']
            except Exception as e:
                print(f"Warning: Could not quit Excel application: {e}")
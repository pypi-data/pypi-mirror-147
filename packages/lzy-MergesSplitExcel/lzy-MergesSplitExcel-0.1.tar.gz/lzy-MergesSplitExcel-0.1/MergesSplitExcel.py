from win32com.client import Dispatch


class MergesSplitExcel:
    def __init__(self):
        self.Application = Dispatch("Excel.Application")
        self.Application.Visible = False
        self.Application.DisplayAlerts = False

    def excel_object(self,**kwargs):
        return self.Application.Workbooks.Open(kwargs.get('filepath'))

    def copy_sheet(self,**kwargs):
        copy_sheet = kwargs.get('copy_excel_object').Worksheets(kwargs.get('copy_sheet'))
        copy_sheet.Copy(None, kwargs.get('paste_excel_object').Sheets(kwargs.get('paste_excel_object').Sheets.Count))
        if kwargs.get('new_sheet_name'):
            kwargs.get('paste_excel_object').Sheets(kwargs.get('paste_excel_object').Sheets.Count).Name = kwargs.get('new_sheet_name')

    def save(self,**kwargs):
        kwargs.get('fileobject').Save()
        self.Application.Quit()

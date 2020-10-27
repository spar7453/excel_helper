import xlwings as xw
from typing import Union, Any
from excel_helper.workbook_helper import WorkBookHelper

class SheetHelper:
    def __init__(self, sheet: xw.main.Sheet):
        self.sheet: xw.main.Sheet = sheet
        self.__last_cell: xw.main.Range = sheet.cells.last_cell
        self.__last_row: int = self.__last_cell.row
        self.__last_col_num: int = self.__last_cell.column

    def iter_row(self, cell: xw.main.Range) -> Union[xw.main.Range, None]:
        if cell.row == self.__last_row:
            return None
        else:
            # seems faster than cell.offset(1, 0)
            return self.sheet.cells(cell.row + 1, cell.column)

    def iter_col(self, cell: xw.main.Range) -> Union[xw.main.Range, None]:
        if cell.column == self.__last_col_num:
            return None
        else:
            # seems faster than cell.offset(0, 1)
            return self.sheet.cells(cell.row, cell.column + 1)

    def find_value_row(self, col: str, value: Any, start_row: int = 1) -> Union[int, None]:
        if col.isalpha():
            col_num = self.column_number(col.upper())
            last_non_empty_row = self.sheet.cells(self.__last_row, col_num).end("up").row
            current_cell = self.sheet.range(col + str(start_row))
            if start_row > last_non_empty_row:
                return None
            else:
                for i in range(start_row, last_non_empty_row + 1):
                    if current_cell.value == value:
                        return i
                    else:
                        current_cell = self.iter_row(current_cell)
                return None
        else:
            return None

    def find_value_col(self, row: int, value: Any, start_col: str = "A") -> Union[str, None]:
        if start_col.isalpha():
            start_col_num = self.column_number(start_col.upper())
            last_non_empty_col = self.sheet.cells(row, self.__last_col_num).end("left").column
            current_cell = self.sheet.range(start_col + str(row))
            if start_col_num > last_non_empty_col:
                return None
            else:
                for i in range(start_col_num, last_non_empty_col + 1):
                    if current_cell.value == value:
                        return self.column_letter(i)
                    else:
                        current_cell = self.iter_col(current_cell)
                return None
        else:
            return None

    @staticmethod
    def column_letter(n: int) -> Union[str, None]:
        string = ""
        ascii_A = ord("A")
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(ascii_A + remainder) + string
        if string == "":
            return None
        else:
            return string

    @staticmethod
    def column_number(col: str) -> Union[str, None]:
        ascii_A = ord("A")
        if col.isalpha():
            n = None
            for alpha in col.upper():
                if n == None:
                    n = 1 + ord(alpha) - ascii_A
                else:
                    n = n * 26 + 1 + ord(alpha) - ascii_A
            return n
        else:
            return None


# active_book = xw.books.active
# checker = WorkBookHelper(xw.books.active)
# sheet = checker.check_sheet("Sheet1")
# sheet_helper = SheetHelper(sheet)
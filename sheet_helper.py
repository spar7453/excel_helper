import xlwings as xw
import pandas as pd
import datetime
from typing import Any, Optional, Dict, List

class SheetHelper:
    def __init__(self, sheet: xw.main.Sheet):
        self.sheet: xw.main.Sheet = sheet
        self.__last_cell: xw.main.Range = sheet.cells.last_cell
        self.__last_row: int = self.__last_cell.row
        self.__last_col_num: int = self.__last_cell.column

    def range(self, cell: str) -> xw.main.Range:
        return self.sheet.range(cell)

    def iter_row(self, cell: xw.main.Range) -> Optional[xw.main.Range]:
        if cell.row == self.__last_row:
            return None
        else:
            # seems faster than cell.offset(1, 0)
            return self.sheet.cells(cell.row + 1, cell.column)

    def iter_col(self, cell: xw.main.Range) -> Optional[xw.main.Range]:
        if cell.column == self.__last_col_num:
            return None
        else:
            # seems faster than cell.offset(0, 1)
            return self.sheet.cells(cell.row, cell.column + 1)

    def get_values_in_col(self, col: str, start_row: Optional[int] = None, end_row: Optional[int] = None) -> pd.Series:
        if col.isalpha():
            upper = col.upper()
            if start_row is None and end_row is None:
                last_non_empty_row = self.sheet.cells(self.__last_row, col).end("up").row
                start_cell = upper + str(1)
                last_cell = upper + str(last_non_empty_row)
                rng = start_cell + ":" + last_cell
                return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
            elif start_row is None and end_row is not None:
                if end_row > 0:
                    start_cell = upper + str(1)
                    last_cell = upper + str(end_row)
                    rng = start_cell + ":" + last_cell
                    return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                else:
                    raise Exception("1 이상의 값을 받아야 합니다")
            elif start_row is not None and end_row is None:
                if start_row > 0:
                    last_non_empty_row = self.sheet.cells(self.__last_row, col).end("up").row
                    start_cell = upper + str(start_row)
                    last_cell = upper + str(last_non_empty_row)
                    rng = start_cell + ":" + last_cell
                    return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                else:
                    raise Exception("1 이상의 값을 받아야 합니다")
            else:
                if start_row > 0:
                    if end_row >= start_row:
                        start_cell = upper + str(start_row)
                        end_cell = upper + str(end_row)
                        rng = start_cell + ":" + end_cell
                        return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                    else:
                        raise Exception("end_row는 start_row 보다 같거나 커야합니다")
                else:
                    raise Exception("1 이상의 값을 받아야 합니다")
        else:
            raise Exception("알파벳을 입력해 주십시오")

    def get_values_in_col(self, col: str, start_row: Optional[int] = None, end_row: Optional[int] = None) -> pd.Series:
        if col.isalpha():
            upper = col.upper()
            if start_row is None and end_row is None:
                last_non_empty_row = self.sheet.cells(self.__last_row, col).end("up").row
                start_cell = upper + str(1)
                last_cell = upper + str(last_non_empty_row)
                rng = start_cell + ":" + last_cell
                return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
            elif start_row is None and end_row is not None:
                if end_row > 0:
                    start_cell = upper + str(1)
                    last_cell = upper + str(end_row)
                    rng = start_cell + ":" + last_cell
                    return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                else:
                    raise Exception("1 이상의 값을 받아야 합니다")
            elif start_row is not None and end_row is None:
                if start_row > 0:
                    last_non_empty_row = self.sheet.cells(self.__last_row, col).end("up").row
                    start_cell = upper + str(start_row)
                    last_cell = upper + str(last_non_empty_row)
                    rng = start_cell + ":" + last_cell
                    return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                else:
                    raise Exception("1 이상의 값을 받아야 합니다")
            else:
                if start_row > 0:
                    if end_row >= start_row:
                        start_cell = upper + str(start_row)
                        end_cell = upper + str(end_row)
                        rng = start_cell + ":" + end_cell
                        return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                    else:
                        raise Exception("end_row는 start_row 보다 같거나 커야합니다")
                else:
                    raise Exception("1 이상의 값을 받아야 합니다")
        else:
            raise Exception("알파벳을 입력해 주십시오")

    def get_values_in_row(self, row: int, start_col: Optional[str] = None, end_col: Optional[str] = None):
        if row > 0 :
            row_str = str(row)
            if start_col is None and end_col is None:
                last_non_empty_col = self.sheet.cells(row, self.__last_col_num).end("left").column
                last_non_empty_col_letter = self.column_letter(last_non_empty_col)
                start_cell = "A" + ":" + row_str
                last_cell = last_non_empty_col_letter + ":" + row_str
                rng = start_cell + ":" + last_cell
                return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
            elif start_col is None and end_col is not None:
                start_cell = "A" + ":" + row_str
                last_cell = end_col + ":" + row_str
                rng = start_cell + ":" + last_cell
                return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
            elif start_col is not None and end_col is None:
                last_non_empty_col = self.sheet.cells(row, self.__last_col_num).end("left").column
                last_non_empty_col_letter = self.column_letter(last_non_empty_col)
                start_cell = start_col + ":" + row_str
                last_cell = last_non_empty_col_letter + ":" + row_str
                rng = start_cell + ":" + last_cell
                return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
            else:
                start_col_num = self.column_number(start_col)
                end_col_num = self.column_number(end_col)
                if end_col_num >= start_col_num:
                    start_cell = start_col + ":" + row_str
                    last_cell = end_col + ":" + row_str
                    rng = start_cell + ":" + last_cell
                    return self.sheet.range(rng).options(pd.DataFrame, index=False, header=False).value.squeeze()
                else:
                    raise Exception("end_col은 start_col 뒤에 있어야 합니다.")
        else:
            raise Exception("1 이상의 값을 받아야 합니다")

    def get_all_values_in_col(self, col: str) -> pd.Series:
        return self.get_values_in_col(col)

    def get_all_values_in_col(self, row: int) -> pd.Series:
        return self.get_values_in_row(row)

    def get_value_idx_in_col(self, col) -> Dict[Any, List[str]]:
        column_values = self.get_all_values_in_col(col)
        dict = {}
        for idx, value in zip(column_values.index, column_values.values):
            if value is not None:
                cell = col + str(idx + 1)
                if type(value) == datetime.datetime:
                    date_string = value.strftime("%Y-%m-%d")
                    if date_string in dict:
                        dict[date_string].append(cell)
                    else:
                        dict[date_string] = [cell]
                else:
                    if value in dict:
                        dict[value].append(cell)
                    else:
                        dict[value] = [cell]
            else:
                continue
        return dict

    def get_value_idx_in_row(self, row) -> Dict[Any, List[str]]:
        row_values = self.get_all_values_in_row(row)
        dict = {}
        for idx, value in zip(row_values.index, row_values.values):
            if value is not None:
                cell = self.column_letter(idx + 1) + str(row)
                if type(value) == datetime.datetime:
                    date_string = value.strftime("%Y-%m-%d")
                    if date_string in dict:
                        dict[date_string].append(cell)
                    else:
                        dict[date_string] = [cell]
                else:
                    if value in dict:
                        dict[value].append(cell)
                    else:
                        dict[value] = [cell]
            else:
                continue
        return dict

    def get_col_from_cell(self, cell: str) -> str:
        return self.column_letter(self.sheet.range(cell).column)

    def get_row_from_cell(self, cell: str) -> int:
        return self.sheet.range(cell).row

    def filter_cells_after_col(self, cell_list: List[str], col: str) -> List[str]:
        if col.isalpha():
            col_num = self.column_number(col)
            res = []
            for cell in cell_list:
                cell_col = self.get_col_from_cell(cell)
                if self.column_number(cell_col) > col_num:
                    res.append(cell)
                else:
                    continue
            return res
        else:
            raise Exception("알파벳을 입력해 주십시오")

    def filter_cells_after_row(self, cell_list: List[str], row: int) -> List[str]:
        if row > 0:
            res = []
            for cell in cell_list:
                cell_row = self.get_row_from_cell(cell)
                if cell_row > row:
                    res.append(cell)
                else:
                    continue
            return res
        else:
            raise Exception("1 이상의 값을 받아야 합니다")

    def find_first_location_in_col(self, col: str, value: Any, start_row: int = 1) -> str:
        upper = col.upper()
        all_locations = self.get_value_idx_in_col(col)[value]
        filtered_locations = self.filter_cells_after_row(all_locations, start_row)
        if len(filtered_locations) == 0:
            raise Exception(f"{upper}열에서 {value} 값을 찾을 수 없습니다.")
        else:
            return filtered_locations[0]

    def find_first_location_in_row(self, row: int, value: Any, start_col: str = "A") -> str:
        all_locations = self.get_value_idx_in_row(row)[value]
        filtered_locations = self.filter_cells_after_col(all_locations, start_col)
        if len(filtered_locations) == 0:
            raise Exception(f"{row}행에서 {value} 값을 찾을 수 없습니다.")
        else:
            return filtered_locations[0]

    @staticmethod
    def column_letter(n: int) -> str:
        if n < 1:
            raise Exception("1 이상의 값을 받아야합니다.")
        else:
            string = ""
            ascii_A = ord("A")
            while n > 0:
                n, remainder = divmod(n - 1, 26)
                string = chr(ascii_A + remainder) + string
            return string

    @staticmethod
    def column_number(col: str) -> int:
        ascii_A = ord("A")
        if col.isalpha():
            n = 0
            for alpha in col.upper():
                if n is None:
                    n = 1 + ord(alpha) - ascii_A
                else:
                    n = n * 26 + 1 + ord(alpha) - ascii_A
            return n
        else:
            raise Exception("알파벳을 받아야합니다.")

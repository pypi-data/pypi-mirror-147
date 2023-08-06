import pandas
from enum import Enum
from datetime import datetime

class ColumnFormat(Enum):
    Text=0,
    Float=1,
    Integer=2,
    Boolean=3,
    Datetime=4

DEFAULT_FORMAT_VALUE = {
    ColumnFormat.Text: '',
    ColumnFormat.Float: 0.0,
    ColumnFormat.Integer: 0,
    ColumnFormat.Boolean: False,
    ColumnFormat.Datetime: datetime(1900, 1, 1)
}

DEFAULT_FORMAT_TYPE = {
    ColumnFormat.Text: str,
    ColumnFormat.Float: float,
    ColumnFormat.Integer: int,
    ColumnFormat.Boolean: bool
    # DateTime does not have a default Type, must be implemented on its own
}


class Column():
    def __init__(self, original_key:str, new_key:str, format:ColumnFormat):
        self.original_key = original_key
        self.new_key = new_key
        self.format = self.format

    def Standardize(self, dataframe:pandas.DataFrame):
        dataframe = self.Enforce_Key_To_Exist(self, dataframe)
        dataframe = self.Enforce_Values_To_Exist(self, dataframe)
        dataframe = self.Enforce_Type_For_Dataframe(self, dataframe)
        dataframe = self.Rename_Dataframe(self, dataframe)
        return dataframe

    def Enforce_Key_To_Exist(self, dataframe:pandas.DataFrame):
        if self.original_key not in dataframe:
            dataframe[self.original_key] = DEFAULT_FORMAT_VALUE(self.format)
        return dataframe

    def Enforce_Values_To_Exist(self, dataframe:pandas.DataFrame):
        return dataframe[self.original_key].fillna(DEFAULT_FORMAT_VALUE(self.format))
    
    def Enforce_Type_For_Dataframe(self, dataframe:pandas.DataFrame):
        if self.format != ColumnFormat.DateTime:
            dataframe[self.original_key] = dataframe[self.original_key].asype(DEFAULT_FORMAT_TYPE(self.format))
        elif self.format == ColumnFormat.DateTime:
            pandas.to_datetime(dataframe[self.original_key], format='%Y-%m-%d')
        return dataframe

    def Rename_Dataframe(self, dataframe:pandas.DataFrame):
        return dataframe.rename(columns={self.original_key: self.new_key})


def Get_All_Original_Keys(column_list:list(Column)):
    return [column.original_key for column in column_list]


def Get_All_New_Keys(column_list:list(Column)):
    return [column.new_key for column in column_list]


# Overwrites existing by key and adds new lines
def Merge_Dataframes(df1:pandas.DataFrame, df2:pandas.DataFrame, by_keys:list(str), sort_by:str): 
    return pandas.concat([df1, df2]).drop_duplicates(by_keys, keep='last').sort_values(sort_by)


# Removes any Column which key does not match the given keys
def Only_Include_Keys_In_Dataframe(dataframe:pandas.DataFrame, keys:list(str)):
    for column in dataframe:
        if column not in keys:
            dataframe = dataframe.drop(columns=[column])
    return dataframe


# Removes given keys from Dataframe
def Exclude_Keys_In_Dataframe(dataframe:pandas.DataFrame, keys:list(str)):
    for column in dataframe:
        if column in keys:
            return dataframe.drop(columns=[column])

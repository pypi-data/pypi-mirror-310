#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import pandas as pd
import os
from mtbp3 import util
    
class ictvmsl:
    def __init__(self, msl_file_path = ""):
        if not isinstance(msl_file_path, str):
            raise TypeError("msl_file_path must be a string")

        if msl_file_path:
            self.msl_file_path = msl_file_path
            self.msl_file_fullpath = msl_file_path
        else:
            self.msl_file_path = f'supp_seq/ICTV_MSL39v4_example.csv'
            self.msl_file_fullpath = util.get_data(self.msl_file_path)

        self.msl_version = ""
        self.msl_column_names = []
        self.msl = self.__load_list()

        if self.msl is not None:
            self.msl_column_names = self.msl.columns.tolist()
            print(f"File {self.msl_file_path} has been loaded")
            print("Column names:", self.msl.columns.tolist())
            print("Total number of rows:", len(self.msl))

    def __load_list(self):
        #file_path = f'./mtbp3/data/supp_seq/ICTV_MSL39v4_example.csv'
        file_path = self.msl_file_fullpath
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def find_rows_given_str(self, search_str="", search_rank="Species", color=""):
        """
        Find rows in the DataFrame that contain the given search string.
        Parameters:
        search_str (str): The string to search for in the DataFrame. Must be a nonempty string.
        search_rank (str): The column name to search within. Must be 'all' or one of the column names in the DataFrame. Default is "Species".
        neighbor_rank (str): (Unused parameter, can be removed or implemented in future versions).
        Returns:
        DataFrame: A DataFrame containing rows that match the search criteria.
        Raises:
        TypeError: If search_str is not a string.
        ValueError: If search_str is an empty string.
        ValueError: If search_rank is not 'all' and not a valid column name in the DataFrame.
        """

        if not isinstance(search_str, str):
            raise TypeError("search_str must be a string")
        if not search_str:
            raise ValueError("search_str must be a nonempty string")
        if search_rank and search_rank != "all" and search_rank not in self.msl_column_names:
            raise ValueError(f"search_rank must be 'all' or one of the following: {', '.join(self.msl_column_names)}")

        if search_rank == "all":
            filtered_df = self.msl[self.msl.apply(lambda row: search_str.lower() in row.astype(str).str.lower().values, axis=1)]
            if color:
                for col in self.msl_column_names:
                    filtered_df[col] = filtered_df[col].apply(lambda row: util.cdt.color_str(row, words=search_str, colors=color) if pd.notna(row) else row)
        else:
            filtered_df = self.msl[self.msl[search_rank].str.contains(search_str, case=False, na=False)]
            if color:
                filtered_df[search_rank] = filtered_df[search_rank].apply(lambda row: util.cdt.color_str(row, words=search_str, colors=color))

        return filtered_df

if __name__ == "__main__":
    pass

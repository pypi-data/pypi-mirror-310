import pandas as pd
import os


class FileMerger:
    def __init__(self, folder_path, output_path):
        self.merged_file_path = None
        self.folder_path = folder_path
        self.output_path = output_path

    def merge_excel_files(self):
        all_data = pd.DataFrame()
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(self.folder_path, file_name)
                df = pd.read_excel(file_path)
                all_data = pd.concat([all_data, df], ignore_index=True)

        all_data.to_excel(self.output_path, index=False)
        print("Merged Excel files saved to", self.output_path)

    def merge_csv_files(self):
        all_data = pd.DataFrame()
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(self.folder_path, file_name)
                df = pd.read_csv(file_path)
                all_data = pd.concat([all_data, df], ignore_index=True)
        all_data.to_csv(self.output_path, index=False)
        print("Merged CSV files saved to", self.output_path)

        self.merged_file_path = self.output_path

    def get_merged_file_path(self):
        return self.merged_file_path

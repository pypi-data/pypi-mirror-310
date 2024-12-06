import os
import pandas as pd
import pytest
from data_merge.file_merger import FileMerger


@pytest.fixture
def test_data_folder(tmpdir):
    # Create a temporary directory for testing
    temp_folder = tmpdir.mkdir("data")

    # Create sample CSV files
    csv_data1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    csv_data2 = pd.DataFrame({"A": [7, 8, 9], "B": [10, 11, 12]})
    csv_file1 = temp_folder.join("data1.csv")
    csv_file2 = temp_folder.join("data2.csv")
    csv_data1.to_csv(csv_file1, index=False)
    csv_data2.to_csv(csv_file2, index=False)

    yield temp_folder
    temp_folder.remove()


def test_merge_csv_files(test_data_folder):
    output_path = os.path.join(test_data_folder, "merged.csv")
    merger = FileMerger(str(test_data_folder), output_path)
    merger.merge_csv_files()

    # Check if the merged file was created
    assert os.path.isfile(output_path)

    # Check if the merged file contains the expected data
    merged_data = pd.read_csv(output_path)
    expected_data = pd.DataFrame({"A": [1, 2, 3, 7, 8, 9], "B": [4, 5, 6, 10, 11, 12]})
    merged_data = merged_data.sort_values(by=["A", "B"]).reset_index(drop=True)
    expected_data = expected_data.sort_values(by=["A", "B"]).reset_index(drop=True)
    assert merged_data.equals(expected_data)



import pandas as pd
import os
import zipfile

# Test the file splitting logic
def test_file_split():
    # Read test data
    df = pd.read_csv('test_data.csv')
    print("Original data:")
    print(df)
    print()

    # Split by City column
    column = 'City'
    groups = df.groupby(column)

    print(f"Splitting by column: {column}")
    print(f"Number of groups: {len(groups)}")
    print()

    # Create test output directory
    os.makedirs('test_output', exist_ok=True)

    # Create split files
    for name, group in groups:
        print(f"Group: {name}")
        print(group)
        print()

        # Save as CSV
        filename = f'{name}_test_data.csv'
        filepath = os.path.join('test_output', filename)
        group.to_csv(filepath, index=False)

    # Create ZIP file
    zip_path = 'test_output/split_test.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir('test_output'):
            if file.endswith('.csv'):
                zipf.write(os.path.join('test_output', file), file)

    print(f"ZIP file created: {zip_path}")
    print("Test completed successfully!")

if __name__ == '__main__':
    test_file_split()
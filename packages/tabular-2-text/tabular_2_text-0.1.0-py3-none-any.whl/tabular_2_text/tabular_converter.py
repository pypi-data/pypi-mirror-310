import pandas as pd

def dataframe_to_text(input_data, output_file_path):
    """
    Converts a DataFrame or a CSV file to a text file with formatted content.
    The text file is created in your local project folder.

    Parameters:
        input_data (str or pd.DataFrame): The input can be a file path to a CSV file or a pandas DataFrame.
        output_file_path (str): The path to save the generated text file.

    Returns:
        str: The path to the generated text file.
    """
    # Load the DataFrame from a CSV file if input_data is a file path
    if isinstance(input_data, str):
        df = pd.read_csv(input_data)
    elif isinstance(input_data, pd.DataFrame):
        df = input_data
    else:
        raise ValueError("Input data must be a file path (str) or a pandas DataFrame.")

    # Convert the DataFrame to text
    text_content = []
    for index, row in df.iterrows():
        entry = [f"{col}: {row[col]}" for col in df.columns]
        text_content.append('\n\n'.join(entry))

    # Write the content to the text file
    with open(output_file_path, 'w') as file:
        file.write('\n\n***********************************************\n\n'.join(text_content))
    
    print(f"{output_file_path} is in your local project folder.")
    return output_file_path
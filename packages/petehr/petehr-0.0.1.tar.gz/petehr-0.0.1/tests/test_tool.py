import os
import tempfile

from petehr import Text2Code


def test_text2code():
    # Create a temporary CSV file with mappings
    csv_content = """text,cui
hello,C001
test,C002
python code,C003
"""
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=".csv"
    ) as dictionary_file:
        dictionary_file.write(csv_content)
        dictionary_path = dictionary_file.name

    # Initialize Text2Cui and load the temporary dictionary
    processor = Text2Code(dictionary_path)

    # Define test inputs and expected outputs
    test_cases = [
        ("hello world!", "C001"),
        ("this is a test case", "C002"),
        ("some python code here", "C003"),
        ("unknown text", ""),
    ]

    # Test each case
    for inp_text, expected_cuis in test_cases:
        assert (
            processor.convert(inp_text) == expected_cuis
        ), f"Failed for input: {inp_text}"

    print("All test cases passed.")

    # Clean up the temporary file
    os.remove(dictionary_path)


# Run the test
test_text2code()

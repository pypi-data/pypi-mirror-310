import os
import tempfile

from ehrt import Text2Cui  # Replace 'tether' with the actual module name if different


def test_text2cui():
    # Create a temporary CSV file with mappings
    csv_content = """text,cui
hello,C001
test,C002
python code,C003
"""
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=".csv"
    ) as temp_file:
        temp_file.write(csv_content)
        temp_path = temp_file.name

    # Initialize Text2Cui and load the temporary dictionary
    text2cui_processor = Text2Cui(temp_path)

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
            text2cui_processor.traverse(inp_text) == expected_cuis
        ), f"Failed for input: {inp_text}"

    print("All test cases passed.")

    # Clean up the temporary file
    os.remove(temp_path)


# Run the test
test_text2cui()

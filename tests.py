from parser import ParseListOfTasks

def test_parser():
    parser = ParseListOfTasks()

    # Test case 1: Simplest task description
    input_str = "Task1 takes 1\nneeds none\n"
    expected_output = [('Task1', 1, 'none')]
    result = parser.parse(input_str)
    assert result == expected_output, f"Test case 1 failed: {result}"

    # Test case 2: Task with dependencies
    input_str = "Task2 takes 2\nneeds ((Task1 and Task3) or Task4)\n"
    expected_output = [('Task2', 2, '((Task1 and Task3) or Task4)')]
    result = parser.parse(input_str)
    assert result == expected_output, f"Test case 2 failed: {result}"

    # Test case 3: Multiple tasks with dependencies
    input_str = "Task1 takes 1\nneeds none\nTask2 takes 2\nneeds Task1\nTask3 takes 3\nneeds Task2\n"
    expected_output = [('Task1', 1, 'none'), ('Task2', 2, 'Task1'), ('Task3', 3, 'Task2')]
    result = parser.parse(input_str)
    assert result == expected_output, f"Test case 3 failed: {result}"

    # Test case 4: Invalid input with missing fields
    input_str = "Task1 takes 1\n"
    expected_output = []
    result = parser.parse(input_str)
    assert result == expected_output, f"Test case 4 failed: {result}"

    # Test case 5: Invalid input with incorrect format
    input_str = "Task1 takes 1\nneeds Task2 or\n"
    expected_output = []
    result = parser.parse(input_str)
    assert result == expected_output, f"Test case 5 failed: {result}"

    print("All test cases passed!")

# Run the test case
test_parser()

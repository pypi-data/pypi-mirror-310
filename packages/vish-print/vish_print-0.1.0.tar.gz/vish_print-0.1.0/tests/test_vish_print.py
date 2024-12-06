# tests/test_vish_print.py
import io
import unittest
from vish_print import print_output

class TestAdvancedPrint(unittest.TestCase):

    def test_plain_print(self):
        captured_output = io.StringIO()
        print_output.print_output("Hello", "World", file=captured_output)
        self.assertEqual(captured_output.getvalue().strip(), "Hello World")

    def test_json_format(self):
        captured_output = io.StringIO()
        print_output.print_output("Hello", "World", file=captured_output, format_type="json")
        self.assertEqual(captured_output.getvalue().strip(), '{"message": "Hello World"}')

    def test_log_output(self):
        with self.assertLogs("vish_print.printer", level="INFO") as log:
            print_output.print_output("Test", "Log", log=True)
        self.assertTrue(any("Test Log" in message for message in log.output))

if __name__ == "__main__":
    unittest.main()

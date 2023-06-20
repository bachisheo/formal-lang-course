"""
Main script to run interpreter from CLI
"""
import sys
import shared


sys.path.insert(1, str(shared.ROOT))
from project.Lagraph.parser_utils import interpret_file

from project.Lagraph.Exceptions import InterpretingError

if __name__ == "__main__":
    try:
        print(interpret_file(sys.argv[1]))
    except InterpretingError as e:
        print("Interpretation error: " + str(e))

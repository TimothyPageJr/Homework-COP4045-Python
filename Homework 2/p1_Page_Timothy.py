def line_number(input_filename: str, output_filename: str) -> None:
    """Read a text file and write its lines prefixed with line numbers."""
    try:
        with open(input_filename, "r", encoding="utf-8") as input_file:
            with open(output_filename, "w", encoding="utf-8") as output_file:
                for number, line in enumerate(input_file, start=1):
                    output_file.write(f"{number}. {line}")
    except Exception as error:
        print(f"Error processing the file: {error}")
        raise


def parse_functions(filename: str) -> tuple:
    """Parse functions from a Python file and return their information."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        functions = []

        for index, line in enumerate(lines):
            stripped_line = line.strip()

            # Look only for top-level function definitions.
            if line.startswith("def "):
                function_name = stripped_line.split("def ", 1)[1].split("(", 1)[0]

                arguments = (
                    stripped_line.split("(", 1)[1]
                    .split(")", 1)[0]
                )

                code_lines = [line]
                next_index = index + 1

                
                while next_index < len(lines):
                    next_line = lines[next_index]
                    next_stripped = next_line.strip()

                    
                    if (
                        next_stripped
                        and not next_stripped.startswith("#")
                        and not next_line.startswith((" ", "\t"))
                    ):
                        break

                    
                    if next_stripped and not next_stripped.startswith("#"):
                        code_lines.append(next_line)

                    next_index += 1

                function_code = "".join(code_lines)

                functions.append(
                    (
                        index + 1,
                        function_name,
                        arguments,
                        function_code,
                    )
                )

        # Sort alphabetically by function name.
        functions.sort(key=lambda item: item[1])

        return tuple(functions)

    except Exception as error:
        print(f"Error processing the file: {error}")
        raise


def main() -> None:
    """Test line_number and parse_functions."""
    source_file = "p1_Page_Timothy.py"
    numbered_file = "p1_Page_Timothy.py.txt"

    line_number(source_file, numbered_file)

    parsed_functions = parse_functions(source_file)

    print("Parsed functions:")
    for function in parsed_functions:
        print(function)


if __name__ == "__main__":
    main()
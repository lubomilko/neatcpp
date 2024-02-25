from cpreproc import CPreprocessor


def main() -> None:
    cpp = CPreprocessor()
    cpp.process_file("input_sample.c")
    with open("out_test_file.c", "w", encoding="utf-8") as file:
        file.write(cpp.output.code)


if __name__ == "__main__":
    main()

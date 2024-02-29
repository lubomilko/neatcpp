from cpreproc import CPreprocessor


def main() -> None:
    cpp = CPreprocessor()
    cpp.process_file("src1.c")
    with open("src1_out.c", "w", encoding="utf-8") as file:
        file.write(cpp.out_code)

    cpp = CPreprocessor()
    cpp.process_file("src2.c")
    with open("src2_out.c", "w", encoding="utf-8") as file:
        file.write(cpp.out_code)


if __name__ == "__main__":
    main()

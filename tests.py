from functions.get_file_content import get_file_content


def test():
    result = get_file_content("calculator", "main.py")
    print("Result for 'calculator/main.py' file:")
    print(result)
    print("==================================================")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'calculator/pkg/calculator.py' file:")
    print(result)
    print("==================================================")

    result = get_file_content("calculator", "/bin/cat")
    print("Result for 'calculator/bin/cat' file:")
    print(result)
    print("")
    print("==================================================")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'calculator/pkg/does_not_exist.py' file:")
    print(result)
    print("==================================================")


if __name__ == "__main__":
    test()

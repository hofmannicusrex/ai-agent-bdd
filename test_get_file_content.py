# /test_get_files_info.py

from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
# print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt length: {result}")
print(f"lorem.txt truncated: {'truncated' in result}")

#################################################
# # First round of tests.
# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))
# print(get_files_info("calculator", "main.py"))

# # Second round of tests.
# print("Result for current directory:")
# print(get_files_info("calculator", "."))

# print("Result for 'pkg' directory:")
# print(get_files_info("calculator", "pkg"))

# print("Result for '/bin' directory:")
# print(get_files_info("calculator", "/bin"))

# print("Result for '../' directory:")
# print(get_files_info("calculator", "../"))

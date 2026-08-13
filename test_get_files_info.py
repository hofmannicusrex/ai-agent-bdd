# /test_get_files_info.py

from functions.get_files_info import get_files_info


# First round of tests.
# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))
# print(get_files_info("calculator", "main.py"))

# Second round of tests.
print("Result for current directory:")
print(get_files_info("calculator", "."))

print("Result for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))

print("Result for '/bin' directory:")
print(get_files_info("calculator", "/bin"))

print("Result for '../' directory:")
print(get_files_info("calculator", "../"))

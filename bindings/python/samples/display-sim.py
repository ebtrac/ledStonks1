import textwrap

txt = input()
fmttd_str = textwrap.fill(txt, width=16)
print("Rows used:", fmttd_str.count("\n"))
print("Total chars (unformatted string):", len(txt))
print(fmttd_str)

fmttd_str_array = fmttd_str.split("\n")
print()
print(fmttd_str_array)

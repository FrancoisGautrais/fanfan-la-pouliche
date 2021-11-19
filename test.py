# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"\$register_module\(\)"

test_str = ("\"use strict\";\n\n"
	"$register_module();\n\n"
	"$require(\"test2.js\");\n"
	"var x = 1;")

subst = "Erreuer"

# You can manually specify the number of replacements by changing the 4th argument
result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

if result:
    print (result)

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

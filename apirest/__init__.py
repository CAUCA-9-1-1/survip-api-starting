import os
import sys

# This will add our library package without needing to install it
if os.path.isdir("../causepy"):
	sys.path.append("../causepy")

temp = ["cryo", "cryo", "hydro", "cryo"]

if all(i in ("cryo", "hydro") for i in temp):
      print("yes")
else:
      print("no")
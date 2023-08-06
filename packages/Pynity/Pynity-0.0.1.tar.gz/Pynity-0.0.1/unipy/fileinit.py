def unipyinit(scriptname):
  f = open(scriptname + ".cs", "w")
  f.write("using System.Collections;\n")
  f.write("using System.Collections.Generic;\n")
  f.write("using UnityEngine\n\n")
  f.write("public class " + scriptname + "  : MonoBehavior {\n")
  f.write("\n")
  f.write("}")
#!/usr/bin/python

import os, sys
import getopt
import json
import re
import sets

def main(argv):
    funcs_by_ext_path = "glbinding/Meta_FunctionStringsByExtension.json"
    allowed_file_extensions = ['cpp', 'h']

    src_dir = ''
    list_times = False
    funcs = set()

    # Argument parsing
    try:
        opts, args = getopt.getopt(argv,"hi:n",["src_dir="])
    except getopt.GetoptError:
        print 'list-opengl-extensions.py -i <src_dir> [-n]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'list-opengl-extensions.py -i <src_dir>'
            sys.exit()
        elif opt in ("-i"):
            src_dir = arg
        elif opt in("-n"):
            list_times = True

    # Parse JSON database of funcs by extension
    funcs_by_ext_json = json.loads(open(funcs_by_ext_path, "r").read())
    
    # Make dict to keep track of usages
    func_usages = dict.fromkeys(funcs_by_ext_json.keys(), 0)

    # Simple pattern to find OpenGL calls
    opengl_func_pat = re.compile(r".*gl::gl([^(]*).*")

    for root, subdirs, filenames in os.walk(src_dir):
        # For every file
        for filename in filenames:
            file_ext = os.path.splitext(filename)[1][1:].strip().lower()
            
            # For every file with allowed extension
            if file_ext in allowed_file_extensions:
                filePath = os.path.join(root, filename)
                with open(filePath, 'r') as f:
                    # Find all usages
                    found = re.findall(opengl_func_pat, f.read())
                    
                    # And add them to our set
                    for usage in found:
                        funcs.add("gl" + usage)
    
    # Fill our dict of usages
    for func in funcs:
        for ext in funcs_by_ext_json:
            if func in funcs_by_ext_json[ext]:
                # print "found func", func, "in", funcs_by_ext_json[ext], "ext", ext
                func_usages[ext] += 1

    # List extensions used
    for i in func_usages:
        if func_usages[i] != 0:
            if list_times:
                print "{} used {} times".format(i, func_usages[i])
            else:
                print i

if __name__ == "__main__":
    main(sys.argv[1:])
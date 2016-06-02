#! /urs/bin/env python

import os, sys
import fnmatch




def main():
    dir = sys.argv[1]
    output_str = ""
    with open('images.yaml', 'w') as file:
        for dirname, subdirlist, filelist in os.walk(dir):
            first_part = os.path.basename(dirname).replace(" ", "").lower()
            for fname in filelist:
                # prepare strings for vraiables
                if fname.endswith(('.jpg', '.png')):
                    second_part = os.path.splitext(fname)[0].lower().replace(" ", "").replace("(","").replace(")","").replace(".", "").replace("-","")
                    output_str += '%s_%s:\n  SOURCE: %s\n  OUTPUT: ${IMAGE}\n' % (first_part, second_part, os.path.join(dirname, fname))
        file.write(output_str)



if __name__ == '__main__':
    main()


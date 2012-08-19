#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pypcd8544_piandmore import *

if '--demo' in sys.argv:
  begin(20)
  print "Initialized."
  drawLine(0, 0, 40, 40, True)
  print "Line Drawn."
  display()
  setTextColor(True, False)
  write('Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tem')
  display()
  sys.exit() 
elif '--write' in sys.argv:
  print "Initializing..."
  try:
    contrast = int(sys.argv[sys.argv.index('--write')+1])
  except IndexError:
    print "Usage: %s --write <contrast>\n(Try using values between 20 and 50)" % sys.argv[0]
    sys.exit(1)
  print "Using contrast %d" % contrast
  begin(contrast, False)
  print "Writing"
  string = sys.stdin.read()
  print "Text: '%s'" % string
  setTextColor(True, False)
  write(string)
  display()
  sys.exit(0)
else:
  print "Usage:\n  %s --write <contrast>  Read text from STDIN and write to display\n  %s --demo  Show a demonstration"

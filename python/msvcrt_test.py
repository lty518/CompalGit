##import msvcrt
##print ("Doing a function")
##while True:
##
##    if msvcrt.kbhit():
##        print ("Key pressed: %s" % msvcrt.getch())
import msvcrt

while 1:
  if msvcrt.kbhit(): # Key pressed
    a = ord(msvcrt.getch()) # get first byte of keyscan code
    if a == 0 or a == 224: # is it a function key
      b = ord(msvcrt.getch()) # get next byte of key scan code
      x = a + (b*256) # cook it.
      return x # return cooked scancode
    else:
      return a # else return ascii code

Two simple serial port clock things. They just send strings periodically to the serial port ttyACM0.

The idea is that there is an Arduino on that port listening for strings, which it prints according
to some formatting rules. Lines are separated with asterisks, and lines which start with a colon
are directives for font and colour changes.

The really simple one is `basic_clock.cpp` and is entirely standalone.

The really really simple one is in Python and is actually more powerful, but requires the pyserial
package. Because it's Python we can use all those nice packages...

I've set up a virtualenv to install things into. Remember to do `source venv/bin/activate`.


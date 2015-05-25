This project serves as a file repository and issue tracker for pygame for S60 releases and dependencies.

After installing, try out this simple [snake](http://pygame-symbian-s60.googlecode.com/files/snake.py) game. The PyS60 snake game converted to pygame. Copy the file to \data\pygame\apps\ on your phone and it will show up in launcher's Applications list.

|![http://pygame-symbian-s60.googlecode.com/svn/wiki/snake_on_vista.jpg](http://pygame-symbian-s60.googlecode.com/svn/wiki/snake_on_vista.jpg) |![http://pygame-symbian-s60.googlecode.com/svn/wiki/snake_on_e51.jpg](http://pygame-symbian-s60.googlecode.com/svn/wiki/snake_on_e51.jpg)|
|:---------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| Snake on Vista                                                                                                                               | Snake on Nokia E51                                                                                                                      |


There is also a [PyBox2D physics](http://code.google.com/p/pybox2d/) library package for PyS60 available for [download](http://pygame-symbian-s60.googlecode.com/files/Box2D.sis) and an [example](http://code.google.com/p/pygame-symbian-s60/source/browse/trunk/pybox2d/symbian/box2d_crazyballs.py) using pygame( works on PC as well if you have pygame and PyBox2D installed ).

### Something about the launcher ###

When application is selected the launcher starts a PyS60 background server and closes itself. The server waits for the launcher to close and starts a new pygame process for the selected application. This ensures that the application has a clean pygame environment. If you encounter any problems, the launcher is configured to write standard output to \data\pygame\stdout.txt and applications started with the launcher write to appout.txt.

## Roadmap ##

  1. Use PyS60 application packaging tool
    * Split the pygame runtime and launcher into separate packages
    * Create PyS60 library package
      * Use the package to create the launcher application
      * Launcher should have all the extensions of PyS60 and pygame
  1. Improve startup speed
    * ~~Byte-compiled and zipped pygame library~~
  1. Make tests run on phone and simulator
  1. Make mixer.music work ( audio streaming )
    * Crashes in SDL currently
  1. Tools for creating stand-alone pygame applications
  1. Enable pygame joystick to handle acceleration sensor
  1. Enable pygame camera to use phone's camera(s)
  1. See if at least notes and queries from appuifw work with pygame
  1. Ensure OpenGL ES works with pygame

### Sources ###

The pygame sources are available at the official pygame repository. See: http://www.pygame.org/

This project stores the sources of used external libraries. See the [how\_to\_build.txt](http://www.seul.org/viewcvs/viewcvs.cgi/trunk/symbian/how_to_build.txt?root=PyGame&view=markup) in pygame SVN about how to build the project.

PyBox2D build scripts for Symbian can also be found from SVN.




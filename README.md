# MicroWorld

This is my like... millionth attempt at building a RTS style game.

But really this is a bit of a culmination of about 40 different projects that I've been working on all in various states of completion.

MicroWorld isn't really playable as of right now and is currently just in a bit of a demo state.  Right now it has a functioning menu and I've been working on map generation using Perlin noise as well as building a framework for a JSON driven map saving and loading system.  That's still WIP, though you can play with the generation by going 'new game' and selecting random to get to the current state of the map generation.

Despite it's unfinished state I've decided to go ahead and push it on up to the world of Git.

So what makes this project super awesome and worth backup in version control?  We'll, it's probably my most advanced project as far as messing around with more advanced topics, the Grid class is a good example, utilizing a bunch of the data model methods and all that wizardry.

It also has a fully event driven navigation and interaction system.  This means everything is driven by a bind system which allows me to bind SDL events to callable methods.  Neato.  Well except when pygame_gui broke my events because PyGame had a bug with USER_EVENT, but that's been corrected as of 2.0.12dev.

The scene design and implementation is pretty streamlined as well.  You'll be able to tell that it's got a lot going on by the 8 current scenes that will expand as I add to this project.  Each part of the program is technically a self-contained mini program in and of itself, though almost all of it is dependent on the game reference.

I've also successfully implemented screen resolution changes via the GUI, meaning you can change the screen size inside the game and it can be applied and take effect without restarting the game.

This is also the first project where I've implemented the pygame_gui by MyreMylar for more then simple buttons.  It's a very well written and implemented library, so I'd highly recommend anyone looking to play around with PyGame give it a go even if it did break my event system for a bit.

There is a bit of redundant 'testing' code still in this project but I will be cleaning that up as things progress.

### Requirements

Python 3.6+  (developed on 3.8, but should be okay with 3.6/7)
Pygame 2.0+  (developed on 2.0.10dev)
Noise https://github.com/caseman/noise
pygame_gui https://github.com/MyreMylar/pygame_gui

### On The Burner
- [ ] Map Generation
- [ ] Map Editor
- [ ] Some form of playable game


import sys
import os
#import chipmunk
#from chipmunk import *
#print dir( chipmunk )


import os, sys
import pygame
from pygame import constants
from pygame.locals import *
from Box2D import *

INFINITY = 1e1000
BLACK    = 0x0
THISDIR = os.path.dirname( __file__ )
DISPLAY_SIZE = 240, 320

class StopDemoException( Exception ): pass

def check_exit_event( event ):
    if event.type == pygame.KEYDOWN:
        # K_ESCAPE = Right softkey
        if event.type == pygame.KEYDOWN \
        and event.key == constants.K_ESCAPE:
            raise StopDemoException( "User exited" )
    elif event.type == pygame.QUIT:
        raise StopDemoException( "User exited" )
    return None

class PhysicsWorld:
    targetFPS = 40
    timeStep  = 1000 / targetFPS
    iterations = 5
    bodies = []
    count = 0
    worldAABB = None
    world     = None
    groundBodyDef = None
    groundShapeDef = None

    def __init__(self):

        # Step 1: Create Physics World Boundaries
        self.worldAABB = b2AABB()
        self.worldAABB.lowerBound = b2Vec2(-0.0, -0.0);
        self.worldAABB.upperBound = b2Vec2(24.0, 32.0);

        # Step 2: Create Physics World with Gravity
        gravity = b2Vec2(0.0, 10.0);
        doSleep = True
        self.world = b2World(self.worldAABB, gravity, doSleep);

        def make_rect(x,y, w, h):
            self.groundBodyDef = b2BodyDef();
            self.groundBodyDef.position = b2Vec2(x,y);
            self.groundBody = self.world.CreateBody(self.groundBodyDef);

            self.groundShapeDef = b2PolygonDef();
            self.groundShapeDef.SetAsBox(w, h);
            self.groundBody.CreateShape(self.groundShapeDef);
        # Make world borders
        # Ground
        make_rect( 0.0, 32.0,  24,  0.05 )
        # Top
        make_rect( 0.0,  0.0,  24,  0.05 )
        # Left
        make_rect( 0.0,  0.0, 0.1, 32.0 )
        # Right
        make_rect( 24.0, 0.0, 0.1, 32.0 )



    def addBall(self):
        # Create Dynamic Body
        bodyDef = b2BodyDef();
        bodyDef.position = ( 0.2+self.count * 0.6, 1.8);
        b = self.world.CreateBody(bodyDef);
        self.bodies.append( b )

        # Create Shape with Properties
        circle = b2CircleDef()
        circle.radius      = 0.2 + 0.1 * self.count
        circle.density     = 1
        circle.restitution = 1.1
        circle.mass = 0.1 + 0.1 * self.count

        # Assign shape to Body
        self.bodies[self.count].CreateShape(circle);
        self.bodies[self.count].SetMassFromShapes();

        # Increase Counter
        self.count += 1;

def main():

    # Initialize and setup screen
    pygame.init()

    world = PhysicsWorld()

    for x in xrange(20):
        world.addBall()

    if os.name == "e32":
        size = pygame.display.list_modes()[0]
    else:
        size =  DISPLAY_SIZE

    screen = pygame.display.set_mode(size)
    clock  = pygame.time.Clock()
    tics   = pygame.time.get_ticks()
    colors = [ 0xFF0000, 0x00FF00, 0xFF00FF, 0x00FF00, 0xFFFF00, 0x00FFFF ]

    from pygame import draw
    while 1:

        clock.tick(30)
        for event in pygame.event.get():
            check_exit_event( event )

        # Clear screen
        screen.fill(BLACK)

        velocityIterations = 10
        positionIterations = 8

        timeStep = 2. / 60.
        world.world.SetWarmStarting(True)
    	world.world.SetContinuousPhysics(True)
        world.world.Step(timeStep, 10, positionIterations)
        world.world.Validate()

        i = 0
        for b in world.bodies:
            x, y = b.position.tuple()
            r = b.GetShapeList()[0].radius
            draw.circle( screen, colors[ i % len(colors)], ((x)*10, (y) * 10), r * 10, 0 )
            i += 1

        pygame.display.flip()
        clock.tick(30)

        tics = pygame.time.get_ticks()


    #for x in xrange(100):
        #print ballShape.body.p.x, ballShape.body.p.y


if __name__ == '__main__':
    try:
        main()
    except StopDemoException:
        pass

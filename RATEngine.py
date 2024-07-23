# RATEngine V0.6 build 1 2024

from math import sin, cos, radians
import pygame
from RATRender import *
from RAThematics import *
from RATriangles import *
from RATEntities import *

pygame.init()
pygame.display.set_caption("RATEngine V0.6b12024")
pygame.font.init()
FONT = pygame.font.SysFont('Calibri', 18)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

#ENGINE GLOBALS
GAME_RUNNING = True
CANVAS_D = 7
WIDTH = 100*CANVAS_D
HEIGHT = 75*CANVAS_D
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
NEAR_Z = -0.25 #<- smaller negative means smaller near-clipping distance
FAR_Z = 0.01 #<- lower number means higher view distance
FOG_DEPTH = 100.0
USER_FOV = 110.0 #<- User-controlled FOV
FOV = radians(90.0 - (USER_FOV/2.0))
FOV_sin = sin(FOV)
FOV_cos = cos(FOV)
CANVAS_W = WIDTH // CANVAS_D
CANVAS_H = HEIGHT // CANVAS_D
CANVAS_WH = CANVAS_W >> 1
CANVAS_HH = CANVAS_H >> 1
CANVAS_M = CANVAS_W * CANVAS_H
VIEW_W = 1.0
VIEW_H = 1.0
if WIDTH > HEIGHT:
  VIEW_H = WIDTH/HEIGHT
else:
  VIEW_W = HEIGHT/WIDTH
PER_W_MUL = CANVAS_W * FOV_sin * VIEW_W
PER_H_MUL = CANVAS_H * FOV_sin * VIEW_H
COLOR_BLACK = pygame.Color(0,0,0)
SKY_COLOR = pygame.Color(15,20,45)
DEPTH_BUFFER = [FAR_Z]*CANVAS_M
COLOR_BUFFER = []
for _ in range(CANVAS_M):
  COLOR_BUFFER.append(pygame.Color(SKY_COLOR))
N_PLANE = (     0.0,0.0,    1.0)
L_PLANE = ( FOV_sin,0.0,FOV_cos)
R_PLANE = (-FOV_sin,0.0,FOV_cos)
B_PLANE = ( 0.0,FOV_sin,FOV_cos)
T_PLANE = (0.0,-FOV_sin,FOV_cos)
KEYS = [False]*512

#Player controlled camera
#This dict is *technically* an object but don't expect every object method to work correctly
CAMERA = {
  "scale": identity(),
  "pitch": identity(),
  "yaw": identity(),
  "roll": identity(),
  "translation": identity(),
  "rotation": identity(),
  "transform": identity()
}
translateObject(CAMERA, 0.0, 16.0, 0.0)

## MAPPING AREA ##

ONGAH = loadTexture("textures/ongah.jpg")
EXBRL = loadTexture("textures/barrel.jpg")
ASPLT = loadTexture("textures/asphalt.jpg")
BCKRD = loadTexture("textures/brick_red.png")
BKRDW = loadTexture("textures/brick_window_red.png")
BCKBR = loadTexture("textures/brick_brown.png")
BKBRW = loadTexture("textures/brick_window_brown.png")
BCKHZ = loadTexture("textures/brick_hazel.png")
BKHZW = loadTexture("textures/brick_window_hazel.png")
BCKGR = loadTexture("textures/brick_gray.png")
BKGRW = loadTexture("textures/brick_window_gray.png")
CHNLK = loadTexture("textures/chainlink.png")
WDBOX = loadTexture("textures/box.jpg")
CRGTD = loadTexture("textures/corrugated.jpg")
LDDER = loadTexture("textures/ladder.png")
TRASH = loadTexture("textures/trash.png")

CAT_SPRITE = Plane(  0.0,  5.0, 60.0, 270.0,  0.0, 0.0,  5.0, 1.0,   5.0, ONGAH, 1.000, 1.0, 120.0, True, False)

SCENE_OBJECTS = [
  CAT_SPRITE,
  Plane(  0.0,  0.0,  0.0,   0.0,   0.0, 0.0, 32.0, 1.0, 64.0, ASPLT, 4.000, 8.0, 120.0, True, False),
  Plane(-32.0, 16.0,-32.0, -90.0, -90.0, 0.0, 32.0, 1.0, 16.0, BCKRD, 2.000, 1.0, 120.0, True, False),
  Plane(-32.0, 64.0,-32.0, -90.0, -90.0, 0.0, 32.0, 1.0, 32.0, BKRDW, 2.000, 2.0, 120.0, True, False),
  Plane(-28.0, 16.0, 32.0, -90.0, -90.0, 0.0, 32.0, 1.0, 16.0, BCKBR, 2.000, 1.0, 120.0, True, False),
  Plane(-28.0, 64.0, 32.0, -90.0, -90.0, 0.0, 32.0, 1.0, 32.0, BKBRW, 2.000, 2.0, 120.0, True, False),
  Plane(-30.0, 48.0,  0.0, -90.0,   0.0, 0.0,  2.0, 1.0, 48.0, BCKBR, 0.125, 2.0, 120.0, True, False),
  Plane( 32.0, 16.0, 32.0, -90.0,  90.0, 0.0, 32.0, 1.0, 16.0, BCKGR, 2.000, 1.0, 120.0, True, False),
  Plane( 32.0, 64.0, 32.0, -90.0,  90.0, 0.0, 32.0, 1.0, 32.0, BKGRW, 2.000, 2.0, 120.0, True, False),
  Plane( 28.0, 16.0,-32.0, -90.0,  90.0, 0.0, 32.0, 1.0, 16.0, BCKHZ, 2.000, 1.0, 120.0, True, False),
  Plane( 28.0, 64.0,-32.0, -90.0,  90.0, 0.0, 32.0, 1.0, 32.0, BKHZW, 2.000, 2.0, 120.0, True, False),
  Plane( 30.0, 48.0,  0.0,  90.0,   0.0, 0.0,  2.0, 1.0, 48.0, BCKHZ, 0.125, 2.0, 120.0, True, False),
  Plane(  0.0, 48.0, 64.0, -90.0,   0.0, 0.0, 32.0, 1.0, 48.0, BCKBR, 2.000, 2.0, 120.0, True, False),  
  Plane(  0.0, 16.0,-60.0,  90.0,   0.0, 0.0, 32.0, 1.0, 16.0, CHNLK, 4.000, 2.0, 120.0, True, False),
  Plane(-12.0,  0.5,-48.0,   0.0,  20.0, 0.0,  8.0, 1.0,  6.0, TRASH, 1.000, 1.0, 120.0, True, False),
  Plane(-14.0,  0.5,-22.0,   0.0, 150.0, 0.0,  8.0, 1.0,  6.0, TRASH, 1.000, 1.0, 120.0, True, False),
  Plane( 16.0,  0.5, 46.0,   0.0,-120.0, 0.0, 10.0, 1.0,  8.0, TRASH, 1.000, 1.0, 120.0, True, False),
  Plane( 15.0, 22.0,-36.0, -90.0,  90.0, 0.0,  4.0, 1.0, 22.0, LDDER, 1.000, 3.0, 120.0, True, False),
  Cylinder( 24.0,  6.0,-14.0,   0.0,   0.0, 0.0,  4.0, 6.0,  4.0, EXBRL, 1.000, 1.0, 120.0, True, False, div=8),
  Cylinder( 22.0,  6.0,-24.0,   0.0,   0.0, 0.0,  4.0, 6.0,  4.0, EXBRL, 1.000, 1.0, 120.0, True, False, div=8), 
  Cube( 22.0, 40.0,-32.0,   0.0,   0.0, 0.0,  6.0, 4.0,  8.0, CRGTD, 1.000, 1.0, 120.0, True, False),
  Cube( 22.0, 64.0,-32.0,   0.0,   0.0, 0.0,  6.0, 4.0,  8.0, CRGTD, 1.000, 1.0, 120.0, True, False),
  Cube(-12.0,  8.0, 48.0,   0.0,  45.0, 0.0,  8.0, 8.0,  8.0, WDBOX, 1.000, 1.0, 120.0, True, False),
  Cube( 10.0,  6.0, 50.0,   0.0,  30.0, 0.0,  6.0, 6.0,  6.0, WDBOX, 1.000, 1.0, 120.0, True, False),
  Cube(-14.0,  4.0,-54.0,   0.0, -25.0, 0.0,  4.0, 4.0,  4.0, WDBOX, 1.000, 1.0, 120.0, True, False)
]

SCENE_LIGHTS = [
  SpotLight(0.0,0.0,0.0,0.0,0.0,-1.0,30.0,10.0,30.0),
  #PointLight(0.0,10.0,40.0,10.0),
]

##################

SCENE_TRIANGLES = [] #<- Used to keep track of all triangles that will be rendered

while GAME_RUNNING:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      GAME_RUNNING = False
    if event.type == pygame.KEYDOWN:
      KEYS[event.scancode] = True
    if event.type == pygame.KEYUP:
      KEYS[event.scancode] = False
  
  #User input section
  if KEYS[26]:
    translateObjectDirection(CAMERA, 'f', CAMERA['yaw'], 1.0)
  if KEYS[22]:
    translateObjectDirection(CAMERA, 'f', CAMERA['yaw'],-1.0)
  if KEYS[4]:
    translateObjectDirection(CAMERA, 'r', CAMERA['yaw'],-1.0)
  if KEYS[7]:
    translateObjectDirection(CAMERA, 'r', CAMERA['yaw'], 1.0)
  if KEYS[41]:
    GAME_RUNNING = False

  mousePos = pygame.mouse.get_rel()
  rotateObject(CAMERA, mousePos[1]/4, mousePos[0]/4, 0.0)
  applyTransforms(CAMERA)

  pygame.mouse.set_pos(WIDTH//2, HEIGHT//2)

  CAM_TRANSF_INV = getInverseCameraTransform(CAMERA)
  
  CAT_SPRITE['yaw'] = CAMERA['yaw']
  applyTransforms(CAT_SPRITE)

  setPositionToObject(SCENE_LIGHTS[0], CAMERA)
  setNormalToDirection(SCENE_LIGHTS[0], CAMERA, 'f')

  #Loop through all objects in the SCENE_OBJECTS list and perform the following steps:
  for object in SCENE_OBJECTS:
    #For all objects with parents we need to determine to complete transform which includes not only the child, but all of its parents
    parentRotation = object['rotation']
    parentTransform = object['transform']
    currentObject = object
    while currentObject['parent'] is not None:
      parentRotation = matmul(parentRotation, currentObject['parent']['rotation'])
      parentTransform = matmul3(parentTransform, currentObject['parent']['rotation'], currentObject['parent']['translation'])
      currentObject = currentObject['parent'] 
    
    #This represents the x, y, z values of the entire object which then gets transformed in reference to the camera
    positionTransform = [parentTransform[3], parentTransform[7], parentTransform[11]]
    vertran(positionTransform, CAM_TRANSF_INV)
    
    #Before clipping triangles, we can determine if an entire object even needs to be clipped by testing
    #its bound against the clipping planes
    nearPlaneTest = dot(N_PLANE, positionTransform) + NEAR_Z > object['bound']
    leftPlaneTest = dot(L_PLANE, positionTransform) + NEAR_Z > object['bound']
    rightPlaneTest = dot(R_PLANE, positionTransform) + NEAR_Z > object['bound']
    topPlaneTest = dot(T_PLANE, positionTransform) + NEAR_Z > object['bound']
    bottomPlaneTest = dot(B_PLANE, positionTransform) + NEAR_Z > object['bound']
    objectWithinPlanes = nearPlaneTest and leftPlaneTest and rightPlaneTest and topPlaneTest and bottomPlaneTest

    #If the object itself is beyond its own render distance then don't bother to render it
    if magnitude(positionTransform) < object['renderDistance']:
      #But it isn't then iterate through each of its triangles and process then accordingly:
      for triangle in object['triangles']:
        #Create a copy of each triangle and transform it by worldspace and then cameraspace (also transform normals by rotation)
        tCopy = triangle.copy()
        totalTransform = matmul(parentTransform, CAM_TRANSF_INV)
        transformTriangle(tCopy, totalTransform, parentRotation)
        #Test if the triangle is facing the camera or else cull it 
        #(the cull test method requires that the triangle is already transformed by the cameraspace)
        if triangleFacingCamera(tCopy):
          #If the triangle is not culled then calculate its distance to the camera and save it for sorting
          tCopy['magnitude'] = magnitude(center(tCopy))
          #If the entire object was within each plane then just add this triangle
          if objectWithinPlanes:
            SCENE_TRIANGLES.append(tCopy)
          else:
            #If not then clip the triangle against each plane and return the new triangles
            trianglesToClip = [tCopy]
            clipTriangles(trianglesToClip, N_PLANE, NEAR_Z)
            clipTriangles(trianglesToClip, L_PLANE, NEAR_Z)
            clipTriangles(trianglesToClip, R_PLANE, NEAR_Z)
            clipTriangles(trianglesToClip, T_PLANE, NEAR_Z)
            clipTriangles(trianglesToClip, B_PLANE, NEAR_Z)
            for fragment in trianglesToClip:
              SCENE_TRIANGLES.append(fragment)
  #Sort the triangles first by translucency and then by distance
  #This makes all translucent triangles render last which renders them correctly but hurts performance
  SCENE_TRIANGLES.sort(key=lambda t: (t['object']['translucent'], t['magnitude']))

  #Iterate through the processed list of triangles, transform them by the projection inputs, then finally render them with lighting and textures
  for triangle in SCENE_TRIANGLES:
    projectTriangle(triangle, CANVAS_WH, CANVAS_HH, PER_W_MUL, PER_H_MUL)
    renderTriangleTextured(
      triangle, CANVAS_W, CANVAS_WH, PER_W_MUL, CANVAS_H, CANVAS_HH, PER_H_MUL, CANVAS_D, 
      DEPTH_BUFFER, COLOR_BUFFER, COLOR_BLACK, SKY_COLOR, FOG_DEPTH, FAR_Z, SCENE_LIGHTS, CAMERA['transform'], SCREEN
    )
    #wireframe(getTriangleA(triangle), getTriangleB(triangle), getTriangleC(triangle), CANVAS_D, SCREEN)
    
  FPS_TEXT = FONT.render(str(clock.get_fps()), False, (255, 255, 255))
  SCREEN.blit(FPS_TEXT, (0,0))

  pygame.display.flip() 

  SCENE_TRIANGLES.clear() #<- empty the triangles out for the next frame
  DEPTH_BUFFER[:] = [FAR_Z]*CANVAS_M #<- reset the depth buffer for the next frame
  for z in range(CANVAS_M): #<- reset the background color for the next frame
    COLOR_BUFFER[z].update(SKY_COLOR)
  SCREEN.fill(SKY_COLOR)

  clock.tick(30) #<- frame limit value

pygame.quit()


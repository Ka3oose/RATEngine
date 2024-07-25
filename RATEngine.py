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
CANVAS_D = 6
WIDTH = 96*CANVAS_D
HEIGHT = 72*CANVAS_D
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
  Plane( 15.0, 22.0,-36.0, -90.0,  90.0, 0.0,  4.0, 1.0, 22.0, LDDER, 1.000, 3.0, 120.0, False, False),
  Cylinder(24.0,6.0,-14.0,   0.0,   0.0, 0.0,  4.0, 6.0,  4.0, EXBRL, 1.000, 1.0, 120.0, True, False, div=8),
  Cylinder(22.0,6.0,-24.0,   0.0,   0.0, 0.0,  4.0, 6.0,  4.0, EXBRL, 1.000, 1.0, 120.0, True, False, div=8), 
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
    objectToCamX = parentTransform[3] - CAMERA['transform'][3]
    objectToCamY = parentTransform[7] - CAMERA['transform'][7]
    objectToCamZ = parentTransform[11] - CAMERA['transform'][11]
    objectToCamMagnitude = sqrt(objectToCamX*objectToCamX + objectToCamY*objectToCamY + objectToCamZ*objectToCamZ)

    #If the object itself is beyond its own render distance then don't bother to render it
    if objectToCamMagnitude < object['renderDistance']:
      #But it isn't then iterate through each of its triangles and process then accordingly:
      for triangle in object['triangles']:
        #Create a copy of each triangle and transform it by worldspace and then cameraspace (also transform normals by rotation)
        triCopy = triangle.copy()
        totalTransform = matmul(parentTransform, CAM_TRANSF_INV)
        #Transform the triangle's vertex positions by the total transform (all parent transforms, self, and camera)
        #Transform the triangle's vertex normals by all parent transforms (used for lighting so must remain world space)
        tax, tay, taz = triCopy['ax'], triCopy['ay'], triCopy['az']
        tbx, tby, tbz = triCopy['bx'], triCopy['by'], triCopy['bz']
        tcx, tcy, tcz = triCopy['cx'], triCopy['cy'], triCopy['cz']
        tap, taq, tar = triCopy['ap'], triCopy['aq'], triCopy['ar']
        tbp, tbq, tbr = triCopy['bp'], triCopy['bq'], triCopy['br']
        tcp, tcq, tcr = triCopy['cp'], triCopy['cq'], triCopy['cr']
        triCopy['ax'] = tax*totalTransform[0]+tay*totalTransform[1]+taz*totalTransform[ 2]+totalTransform[ 3]
        triCopy['ay'] = tax*totalTransform[4]+tay*totalTransform[5]+taz*totalTransform[ 6]+totalTransform[ 7]
        triCopy['az'] = tax*totalTransform[8]+tay*totalTransform[9]+taz*totalTransform[10]+totalTransform[11]
        triCopy['bx'] = tbx*totalTransform[0]+tby*totalTransform[1]+tbz*totalTransform[ 2]+totalTransform[ 3]
        triCopy['by'] = tbx*totalTransform[4]+tby*totalTransform[5]+tbz*totalTransform[ 6]+totalTransform[ 7]
        triCopy['bz'] = tbx*totalTransform[8]+tby*totalTransform[9]+tbz*totalTransform[10]+totalTransform[11]
        triCopy['cx'] = tcx*totalTransform[0]+tcy*totalTransform[1]+tcz*totalTransform[ 2]+totalTransform[ 3]
        triCopy['cy'] = tcx*totalTransform[4]+tcy*totalTransform[5]+tcz*totalTransform[ 6]+totalTransform[ 7]
        triCopy['cz'] = tcx*totalTransform[8]+tcy*totalTransform[9]+tcz*totalTransform[10]+totalTransform[11]
        triCopy['ap'] = tap*parentRotation[0]+taq*parentRotation[1]+tar*parentRotation[ 2]+parentRotation[ 3]
        triCopy['aq'] = tap*parentRotation[4]+taq*parentRotation[5]+tar*parentRotation[ 6]+parentRotation[ 7]
        triCopy['ar'] = tap*parentRotation[8]+taq*parentRotation[9]+tar*parentRotation[10]+parentRotation[11]
        triCopy['bp'] = tbp*parentRotation[0]+tbq*parentRotation[1]+tbr*parentRotation[ 2]+parentRotation[ 3]
        triCopy['bq'] = tbp*parentRotation[4]+tbq*parentRotation[5]+tbr*parentRotation[ 6]+parentRotation[ 7]
        triCopy['br'] = tbp*parentRotation[8]+tbq*parentRotation[9]+tbr*parentRotation[10]+parentRotation[11]
        triCopy['cp'] = tcp*parentRotation[0]+tcq*parentRotation[1]+tcr*parentRotation[ 2]+parentRotation[ 3]
        triCopy['cq'] = tcp*parentRotation[4]+tcq*parentRotation[5]+tcr*parentRotation[ 6]+parentRotation[ 7]
        triCopy['cr'] = tcp*parentRotation[8]+tcq*parentRotation[9]+tcr*parentRotation[10]+parentRotation[11]
        #Test if the triangle is facing the camera or else cull it 
        #(the cull test method requires that the triangle is already transformed by the cameraspace)
        #This method is an alternative form of dot(cross(b-a, c-a), a) which finds the cross product of two
        #vectors of the triangle's edges and compares its angle to the angle of the camera to one of the edges
        b_a_x = triCopy['bx'] - triCopy['ax']
        b_a_y = triCopy['by'] - triCopy['ay']
        b_a_z = triCopy['bz'] - triCopy['az']
        c_a_x = triCopy['cx'] - triCopy['ax']
        c_a_y = triCopy['cy'] - triCopy['ay']
        c_a_z = triCopy['cz'] - triCopy['az']
        c00 = triCopy['ax'] * b_a_y * c_a_z
        c01 = triCopy['ax'] * c_a_y * b_a_z
        c02 = c_a_x * triCopy['ay'] * b_a_z
        c03 = b_a_x * triCopy['ay'] * c_a_z
        c04 = b_a_x * c_a_y * triCopy['az']
        c05 = c_a_x * b_a_y * triCopy['az']
        if (c00 - c01 + c02 - c03 + c04 - c05) > 0.0:
          #If the triangle is not culled then calculate its distance to the camera and save it for sorting
          #Distances are determined from the center of the triangle which is an average of all of its x, y, and z positions
          centerX = (triCopy['ax'] + triCopy['bx'] + triCopy['cx']) / 3.0
          centerY = (triCopy['ay'] + triCopy['by'] + triCopy['cy']) / 3.0
          centerZ = (triCopy['az'] + triCopy['bz'] + triCopy['cz']) / 3.0
          triCopy['magnitude'] = sqrt(centerX*centerX + centerY*centerY + centerZ*centerZ)
          #Clip the triangle against each plane
          trianglesToClip = [triCopy]
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

  for triangle in SCENE_TRIANGLES:
    #Transform the triangle vertex position values to screen space using special inputs that determine FOV and offsetting
    triangle['az'] = 1/triangle['az']
    triangle['bz'] = 1/triangle['bz']
    triangle['cz'] = 1/triangle['cz']
    triangle['ax'] = CANVAS_WH + (triangle['ax'] * triangle['az']) * PER_W_MUL
    triangle['ay'] = CANVAS_HH - (triangle['ay'] * triangle['az']) * PER_H_MUL
    triangle['au'] *= triangle['az']
    triangle['av'] *= triangle['az']
    triangle['bx'] = CANVAS_WH + (triangle['bx'] * triangle['bz']) * PER_W_MUL
    triangle['by'] = CANVAS_HH - (triangle['by'] * triangle['bz']) * PER_H_MUL
    triangle['bu'] *= triangle['bz']
    triangle['bv'] *= triangle['bz']
    triangle['cx'] = CANVAS_WH + (triangle['cx'] * triangle['cz']) * PER_W_MUL
    triangle['cy'] = CANVAS_HH - (triangle['cy'] * triangle['cz']) * PER_H_MUL
    triangle['cu'] *= triangle['cz']
    triangle['cv'] *= triangle['cz']
    
    renderTriangleTextured(
      triangle, CANVAS_W, CANVAS_WH, PER_W_MUL, CANVAS_H, CANVAS_HH, PER_H_MUL, CANVAS_D, DEPTH_BUFFER, 
      COLOR_BUFFER, COLOR_BLACK, SKY_COLOR, FOG_DEPTH, FAR_Z, SCENE_LIGHTS, CAMERA['transform'], SCREEN
    )
    #wireframe(getTriangleA(triangle), getTriangleB(triangle), gettriCopy(triangle), CANVAS_D, SCREEN)
    
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


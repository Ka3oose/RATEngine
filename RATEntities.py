import pygame
from RAThematics import *
from RATriangles import *
from math import sqrt, cos, sin
from math import pi as PI

def Light(x, y, z, p, q, r, a, e, b, type):
  return {
    "position": [x, y, z],
    "normal": [p, q, r],
    "brightness": b,
    "angle": a,
    "exponent": e,
    "type": type
    }

def AmbientLight(b):
  return Light(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, b, 0)

def DirectionLight(p, q, r, b):
  return Light(0.0, 0.0, 0.0, p, q, r, 0.0, 0.0, b, 1)

def PointLight(x, y, z, b):
  return Light(x, y, z, 0.0, 0.0, 0.0, 0.0, 0.0, b, 2)

def SpotLight(x, y, z, p, q, r, a, e, b):
  return Light(x, y, z, p, q, r, a, e, b, 3)

def loadTexture(filepath):
  imageFile = pygame.image.load(filepath).convert_alpha()
  pixels = []
  for y in range(imageFile.get_height()):
    for x in range(imageFile.get_width()):
      pixels.append(imageFile.get_at((x, y)))
  texture = {
    "width": imageFile.get_width(),
    "height": imageFile.get_height(),
    "image": tuple(pixels)
  }
  return texture

MSGTX = {
  "width": 2,
  "height": 2,
  "image": (pygame.Color(208,48,240),pygame.Color(0,0,0),pygame.Color(0,0,0),pygame.Color(208,48,240))
}

def Model(tris, x=0.0, y=0.0, z=0.0, pi=0.0, ya=0.0, ro=0.0, sx=1.0, sy=1.0, sz=1.0, 
          texture=MSGTX, tsx=1.0, tsy=1.0, rdist=100.0, sh=False, trans=True):
  constructedModel = {
    "scale": identity(),
    "pitch": identity(),
    "yaw": identity(),
    "roll": identity(),
    "translation": identity(),
    "rotation": identity(),
    "transform": identity(),
    "parent": None,
    "tScaleX": tsx,
    "tScaleY": tsy,
    "renderDistance": rdist,
    "shaded": sh,
    "translucent": trans,
    "triangles": None,
    "texture": texture
  }
  scaleObject(constructedModel, sx, sy, sz)
  rotateObject(constructedModel, pi, ya, ro)
  translateObject(constructedModel, x, y, z)
  for triangle in tris:
    triangle['object'] = constructedModel
  constructedModel['triangles'] = tris

  return constructedModel

def OBJ(filepath, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans):
  triangles = []
  file = open(filepath, "r")
  vList = [0.0]
  nList = [0.0]
  tList = [0.0]
  for line in file:
    lineSplit = line.split()
    if lineSplit[0] == 'v':
      vList.append([float(lineSplit[1]), float(lineSplit[2]), float(lineSplit[3]), 1.0])
    elif lineSplit[0] == 'vn':
      nList.append([float(lineSplit[1]), float(lineSplit[2]), float(lineSplit[3])])
    elif lineSplit[0] == 'vt':
      tList.append([float(lineSplit[1]), float(lineSplit[2])])
    elif lineSplit[0] == 'f':
      faceA = lineSplit[1].split('/')
      faceB = lineSplit[2].split('/')
      faceC = lineSplit[3].split('/')
      fAvert = int(faceA[0])
      fAtext = int(faceA[1])
      fAnorm = int(faceA[2])
      fBvert = int(faceB[0])
      fBtext = int(faceB[1])
      fBnorm = int(faceB[2])
      fCvert = int(faceC[0])
      fCtext = int(faceC[1])
      fCnorm = int(faceC[2])
      triangles.append(
        createTriangle(
          vList[fAvert][0], vList[fAvert][1], vList[fAvert][2], tList[fAtext][0], tList[fAtext][1], nList[fAnorm][0], nList[fAnorm][1], nList[fAnorm][2],
          vList[fCvert][0], vList[fCvert][1], vList[fCvert][2], tList[fCtext][0], tList[fCtext][1], nList[fCnorm][0], nList[fCnorm][1], nList[fCnorm][2],
          vList[fBvert][0], vList[fBvert][1], vList[fBvert][2], tList[fBtext][0], tList[fBtext][1], nList[fBnorm][0], nList[fBnorm][1], nList[fBnorm][2]
        )
      )
  file.close()
  return Model(triangles, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans)  

def Cylinder(x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans, div=6):
  DIV = (PI*2.0) / div
  triangles = []
  for i in range(div):
    triangles.append(createTriangle(
        cos(i * DIV), -1.0, sin(i * DIV), 0.0,0.0, cos(i * DIV), -1.0, sin(i * DIV),
        0.0,-1.0, 0.0, 0.0,0.0, 0.0, -1.0, 0.0,
        cos((i+1) * DIV),-1.0, sin((i+1) * DIV), 0.0,0.0,cos((i+1) * DIV), -1.0, sin((i+1) * DIV)
      ))
    triangles.append(createTriangle(
        cos(i * DIV),-1.0, sin(i * DIV), i/div,1.0, cos(i * DIV), 0.0, sin(i * DIV),
        cos((i+1) * DIV), 1.0, sin((i+1) * DIV), (i+1)/div,0.0,cos((i+1) * DIV),  0.0, sin((i+1) * DIV),
        cos(i * DIV), 1.0, sin(i * DIV), i/div,0.0, cos(i * DIV),  0.0, sin(i * DIV)
      ))
    triangles.append(createTriangle(
        cos((i+1) * DIV), 1.0, sin((i+1) * DIV), (i+1)/div,0.0,cos((i+1) * DIV),  0.0, sin((i+1) * DIV),
        cos(i * DIV),-1.0, sin(i * DIV), i/div,1.0, cos(i * DIV), 0.0, sin(i * DIV),
        cos((i+1) * DIV),-1.0, sin((i+1) * DIV), (i+1)/div,1.0,cos((i+1) * DIV), 0.0, sin((i+1) * DIV)
      ))
    triangles.append(createTriangle(
        cos(i * DIV), 1.0, sin(i * DIV), 0.0,0.0, cos(i * DIV),  1.0, sin(i * DIV),
        cos((i+1) * DIV), 1.0, sin((i+1) * DIV), 0.0,0.0,cos((i+1) * DIV),  1.0, sin((i+1) * DIV),
        0.0, 1.0, 0.0, 0.0,0.0, 0.0,  1.0, 0.0
      ))
  return Model(triangles, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans)

def Cube(x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans):
  triangles = [
    createTriangle(-1.0,-1.0,-1.0,0.0,0.0,0.0,-1.0,0.0,-1.0,-1.0, 1.0,0.0,1.0,0.0,-1.0,0.0, 1.0,-1.0, 1.0,1.0,1.0,0.0,-1.0,0.0),
    createTriangle( 1.0,-1.0, 1.0,1.0,1.0,0.0,-1.0,0.0, 1.0,-1.0,-1.0,1.0,0.0,0.0,-1.0,0.0,-1.0,-1.0,-1.0,0.0,0.0,0.0,-1.0,0.0),
    createTriangle(-1.0, 1.0,-1.0,0.0,1.0,0.0, 1.0,0.0, 1.0, 1.0, 1.0,1.0,0.0,0.0, 1.0,0.0,-1.0, 1.0, 1.0,0.0,0.0,0.0, 1.0,0.0),
    createTriangle( 1.0, 1.0, 1.0,1.0,0.0,0.0, 1.0,0.0,-1.0, 1.0,-1.0,0.0,1.0,0.0, 1.0,0.0, 1.0, 1.0,-1.0,1.0,1.0,0.0, 1.0,0.0),
    createTriangle(-1.0,-1.0,-1.0,1.0,1.0,-1.0,0.0,0.0,-1.0, 1.0, 1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,-1.0, 1.0,0.0,1.0,-1.0,0.0,0.0),
    createTriangle(-1.0, 1.0, 1.0,0.0,0.0,-1.0,0.0,0.0,-1.0,-1.0,-1.0,1.0,1.0,-1.0,0.0,0.0,-1.0, 1.0,-1.0,1.0,0.0,-1.0,0.0,0.0),
    createTriangle( 1.0,-1.0,-1.0,0.0,1.0, 1.0,0.0,0.0, 1.0,-1.0, 1.0,1.0,1.0, 1.0,0.0,0.0, 1.0, 1.0, 1.0,1.0,0.0, 1.0,0.0,0.0),
    createTriangle( 1.0, 1.0, 1.0,1.0,0.0, 1.0,0.0,0.0, 1.0, 1.0,-1.0,0.0,0.0, 1.0,0.0,0.0, 1.0,-1.0,-1.0,0.0,1.0, 1.0,0.0,0.0),
    createTriangle(-1.0,-1.0, 1.0,1.0,1.0,0.0,0.0, 1.0, 1.0, 1.0, 1.0,0.0,0.0,0.0,0.0, 1.0, 1.0,-1.0, 1.0,0.0,1.0,0.0,0.0, 1.0),
    createTriangle( 1.0, 1.0, 1.0,0.0,0.0,0.0,0.0, 1.0,-1.0,-1.0, 1.0,1.0,1.0,0.0,0.0, 1.0,-1.0, 1.0, 1.0,1.0,0.0,0.0,0.0, 1.0),
    createTriangle(-1.0,-1.0,-1.0,0.0,1.0,0.0,0.0,-1.0, 1.0,-1.0,-1.0,1.0,1.0,0.0,0.0,-1.0, 1.0, 1.0,-1.0,1.0,0.0,0.0,0.0,-1.0),
    createTriangle( 1.0, 1.0,-1.0,1.0,0.0,0.0,0.0,-1.0,-1.0, 1.0,-1.0,0.0,0.0,0.0,0.0,-1.0,-1.0,-1.0,-1.0,0.0,1.0,0.0,0.0,-1.0),
  ]
  return Model(triangles, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans)

def Plane(x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans):
  triangles = [
    createTriangle(-1.0,0.0,-1.0,0.0,1.0,0.0,1.0,0.0, 1.0,0.0, 1.0,1.0,0.0,0.0,1.0,0.0,-1.0,0.0, 1.0,0.0,0.0,0.0,1.0,0.0),
    createTriangle( 1.0,0.0, 1.0,1.0,0.0,0.0,1.0,0.0,-1.0,0.0,-1.0,0.0,1.0,0.0,1.0,0.0, 1.0,0.0,-1.0,1.0,1.0,0.0,1.0,0.0)
  ]
  return Model(triangles, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans)

def Grid(x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans, mul=1):
  triangles = []
  om = 1.0/mul
  for r in range(mul):
    for c in range(mul):
      cm = c/mul
      rm = r/mul
      triangles.append(createTriangle(
          cm-0.5, 0.0, rm-0.5, cm, 1-rm,0.0,1.0,0.0,
          cm+om-0.5, 0.0, rm+om-0.5, cm+om,1-(rm+om),0.0,1.0,0.0,
          cm-0.5, 0.0, rm+om-0.5, cm,1-(rm+om),0.0,1.0,0.0
        ))
      triangles.append(createTriangle(
          cm+om-0.5, 0.0, rm+om-0.5, cm+om,1-(rm+om),0.0,1.0,0.0,
          cm-0.5, 0.0, rm-0.5, cm, 1-rm,0.0,1.0,0.0,
          cm+om-0.5, 0.0, rm-0.5, cm+om, 1-rm,0.0,1.0,0.0
        ))
  return Model(triangles, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans)

def Cone(x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans, div=6):
  DIV = (PI*2.0) / div
  triangles = []
  for i in range(div):
    triangles.append(createTriangle(
        cos(i * DIV), -1.0, sin(i * DIV), 0.0,0.0, -1.0, 0.0, 1.0,
        0.0, -1.0, 0.0, 0.0,0.0, -1.0, 0.0, 1.0,
        cos((i+1) * DIV), -1.0, sin((i+1) * DIV), 0.0,0.0,-1.0,0.0,1.0
      ))
    triangles.append(createTriangle(
        cos(i * DIV), -1.0, sin(i * DIV), i/div,1.0, cos(i * DIV), 0.0, sin(i * DIV),
        cos((i+1) * DIV), -1.0, sin((i+1) * DIV), (i+1)/div,1.0,cos((i+1) * DIV), 0.0, sin((i+1) * DIV),
        0,  1.0, 0, i/div,0.0, 0, 1.00000000, 0
      ))
  return Model(triangles, x, y, z, pi, ya, ro, sx, sy, sz, texture, tsx, tsy, rdist, sh, trans) 

def scaleObject(object, a, b, c):
  object['scale'] = matmul(object['scale'], identity(a, b, c))
  object['transform'] = matmul3(object['scale'], object['rotation'], object['translation'])

def rotateObject(object, p, y, r):
  matmulpitch(object['pitch'], p)
  matmulyaw(object['yaw'], y)
  matmulroll(object['roll'], r)
  object['rotation'] = matmul(object['rotation'], rotatemat(p, y, r))
  object['transform'] = matmul3(object['scale'], object['rotation'], object['translation'])

def translateObject(object, x, y, z):
  matmultranslate(object['translation'], x, y, z)
  object['transform'] = matmul3(object['scale'], object['rotation'], object['translation'])

def translateObjectDirection(object, direction, rotation, scale):
  matmuldirection(object['translation'], direction, rotation, scale)
  object['transform'] = matmul3(object['scale'], object['rotation'], object['translation'])

def applyTransforms(object):
  object['rotation'] = matmul3(object['pitch'], object['yaw'], object['roll'])
  object['transform'] = matmul3(object['scale'], object['rotation'], object['translation'])  

def setNormalToDirection(light, object, direction):
  directionVectorX = 0.0
  directionVectorY = 0.0
  directionVectorZ = 0.0
  if direction == 'r':
    directionVectorX = object['rotation'][0]
    directionVectorY = object['rotation'][4]
    directionVectorZ = object['rotation'][8]
  elif direction == 'u':
    directionVectorX = object['rotation'][1]
    directionVectorY = object['rotation'][5]
    directionVectorZ = object['rotation'][9]
  elif direction == 'f':
    directionVectorX = object['rotation'][2]
    directionVectorY = object['rotation'][6]
    directionVectorZ = object['rotation'][10]
  magnitude = sqrt(directionVectorX*directionVectorX + directionVectorY*directionVectorY + directionVectorZ*directionVectorZ)
  directionVectorX /= magnitude
  directionVectorY /= magnitude
  directionVectorZ /= magnitude
  light['normal'][0] = directionVectorX
  light['normal'][1] = directionVectorY
  light['normal'][2] = directionVectorZ

def setPositionToObject(light, object):
  light['position'][0] = object['transform'][3]
  light['position'][1] = object['transform'][7]
  light['position'][2] = object['transform'][11]

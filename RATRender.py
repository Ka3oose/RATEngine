import pygame
from RATriangles import *
from RAThematics import vertran, vecsub, magnitude, normalize

#Debugging render method which renders lines between triangle vertices
def wireframe(v0, v1, v2, CANVAS_D, SCREEN):
  d0 = (v0[0]*CANVAS_D, v0[1]*CANVAS_D)
  d1 = (v1[0]*CANVAS_D, v1[1]*CANVAS_D)
  d2 = (v2[0]*CANVAS_D, v2[1]*CANVAS_D)
  pygame.draw.polygon(SCREEN, pygame.Color(255, 255, 255), (d0, d1, d2), 2)

def renderTriangleTextured(
    triangle, CANVAS_W, CANVAS_WH, PER_W_MUL, CANVAS_H, CANVAS_HH, PER_H_MUL, CANVAS_D, DEPTH_BUFFER, COLOR_BUFFER, 
    COLOR_BLACK, SKY_COLOR, FOG_DEPTH, FAR_Z, SCENE_LIGHTS, CAM_TRANSF, SCREEN):

  p0 = getTriangleA(triangle)
  p1 = getTriangleB(triangle)
  p2 = getTriangleC(triangle)

  if p1[1] < p0[1]:
    p0, p1 = p1, p0
  if p2[1] < p0[1]:
    p0, p2 = p2, p0
  if p2[1] < p1[1]:
    p1, p2 = p2, p1

  v01 = lerpVertexY(p0, p1)
  v12 = lerpVertexY(p1, p2)
  v02 = lerpVertexY(p0, p2)

  v01.pop()
  v012 = v01
  for v in v12:
     v012.append(v)

  m = len(v012) >> 1
  vertices_left = v012
  vertices_right = v02
  if v02[m][0] <= v012[m][0]:
    vertices_left = v02
    vertices_right = v012

  TEXTURE = triangle['object']['texture']
  TSX = triangle['object']['tScaleX']
  TSY = triangle['object']['tScaleY']
  textureWidth = TEXTURE['width']
  textureHeight = TEXTURE['height']
  y_b = round(p0[1])
  y_t = round(p2[1])
  for y in range(max(y_b, 0), min(y_t, CANVAS_H)):
    vertices_leftVertex = vertices_left[y - y_b]
    vertices_rightVertex = vertices_right[y - y_b]

    x_vertices = lerpVertexX(vertices_leftVertex, vertices_rightVertex)

    x_l = round(vertices_leftVertex[0])
    x_r = round(vertices_rightVertex[0])

    depthBufferPos = y * CANVAS_W + max(x_l, 0)
    
    for x in range(max(x_l, 0), min(x_r, CANVAS_W)):  
      x_vertex = x_vertices[x - x_l]
      z = x_vertex[2]

      if z > DEPTH_BUFFER[depthBufferPos]: 
        iu = x_vertex[3]
        iv = x_vertex[4]
        tx = int((iu / z) * textureWidth * TSX) % textureWidth
        ty = int((iv / z) * textureHeight * TSY) % textureHeight
        texel = TEXTURE['image'][ty * textureWidth + tx]
        if texel[3] > 0:
          h = 1.0
          if triangle['object']['shaded']:
            oZ = (1/z)
            oX = (oZ*((x - CANVAS_WH) / PER_W_MUL))
            oY = (oZ*((CANVAS_HH - y) / PER_H_MUL))
            pixelPosition = [oX, oY, oZ]
            vertran(pixelPosition, CAM_TRANSF)
            normal = [x_vertex[5], x_vertex[6], x_vertex[7]]
            h = 0.0
            for light in SCENE_LIGHTS:
                normalMagnitude = magnitude(normal)
                if light['type'] == 0:
                    h += light['brightness'] 
                elif light['type'] == 1:
                    nDot = dot(normal, light['normal'])
                    if nDot > 0.0:
                        h += (nDot * light['brightness']) / (normalMagnitude * magnitude(light['normal']))
                elif light['type'] > 1:
                    lightToA = light['position'].copy()
                    vecsub(lightToA, pixelPosition)
                    nDot = dot(normal, lightToA)
                    if nDot > 0.0:
                        if light['type'] == 2:
                            h += (nDot * light['brightness']) / (normalMagnitude* dot(lightToA, lightToA))
                        elif light['type'] == 3:
                            lightToANormalized = lightToA.copy()
                            normalize(lightToANormalized)
                            aDot = dot(light['normal'], lightToANormalized)
                            h += (nDot * pow(aDot,light['exponent']) * light['brightness']) / (normalMagnitude * dot(lightToA, lightToA))  

          SHADED_COLOR = COLOR_BLACK.lerp(texel, min(h, 1.0))
          FOG_COLOR = SKY_COLOR.lerp(SHADED_COLOR, min((z - FAR_Z)*FOG_DEPTH, 1.0))
          DRAWN_COLOR = COLOR_BUFFER[depthBufferPos].lerp(FOG_COLOR, texel[3]/255)

          pygame.draw.rect(SCREEN, DRAWN_COLOR, pygame.Rect(x*CANVAS_D, y*CANVAS_D, CANVAS_D, CANVAS_D))    

          DEPTH_BUFFER[depthBufferPos] = z
          COLOR_BUFFER[depthBufferPos].update(DRAWN_COLOR)
      
      depthBufferPos += 1 

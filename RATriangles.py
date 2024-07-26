import pygame
from math import sqrt
from RAThematics import dot, magnitude, matmul, matmul3, normalize, vecsub, vertran

#Returns a triangle represented by a dict structure. A triangle contains three vertices each containing
#x, y, z values (these are the triangles local, world, and projected points as it travels through the rendering pipeling)
#u, v values (these are the triangles texture coordinates normalized to [0, 1])
#p, q, r values (these are the normal points for each vertex of the triangle)
#object (this is a pointer to the object that the triangle belongs to)
#magnitude (this is the distance from the triangle to the camera used for triangle sorting)
def createTriangle(
    ax, ay, az, au, av, ap, aq, ar, 
    bx, by, bz, bu, bv, bp, bq, br, 
    cx, cy, cz, cu, cv, cp, cq, cr,
    object=None, magnitude=0.0):
  return {
    'ax': ax, 'ay': ay, 'az': az, 'au': au, 'av': av, 'ap': ap, 'aq': aq, 'ar': ar,
    'bx': bx, 'by': by, 'bz': bz, 'bu': bu, 'bv': bv, 'bp': bp, 'bq': bq, 'br': br,
    'cx': cx, 'cy': cy, 'cz': cz, 'cu': cu, 'cv': cv, 'cp': cp, 'cq': cq, 'cr': cr,
    'object': object, 'magnitude': magnitude
  }

#Returns a triangle dict from pre-built vertices
#Really only used during clipping to build new triangles from intersected vertices
def reforgeTriangle(v0, v1, v2, object=None, magnitude=0.0):
  return {
    'ax': v0[0], 'ay': v0[1], 'az': v0[2], 'au': v0[3], 'av': v0[4], 'ap': v0[5], 'aq': v0[6], 'ar': v0[7],
    'bx': v1[0], 'by': v1[1], 'bz': v1[2], 'bu': v1[3], 'bv': v1[4], 'bp': v1[5], 'bq': v1[6], 'br': v1[7],
    'cx': v2[0], 'cy': v2[1], 'cz': v2[2], 'cu': v2[3], 'cv': v2[4], 'cp': v2[5], 'cq': v2[6], 'cr': v2[7],
    'object': object, 'magnitude': magnitude
  }

#Return lists representing each of the triangle's vertices
def getTriangleA(t):
  return [t['ax'], t['ay'], t['az'], t['au'], t['av'], t['ap'], t['aq'], t['ar']]

def getTriangleB(t):
  return [t['bx'], t['by'], t['bz'], t['bu'], t['bv'], t['bp'], t['bq'], t['br']]

def getTriangleC(t):
  return [t['cx'], t['cy'], t['cz'], t['cu'], t['cv'], t['cp'], t['cq'], t['cr']]

#Return lists representing only the triangle's normals
def getTriangleANormal(t):
  return [t['ap'], t['aq'], t['ar']]

def getTriangleBNormal(t):
  return [t['bp'], t['bq'], t['br']]

def getTriangleCNormal(t):
  return [t['cp'], t['cq'], t['cr']]

#Return lists representing only the triangle's position points
def getTriangleAPosition(t):
  return [t['ax'], t['ay'], t['az']]

def getTriangleBPosition(t):
  return [t['bx'], t['by'], t['bz']]

def getTriangleCPosition(t):
  return [t['cx'], t['cy'], t['cz']]

#Return center position of triangle
def center(t):
  return [
    (t['ax'] + t['bx'] + t['cx']) / 3,
    (t['ay'] + t['by'] + t['cy']) / 3,
    (t['az'] + t['bz'] + t['cz']) / 3
  ]

#Return list of interpolated vertices between the lowest point and the highest point
def lerpVertexY(vA, vB):
  y0 = round(vA[1])
  y1 = round(vB[1])
  if y0 == y1:
    return [vA]
  x = vA[0]
  z = vA[2]
  u = vA[3]
  v = vA[4] 
  p = vA[5]
  q = vA[6]
  r = vA[7]
  x1 = vB[0]
  z1 = vB[2]
  u1 = vB[3]
  v1 = vB[4]
  p1 = vB[5]
  q1 = vB[6]
  r1 = vB[7]
  idenom = y1 - y0
  x_slope = (x1 - x) / idenom
  z_slope = (z1 - z) / idenom
  u_slope = (u1 - u) / idenom
  v_slope = (v1 - v) / idenom
  p_slope = (p1 - p) / idenom
  q_slope = (q1 - q) / idenom
  r_slope = (r1 - r) / idenom
  values = [[x, y0, z, u, v, p, q, r]]
  for y in range(y0, y1):
    x += x_slope
    z += z_slope
    u += u_slope
    v += v_slope
    p += p_slope
    q += q_slope
    r += r_slope
    values.append([x, y+1, z, u, v, p, q, r])
  return values

#Return list of interpolated vertices between the leftmost point and the rightmost point
def lerpVertexX(vA, vB):
  x0 = round(vA[0])
  x1 = round(vB[0])
  if x0 == x1:
    return [vA]
  y = vA[1]
  z = vA[2]
  u = vA[3]
  v = vA[4] 
  p = vA[5]
  q = vA[6]
  r = vA[7]
  z1 = vB[2]
  u1 = vB[3]
  v1 = vB[4]
  p1 = vB[5]
  q1 = vB[6]
  r1 = vB[7]
  idenom = x1 - x0
  z_slope = (z1 - z) / idenom
  u_slope = (u1 - u) / idenom
  v_slope = (v1 - v) / idenom
  p_slope = (p1 - p) / idenom
  q_slope = (q1 - q) / idenom
  r_slope = (r1 - r) / idenom
  values = []
  for x in range(x0, x1):
    values.append([x, y, z, u, v, p, q, r])
    z += z_slope
    u += u_slope
    v += v_slope
    p += p_slope
    q += q_slope
    r += r_slope
  return values

#Helper function for clipTriangles method
#Finds the interpolated vertex between two vertices
def intersect(a, b, plane, NEAR_Z):
  b_to_a = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
  t = (-NEAR_Z - dot(plane, a)) / dot(plane, b_to_a)
  x = (1 - t) * a[0] + (t * b[0])
  y = (1 - t) * a[1] + (t * b[1])
  z = (1 - t) * a[2] + (t * b[2])
  u = (1 - t) * a[3] + (t * b[3])
  v = (1 - t) * a[4] + (t * b[4])
  p = (1 - t) * a[5] + (t * b[5])
  q = (1 - t) * a[6] + (t * b[6])
  r = (1 - t) * a[7] + (t * b[7])
  return [x, y, z, u, v, p, q, r]

#Clip a list of triangles against a plane
#Determines if/how to clip a triangle against a particular plane by checking which
#points are inside/outside of the plane and then interescting those points
#to return an interpolating vertex which can be used to build new triangles
def clipTriangles(triangles, plane, NEAR_Z):  
  fragments = []
  for triangle in triangles:
    triA = getTriangleA(triangle)
    triB = getTriangleB(triangle)
    triC = getTriangleC(triangle)

    object = triangle['object']
    magnitude = triangle['magnitude']

    d0 = dot(plane, triA) + NEAR_Z 
    d1 = dot(plane, triB) + NEAR_Z
    d2 = dot(plane, triC) + NEAR_Z

    if d0 > 0 and d1 > 0 and d2 > 0:
      fragments.append(triangle)
    elif d0 > 0 and d1 < 0 and d2 < 0:
      bprime = intersect(triA, triB, plane, NEAR_Z)
      cprime = intersect(triA, triC, plane, NEAR_Z)
      fragments.append(reforgeTriangle(triA, bprime, cprime, object, magnitude))
    elif d0 < 0 and d1 > 0 and d2 < 0:
      bprime = intersect(triB, triC, plane, NEAR_Z)
      cprime = intersect(triB, triA, plane, NEAR_Z)
      fragments.append(reforgeTriangle(triB, bprime, cprime, object, magnitude))
    elif d0 < 0 and d1 < 0 and d2 > 0:
      bprime = intersect(triC, triA, plane, NEAR_Z)
      cprime = intersect(triC, triB, plane, NEAR_Z)
      fragments.append(reforgeTriangle(triC, bprime, cprime, object, magnitude))
    elif d0 < 0 and d1 > 0 and d2 > 0:
      aprime = intersect(triB,triA,plane, NEAR_Z)
      bprime = intersect(triC,triA,plane, NEAR_Z)
      fragments.append(reforgeTriangle(triB, triC, aprime, object, magnitude))
      fragments.append(reforgeTriangle(aprime, triC, bprime, object, magnitude))
    elif d0 > 0 and d1 < 0 and d2 > 0:
      aprime = intersect(triC,triB,plane, NEAR_Z)
      bprime = intersect(triA,triB,plane, NEAR_Z)
      fragments.append(reforgeTriangle(triC, triA, aprime, object, magnitude))
      fragments.append(reforgeTriangle(aprime, triA, bprime, object, magnitude))
    elif d0 > 0 and d1 > 0 and d2 < 0:
      aprime = intersect(triA,triC,plane, NEAR_Z)
      bprime = intersect(triB,triC,plane, NEAR_Z)
      fragments.append(reforgeTriangle(triA, triB, aprime, object, magnitude))
      fragments.append(reforgeTriangle(aprime, triB, bprime, object, magnitude))
  
  triangles[:] = fragments[:]


def processTriangles(SCENE_OBJECTS, SCENE_TRIANGLES, CAMERA, CAM_TRANSF_INV, N_PLANE, L_PLANE, R_PLANE, T_PLANE, B_PLANE, NEAR_Z):
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

#Debugging render method which renders lines between triangle vertices
def wireframe(v0, v1, v2, CANVAS_D, SCREEN):
  d0 = (v0[0]*CANVAS_D, v0[1]*CANVAS_D)
  d1 = (v1[0]*CANVAS_D, v1[1]*CANVAS_D)
  d2 = (v2[0]*CANVAS_D, v2[1]*CANVAS_D)
  pygame.draw.polygon(SCREEN, pygame.Color(255, 255, 255), (d0, d1, d2), 2)

def renderTriangles(
    SCENE_TRIANGLES, CANVAS_W, CANVAS_WH, CANVAS_H, CANVAS_HH, PER_W_MUL, PER_H_MUL, CANVAS_D, DEPTH_BUFFER, 
    COLOR_BUFFER, COLOR_BLACK, SKY_COLOR, FOG_DEPTH, FAR_Z, SCENE_LIGHTS, CAMERA_TRANSFORM, SCREEN):
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

    p0 = [triangle['ax'], triangle['ay'], triangle['az'], triangle['au'], triangle['av'], triangle['ap'], triangle['aq'], triangle['ar']]
    p1 = [triangle['bx'], triangle['by'], triangle['bz'], triangle['bu'], triangle['bv'], triangle['bp'], triangle['bq'], triangle['br']]
    p2 = [triangle['cx'], triangle['cy'], triangle['cz'], triangle['cu'], triangle['cv'], triangle['cp'], triangle['cq'], triangle['cr']]

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
    for v in v12:
      v01.append(v)

    m = len(v01) >> 1
    vertices_left = v01
    vertices_right = v02
    if v02[m][0] <= v01[m][0]:
      vertices_left = v02
      vertices_right = v01

    TEXTURE = triangle['object']['texture']
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
          tx = int((iu / z) * TEXTURE['width'] * triangle['object']['tScaleX']) % TEXTURE['width']
          ty = int((iv / z) * TEXTURE['height'] * triangle['object']['tScaleY']) % TEXTURE['height']
          texel = TEXTURE['image'][ty * TEXTURE['width'] + tx]
          if texel[3] > 0:
            h = 1.0
            if triangle['object']['shaded']:
              h = 0.0
              worldspacePixel = [(1/z)*((x - CANVAS_WH) / PER_W_MUL), (1/z)*((CANVAS_HH - y) / PER_H_MUL), 1/z]
              vertran(worldspacePixel, CAMERA_TRANSFORM)
              worldspaceNormal = [x_vertex[5], x_vertex[6], x_vertex[7]]
              normalMagnitude = magnitude(worldspaceNormal)
              for light in SCENE_LIGHTS:
                  lightToPixel = vecsub(light['position'], worldspacePixel)
                  if light['type'] == 0:
                      h += light['brightness'] 
                  elif light['type'] == 1:
                      directionDot = dot(worldspaceNormal, light['normal'])
                      if directionDot > 0.0:
                        h += (directionDot * light['brightness']) / (normalMagnitude * magnitude(light['normal']))
                  elif light['type'] == 2:
                      pointDot = dot(worldspaceNormal, lightToPixel)
                      if pointDot > 0.0:
                        h += (pointDot * light['brightness']) / (normalMagnitude * dot(lightToPixel, lightToPixel))
                  elif light['type'] == 3:
                      spotDot = dot(worldspaceNormal, lightToPixel)
                      lightToPixelNormalized = lightToPixel.copy()
                      normalize(lightToPixelNormalized)
                      if spotDot > 0.0:
                        h += (spotDot * pow(dot(light['normal'], lightToPixelNormalized), light['exponent']) * light['brightness']) / (normalMagnitude * dot(lightToPixel, lightToPixel))

            SHADED_COLOR = COLOR_BLACK.lerp(texel, min(h, 1.0))
            FOG_COLOR = SKY_COLOR.lerp(SHADED_COLOR, min((z - FAR_Z)*FOG_DEPTH, 1.0))
            DRAWN_COLOR = COLOR_BUFFER[depthBufferPos].lerp(FOG_COLOR, texel[3]/255)

            pygame.draw.rect(SCREEN, DRAWN_COLOR, pygame.Rect(x*CANVAS_D, y*CANVAS_D, CANVAS_D, CANVAS_D))    

            DEPTH_BUFFER[depthBufferPos] = z
            COLOR_BUFFER[depthBufferPos].update(DRAWN_COLOR)
        
        depthBufferPos += 1 
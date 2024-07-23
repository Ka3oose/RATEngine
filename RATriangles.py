from RAThematics import dot

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

#Transform a triangle by a matrix 
#Performs vertex-to-matrix multiplication for the x, y, z and p, q, r values of a triangle
#The x, y, z values must be transformed by a matrix that represents all the required transformations
#The p, q, r values must only be transformed by a rotation since normals are.. well.. normalized
def transformTriangle(triangle, transform, rotation):
  tax = triangle['ax']
  tay = triangle['ay']
  taz = triangle['az']
  triangle['ax'] = tax*transform[0]+tay*transform[1]+taz*transform[ 2]+transform[ 3]
  triangle['ay'] = tax*transform[4]+tay*transform[5]+taz*transform[ 6]+transform[ 7]
  triangle['az'] = tax*transform[8]+tay*transform[9]+taz*transform[10]+transform[11]
  tbx = triangle['bx']
  tby = triangle['by']
  tbz = triangle['bz']
  triangle['bx'] = tbx*transform[0]+tby*transform[1]+tbz*transform[ 2]+transform[ 3]
  triangle['by'] = tbx*transform[4]+tby*transform[5]+tbz*transform[ 6]+transform[ 7]
  triangle['bz'] = tbx*transform[8]+tby*transform[9]+tbz*transform[10]+transform[11]
  tcx = triangle['cx']
  tcy = triangle['cy']
  tcz = triangle['cz']
  triangle['cx'] = tcx*transform[0]+tcy*transform[1]+tcz*transform[ 2]+transform[ 3]
  triangle['cy'] = tcx*transform[4]+tcy*transform[5]+tcz*transform[ 6]+transform[ 7]
  triangle['cz'] = tcx*transform[8]+tcy*transform[9]+tcz*transform[10]+transform[11]
  tap = triangle['ap']
  taq = triangle['aq']
  tar = triangle['ar']
  triangle['ap'] = tap*rotation[0]+taq*rotation[1]+tar*rotation[ 2]+rotation[ 3]
  triangle['aq'] = tap*rotation[4]+taq*rotation[5]+tar*rotation[ 6]+rotation[ 7]
  triangle['ar'] = tap*rotation[8]+taq*rotation[9]+tar*rotation[10]+rotation[11]
  tbp = triangle['bp']
  tbq = triangle['bq']
  tbr = triangle['br']
  triangle['bp'] = tbp*rotation[0]+tbq*rotation[1]+tbr*rotation[ 2]+rotation[ 3]
  triangle['bq'] = tbp*rotation[4]+tbq*rotation[5]+tbr*rotation[ 6]+rotation[ 7]
  triangle['br'] = tbp*rotation[8]+tbq*rotation[9]+tbr*rotation[10]+rotation[11]
  tcp = triangle['cp']
  tcq = triangle['cq']
  tcr = triangle['cr']
  triangle['cp'] = tcp*rotation[0]+tcq*rotation[1]+tcr*rotation[ 2]+rotation[ 3]
  triangle['cq'] = tcp*rotation[4]+tcq*rotation[5]+tcr*rotation[ 6]+rotation[ 7]
  triangle['cr'] = tcp*rotation[8]+tcq*rotation[9]+tcr*rotation[10]+rotation[11]


#Transform the triangle's x, y, z values by the projection inputs
#This method will alter the x, y, z, u, v values of the triangle in place
def projectTriangle(tri, CANVAS_WH, CANVAS_HH, PER_W_MUL, PER_H_MUL):
  tri['az'] = 1/tri['az']
  tri['bz'] = 1/tri['bz']
  tri['cz'] = 1/tri['cz']

  tri['ax'] = CANVAS_WH + (tri['ax'] * tri['az']) * PER_W_MUL
  tri['ay'] = CANVAS_HH - (tri['ay'] * tri['az']) * PER_H_MUL
  tri['au'] *= tri['az']
  tri['av'] *= tri['az']

  tri['bx'] = CANVAS_WH + (tri['bx'] * tri['bz']) * PER_W_MUL
  tri['by'] = CANVAS_HH - (tri['by'] * tri['bz']) * PER_H_MUL
  tri['bu'] *= tri['bz']
  tri['bv'] *= tri['bz']

  tri['cx'] = CANVAS_WH + (tri['cx'] * tri['cz']) * PER_W_MUL
  tri['cy'] = CANVAS_HH - (tri['cy'] * tri['cz']) * PER_H_MUL
  tri['cu'] *= tri['cz']
  tri['cv'] *= tri['cz']

#Return center position of triangle
def center(t):
  return [
    (t['ax'] + t['bx'] + t['cx']) / 3,
    (t['ay'] + t['by'] + t['cy']) / 3,
    (t['az'] + t['bz'] + t['cz']) / 3
  ]

#Determine if the triangle is facing the camera or away
#Used only for backface culling test
#Condensed form of dot(cross(b - a, c - a), a) > 0.0
def triangleFacingCamera(tri):
  b_a_x = tri['bx'] - tri['ax']
  b_a_y = tri['by'] - tri['ay']
  b_a_z = tri['bz'] - tri['az']

  c_a_x = tri['cx'] - tri['ax']
  c_a_y = tri['cy'] - tri['ay']
  c_a_z = tri['cz'] - tri['az']

  c00 = tri['ax'] * b_a_y * c_a_z
  c01 = tri['ax'] * c_a_y * b_a_z
  c02 = c_a_x * tri['ay'] * b_a_z
  c03 = b_a_x * tri['ay'] * c_a_z
  c04 = b_a_x * c_a_y * tri['az']
  c05 = c_a_x * b_a_y * tri['az']

  return (c00 - c01 + c02 - c03 + c04 - c05) > 0.0

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
  values = []
  for y in range(y0, y1+1):
    values.append([x, y, z, u, v, p, q, r])
    x += x_slope
    z += z_slope
    u += u_slope
    v += v_slope
    p += p_slope
    q += q_slope
    r += r_slope
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
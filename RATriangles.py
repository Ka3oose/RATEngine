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
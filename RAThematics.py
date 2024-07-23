from math import cos, sin, sqrt, radians

#Return dot product of vectors/vertices
def dot(a, b):
  return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
#Return magnitude of vector/vertex
def magnitude(a):
  return sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])
#Normalize vector/vertex in place
def normalize(a):
  mag = sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])
  a[0] = a[0] / mag
  a[1] = a[1] / mag
  a[2] = a[2] / mag
#Return identity/scale matrix
def identity(i=1.0, j=1.0, k=1.0):
  return [  i,0.0,0.0,0.0,
          0.0,  j,0.0,0.0,
          0.0,0.0,  k,0.0,
          0.0,0.0,0.0,1.0]
#Return general rotation matrix (p->y->r)
def rotatemat(p, y, r):
  pr = radians(p)
  yr = radians(y)
  rr = radians(r)
  cosP = cos(pr)
  sinP = sin(pr)
  cosY = cos(yr)
  sinY = sin(yr)
  cosR = cos(rr)
  sinR = sin(rr)
  return [cosY*cosR, cosR*sinY*sinP - sinR*cosP, cosR*sinY*cosP + sinP*sinR, 0.0,
          cosY*sinR, sinR*sinY*sinP + cosR*cosP, sinR*sinY*cosP - sinP*cosR, 0.0,
              -sinY,                  cosY*sinP,                  cosY*cosP, 0.0,
                0.0,                        0.0,                        0.0, 1.0]
#Return product of two matrices
def matmul(a, b):
  return [a[0]*b[0]+a[4]*b[1]+a[ 8]*b[ 2], a[1]*b[0]+a[5]*b[1]+a[ 9]*b[ 2],
          a[2]*b[0]+a[6]*b[1]+a[10]*b[ 2], a[3]*b[0]+a[7]*b[1]+a[11]*b[ 2]+b[ 3],
          a[0]*b[4]+a[4]*b[5]+a[ 8]*b[ 6], a[1]*b[4]+a[5]*b[5]+a[ 9]*b[ 6],
          a[2]*b[4]+a[6]*b[5]+a[10]*b[ 6], a[3]*b[4]+a[7]*b[5]+a[11]*b[ 6]+b[ 7],
          a[0]*b[8]+a[4]*b[9]+a[ 8]*b[10], a[1]*b[8]+a[5]*b[9]+a[ 9]*b[10],
          a[2]*b[8]+a[6]*b[9]+a[10]*b[10], a[3]*b[8]+a[7]*b[9]+a[11]*b[10]+b[11],
          0.0, 0.0,
          0.0, 1.0]
#Pitch a matrix by an angle in degrees
def matmulpitch(a, angle):
  r = radians(angle)
  _cos = cos(r)
  _sin = sin(r)  
  a4 = a[4]
  a5 = a[5]
  a6 = a[6]
  a7 = a[7]
  a8 = a[8]
  a9 = a[9]
  a10=a[10]
  a11=a[11]
  a[4] = a4*_cos - a8*_sin
  a[5] = a5*_cos - a9*_sin
  a[6] = a6*_cos -a10*_sin
  a[7] = a7*_cos -a11*_sin
  a[8] = a4*_sin + a8*_cos
  a[9] = a5*_sin + a9*_cos
  a[10]= a6*_sin +a10*_cos
  a[11]= a7*_sin +a11*_cos
#Yaw a matrix by an angle in degrees
def matmulyaw(a, angle):
  r = radians(angle)
  _cos = cos(r)
  _sin = sin(r)
  a0 = a[0]
  a1 = a[1]
  a2 = a[2]
  a3 = a[3]
  a8 = a[8]
  a9 = a[9]
  a10=a[10]
  a11=a[11]
  a[0] = a0*_cos + a8*_sin
  a[1] = a1*_cos + a9*_sin
  a[2] = a2*_cos + a10*_sin
  a[3] = a3*_cos + a11*_sin
  a[8] = a8*_cos - a0*_sin
  a[9] = a9*_cos - a1*_sin
  a[10]= a10*_cos- a2*_sin
  a[11]= a11*_cos- a3*_sin
#Roll a matrix by an angle in degrees
def matmulroll(a, angle):
  r = radians(angle)
  _cos = cos(r)
  _sin = sin(r)
  a0 = a[0]
  a1 = a[1]
  a2 = a[2]
  a3 = a[3]
  a4 = a[4]
  a5 = a[5]
  a6 = a[6]
  a7 = a[7]
  a[0] = a0*_cos-a4*_sin
  a[1] = a1*_cos-a5*_sin
  a[2] = a2*_cos-a6*_sin
  a[3] = a3*_cos-a7*_sin
  a[4] = a0*_sin+a4*_cos
  a[5] = a1*_sin+a5*_cos
  a[6] = a2*_sin+a6*_cos
  a[7] = a3*_sin+a7*_cos
#Translate a matrix
def matmultranslate(a, x, y, z):
  a[ 3] += x
  a[ 7] += y
  a[11] += z
#Return product of three matrices
def matmul3(a, b, c):
  d00 = a[0]*b[0]+a[4]*b[1]+a[ 8]*b[ 2]
  d01 = a[1]*b[0]+a[5]*b[1]+a[ 9]*b[ 2]
  d02 = a[2]*b[0]+a[6]*b[1]+a[10]*b[ 2]
  d03 = a[3]*b[0]+a[7]*b[1]+a[11]*b[ 2]+b[ 3]
  d10 = a[0]*b[4]+a[4]*b[5]+a[ 8]*b[ 6]
  d11 = a[1]*b[4]+a[5]*b[5]+a[ 9]*b[ 6]
  d12 = a[2]*b[4]+a[6]*b[5]+a[10]*b[ 6]
  d13 = a[3]*b[4]+a[7]*b[5]+a[11]*b[ 6]+b[ 7]
  d20 = a[0]*b[8]+a[4]*b[9]+a[ 8]*b[10]
  d21 = a[1]*b[8]+a[5]*b[9]+a[ 9]*b[10]
  d22 = a[2]*b[8]+a[6]*b[9]+a[10]*b[10]
  d23 = a[3]*b[8]+a[7]*b[9]+a[11]*b[10]+b[11]
  d30 = a[12]
  d31 = a[13]
  d32 = a[14]
  d33 = a[15]
  return [d00*c[0]+d10*c[1]+d20*c[ 2]+d30*c[ 3], d01*c[0]+d11*c[1]+d21*c[ 2]+d31*c[ 3],
          d02*c[0]+d12*c[1]+d22*c[ 2]+d32*c[ 3], d03*c[0]+d13*c[1]+d23*c[ 2]+d33*c[ 3],
          d00*c[4]+d10*c[5]+d20*c[ 6]+d30*c[ 7], d01*c[4]+d11*c[5]+d21*c[ 6]+d31*c[ 7],
          d02*c[4]+d12*c[5]+d22*c[ 6]+d32*c[ 7], d03*c[4]+d13*c[5]+d23*c[ 6]+d33*c[ 7],
          d00*c[8]+d10*c[9]+d20*c[10]+d30*c[11], d01*c[8]+d11*c[9]+d21*c[10]+d31*c[11],
          d02*c[8]+d12*c[9]+d22*c[10]+d32*c[11], d03*c[8]+d13*c[9]+d23*c[10]+d33*c[11],
          d30, d31, 
          d32, d33]
#Interpolate a point between two points
def interpolate(p0, p1, t):
  return (1 - t) * p0 + t * p1
#Return the difference of two vectors
def vecsub(a, b):
  a[0] -= b[0]
  a[1] -= b[1]
  a[2] -= b[2]
#Transform vertex in place
def vertran(a, b):
  ta0 = a[0]
  ta1 = a[1]
  ta2 = a[2]
  a[0] = ta0*b[ 0]+ta1*b[ 1]+ta2*b[ 2]+b[ 3]
  a[1] = ta0*b[ 4]+ta1*b[ 5]+ta2*b[ 6]+b[ 7]
  a[2] = ta0*b[ 8]+ta1*b[ 9]+ta2*b[10]+b[11]
#Translate a matrix by the forward/right/up direction of a rotation
def matmuldirection(matrix, direction, rotation, scale):
  rotationIndexX = 0
  rotationIndexY = 0
  rotationIndexZ = 0
  if direction == 'r':
    rotationIndexX = 0
    rotationIndexY = 4
    rotationIndexZ = 8 
  elif direction == 'u':
    rotationIndexX = 1
    rotationIndexY = 5
    rotationIndexZ = 9   
  elif direction == 'f':
    rotationIndexX = 2
    rotationIndexY = 6
    rotationIndexZ = 10
  matrix[3]  += rotation[rotationIndexX] * scale
  matrix[7]  += rotation[rotationIndexY] * scale
  matrix[11] += rotation[rotationIndexZ] * scale
#Condensed method to get the inverse camera transform for cameraspace conversion
def getInverseCameraTransform(c):
  cyaw00 = c['yaw'][0]
  cyaw02 = c['yaw'][2]
  cyaw08 = c['yaw'][8]
  cyaw10 = c['yaw'][10]
  ctra03 = c['translation'][3]
  ctra07 = c['translation'][7]
  ctra11 = c['translation'][11]
  cpit05 = c['pitch'][5]
  cpit06 = c['pitch'][6]
  cpit09 = c['pitch'][9]
  cpit10 = c['pitch'][10]
  return [         cyaw00,   0.0,          cyaw08,-cyaw00 * ctra03 - cyaw08 * ctra11,
          cpit09 * cyaw02,cpit05, cpit09 * cyaw10,-cpit05 * ctra07 + cpit09 * (-cyaw02*ctra03 - cyaw10*ctra11),
          cpit10 * cyaw02,cpit06, cpit10 * cyaw10,-cpit06 * ctra07 + cpit10 * (-cyaw02*ctra03 - cyaw10*ctra11),
                      0.0,   0.0,             0.0,                                                         1.0]
#WIKKER MAP
SKY_COLOR = pygame.Color(60,70,120)

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

CAT_SPRITE = Plane(  0.0,  5.0, 60.0, 270.0,  0.0, 0.0,  5.0, 1.0,   5.0, ONGAH, 1.000, 1.0, 100.0, True, False)

SCENE_OBJECTS = [
      Grid(  0.0,  0.0,  0.0,   0.0,  0.0, 0.0, 64.0, 1.0, 128.0, ASPLT, 4.000, 8.0, 400.0, False, False, mul=2),
  CAT_SPRITE,
      Grid(-32.0, 16.0,-32.0, -90.0, -90.0, 0.0, 64.0, 1.0, 32.0, BCKRD, 2.000, 1.0, 200.0, False, False, mul=1),
      Grid(-32.0, 64.0,-32.0, -90.0, -90.0, 0.0, 64.0, 1.0, 64.0, BKRDW, 2.000, 2.0, 200.0, False, False, mul=1),
      Grid(-28.0, 16.0, 32.0, -90.0, -90.0, 0.0, 64.0, 1.0, 32.0, BCKBR, 2.000, 1.0, 200.0, False, False, mul=2),
      Grid(-28.0, 64.0, 32.0, -90.0, -90.0, 0.0, 64.0, 1.0, 64.0, BKBRW, 2.000, 2.0, 200.0, False, False, mul=2),
     Plane(-30.0, 48.0,  0.0, -90.0,   0.0, 0.0,  2.0, 1.0, 48.0, BCKBR, 0.125, 2.0, 100.0, False, False),  
      Grid( 32.0, 16.0, 32.0, -90.0,  90.0, 0.0, 64.0, 1.0, 32.0, BCKGR, 2.000, 1.0, 200.0, False, False, mul=2),
      Grid( 32.0, 64.0, 32.0, -90.0,  90.0, 0.0, 64.0, 1.0, 64.0, BKGRW, 2.000, 2.0, 200.0, False, False, mul=2),
      Grid( 28.0, 16.0,-32.0, -90.0,  90.0, 0.0, 64.0, 1.0, 32.0, BCKHZ, 2.000, 1.0, 200.0, False, False, mul=1),
      Grid( 28.0, 64.0,-32.0, -90.0,  90.0, 0.0, 64.0, 1.0, 64.0, BKHZW, 2.000, 2.0, 200.0, False, False, mul=1),
     Plane( 30.0, 48.0,  0.0,  90.0,   0.0, 0.0,  2.0, 1.0, 48.0, BCKHZ, 0.125, 2.0, 100.0, False, False),  
      Grid(  0.0, 48.0, 64.0, -90.0,   0.0, 0.0, 64.0, 1.0, 96.0, BCKBR, 2.000, 2.0, 200.0, False, False, mul=2),  
     Plane(  0.0, 16.0,-60.0,  90.0,   0.0, 0.0, 32.0, 1.0, 16.0, CHNLK, 4.000, 2.0, 120.0, False, True),   
  Cylinder( 24.0,  6.0,-14.0,   0.0,   0.0, 0.0,  4.0, 6.0,  4.0, EXBRL, 1.000, 1.0, 100.0, False, False, div=8),
  Cylinder( 22.0,  6.0,-24.0,   0.0,   0.0, 0.0,  4.0, 6.0,  4.0, EXBRL, 1.000, 1.0, 100.0, False, False, div=8), 
      Cube( 22.0, 40.0,-32.0,   0.0,   0.0, 0.0,  6.0, 4.0,  8.0, CRGTD, 1.000, 1.0, 100.0, False, False),
      Cube( 22.0, 64.0,-32.0,   0.0,   0.0, 0.0,  6.0, 4.0,  8.0, CRGTD, 1.000, 1.0, 100.0, False, False),
     Plane( 15.0, 22.0,-36.0, -90.0,  90.0, 0.0,  8.0, 1.0, 22.0, LDDER, 1.000, 3.0,  80.0, False, True),
      Cube(-12.0,  8.0, 48.0,   0.0,  45.0, 0.0,  8.0, 8.0,  8.0, WDBOX, 1.000, 1.0, 150.0, False, False),
      Cube( 10.0,  6.0, 50.0,   0.0,  30.0, 0.0,  6.0, 6.0,  6.0, WDBOX, 1.000, 1.0, 150.0, False, False),
      Cube(-14.0,  6.0,-54.0,   0.0, -25.0, 0.0,  4.0, 4.0,  4.0, WDBOX, 1.000, 1.0, 150.0, False, False),
     Plane(-12.0,  1.0,-48.0,   0.0,  20.0, 0.0,  8.0, 1.0,  6.0, TRASH, 1.000, 1.0,  80.0, False, True),
     Plane(-14.0,  1.0,-22.0,   0.0, 150.0, 0.0,  8.0, 1.0,  6.0, TRASH, 1.000, 1.0,  80.0, False, True),
     Plane( 16.0,  1.0, 46.0,   0.0,-120.0, 0.0, 10.0, 1.0,  8.0, TRASH, 1.000, 1.0,  80.0, False, True)
]

SCENE_LIGHTS = [
  PointLight(0.0,16.0,48.0,25.0),
  AmbientLight(0.125)
]
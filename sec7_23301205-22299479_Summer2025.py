from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random #random points e stars akbo je background er jonno
import math

# Camera-related variables
pers_view = 'third' #auto set korlam third person view
cam_target = -1
v_speed = 10 #3rd person e camerar speed
cam_h = 50 #camera r height object er upor theke
fovY = 120  # Field of view
cam_x = 0
cam_y = 80
cam_z = 800 # 3rd person er camera coordinates


#star aktesi background e random positions choose korbo 3d te
count_star = 1000
star = []
for i in range(count_star):
    st_x = random.uniform(-1500, 1500)
    st_y = random.uniform(-1500, 1500)
    st_z = random.uniform(-1500, 1500)
    shine = random.uniform(0.5, 1.0)
    star.append((st_x, st_y, st_z, shine))

#planet er info
#rgb color palette banaitesi shob planet er
color_pl = [(0.5, 0.5, 0.5), (1, 1, 0.77), (0, 0, 1), (1, 0.84,0), (0.75, 0.39, 0), (0.85, 0.65, 0.13), (0, 0.75, 0.5), (0.05, 0.596, 0.73)]
size_pl = [10, 18, 20, 12, 35, 31, 30, 25]
radius_pl = [100,180, 250, 330, 420, 500, 575, 650]
speed_pl = [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03]
ang_pl = [0.0, 90.0, 180.0, 45.0, 270.0, 135.0, 315.0, 60.0] #angle planet der
rot_pl = [0]*8 #rotate korar planet der
rot_sp_pl = [0.1, 0.07, 0.13, 0.05, 0.07, 0.09, 0.06, 0.04] #rotate korar speed
rot_sun = 0.0 #sun er rotation korar

#solar flare er info aguun burst hoye ber hoi sun er
flare_rel_point = 50.0 # sun er centre to je point theke flare release othoba shoot hobe shei distance
flare_sp = 3.0 #shoot hobe je gola oitar speed
radius_fl = 5.0

#game
life = 3
score = 0
pl_miss_count = 0 #tana jodi tinbar e kono planet miss hoi game over. oi consecutive miss howar variable etai rakhbo count
over = False
flare = []

class Flare:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz #velo
        self.flying = True #flare eekhono fly kortese

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    global pers_view, cam_target, rot_sun, cam_x, cam_y, cam_z
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500)  # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if pers_view == 'third':
        gluLookAt(cam_x, cam_y, cam_z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 1, 0)  # Up vector
    else: #pers_view == 'first'
        if cam_target != -1: #first person view 8 ta plsnet er
            pos = cam_target #planet gular jonno
            px = radius_pl[pos]*math.cos(math.radians(ang_pl[pos]))
            py = radius_pl[pos]*math.sin(math.radians(ang_pl[pos]))
            pz = 0
            angle = math.radians(ang_pl[pos])
            lx = -math.sin(angle)
            lz = -math.cos(angle)
            gluLookAt(px, py+cam_h, pz,  # Camera position
                      px+lx*50, py+cam_h, pz+lz*50,  # Look-at target
                      0, 1, 0)  # Up vector
        else: #sun er 1st per jonno cuz or cam_target =-1
            fx, fy, fz, outx, outy, outz = get_flare_point()
            cam_x = fx #camera ta ke position kortesi flare er release point
            cam_y = fy
            cam_z = fz + 30.0 #, Z axis er ektu uporenitesi jeno dekha jai shooting point
            look_x = fx + outx*50.0 #bairer dike takabe je dike flare fire hobe
            look_y = fy + outy*50.0
            look_z = fz
            gluLookAt(cam_x, cam_y, cam_z,  # Camera position
                    look_x, look_y,look_z,  # Look-at target
                    0, 0, 1)  # Up vector



def draw_star():
    glPointSize(2)
    glBegin(GL_POINTS)
    for st_x,st_y,st_z,shine in star:
        glColor3f(shine, shine, shine)
        glVertex3f(st_x, st_y, st_z)
    glEnd()

def draw_sun(): #ekhanne sun r falre release point ta te red sphere akbo
    global rot_sun
    glPushMatrix()
    glRotatef(rot_sun, 0, 0, 1) #z axis er respect e rotate kortesi
    glColor3f(1, 1, 0) #red r green mile holud
    glutSolidSphere(50, 50, 50) #glutSolidCube er moto solidsphere o ase

    #sun er surface e akbo  red flare release korar sphere
    glPushMatrix()
    glTranslatef(flare_rel_point, 0, 0)
    glColor3f(1, 0, 0)
    glutSolidSphere(5, 20, 20)
    glPopMatrix()
    glPopMatrix()

    rot_sun += 0.2
    if rot_sun >= 360.0: #jodi angle 360 r beshi hoi convert kore nibo
        rot_sun -= 360.0

def get_flare_point():
    theta = math.radians(rot_sun)
    fx = flare_rel_point * math.cos(theta)  # je point theke release hobe
    fy = flare_rel_point * math.sin(theta)
    fz = 0.0
    outx = math.cos(theta)  # outwrd normalized direc calculate kore falre bullet er jonno
    outy = math.sin(theta)
    outz = 0.0
    return (fx, fy, fz, outx, outy, outz)


def draw_pl_shade(radius, base_color, dir_light):
    r, g, b = base_color
    lx, ly, lz = dir_light
    brightness = max(lx, 0.0)
    color = (r+ (1-r)*brightness, g +(1-g)*brightness, b+(1-b)*brightness)
    glColor3f(*color)
    gluSphere(gluNewQuadric(), radius, 30, 30)  # parameters are: quadric, radius, slices, stacks


def draw_pl(): #ekhane planet akbo 8 ta
    global ang_pl, rot_pl
    for i in range(8):
        glPushMatrix()
        x = radius_pl[i]*math.cos(math.radians(ang_pl[i])) #x=rcostheta
        y = radius_pl[i]*math.sin(math.radians(ang_pl[i])) #y= rsinthta
        z = 0.0 # planet gula xy plane e ghure
        glTranslatef(x, y, z)
        glRotatef(rot_pl[i], 0, 1, 0)   # parameter gula: angle, x, y, z
        lx, ly, lz = -x, -y, -z
        side = math.sqrt(lx*lx + ly*ly + lz*lz)
        if side == 0:  side = 1.0
        dir_light = (lx/side, ly/side, lz/side) #light er direction
        draw_pl_shade(size_pl[i], color_pl[i], dir_light)
        glPopMatrix()
        ang_pl[i] += speed_pl[i]
        rot_pl[i] += rot_sp_pl[i]

def draw_flares():
    glColor3f(1, 0, 0) #laal
    for i in flare:
        if i.flying:
            glPushMatrix()
            glTranslatef(i.x, i.y, i.z)
            glutSolidSphere(radius_fl, 10, 10)
            glPopMatrix()

def points_collision():
    global score, pl_miss_count, life, over
    running = []
    for i in flare:
        if not i.flying:
            continue
        i.x += i.dx
        i.y += i.dy
        i.z += i.dz

        strike = False
        for j in range(8):
            pl_x = radius_pl[j]*math.cos(math.radians(ang_pl[j]))
            pl_y = radius_pl[j]*math.sin(math.radians(ang_pl[j]))
            pl_z = 0.0
            dis = (i.x - pl_x)**2 + (i.y - pl_y)**2 + (i.z-pl_z)**2
            border = (size_pl[j]+radius_fl)**2 #border er limit ta
            if dis <= border: #taile strike korbe planet ta ke flare
                strike = True
                score += 1
                pl_miss_count = 0
                i.flying = False
                print('A solar flare hit the Planet')
                print(f'Score: {score}')
                break
        if strike:
            continue
        if abs(i.x) > 1000 or abs(i.y)> 1000 or abs(i.z)> 1000: #jodi etto duur chole jai hit na kore tar mane miss korse planet ke hit korar theke
            i.flying = False
            pl_miss_count += 1 #consecutive / tana koita miss hoise increment korbo count e
            if pl_miss_count >= 3: # 3tar beshi miss hoile life ekta kombe
                life -= 1
                print(f"One life decreased, Remaining life: {life}")
                pl_miss_count = 0
                if life <= 0: #3 ta life e shesh hoile game shesh
                    over = True
                    print(f'Game is over. Total score: {score}')
                    print("Press 'r' to RESTART")
            continue
        running.append(i)
    flare[:] = running

def draw_text(x, y, text):
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))



def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    draw_star()
    draw_sun()
    draw_pl()
    draw_flares()
    if not over:
        points_collision()

    glColor3f(1, 1, 1)
    draw_text(10, 730, f"Score: {score}")
    draw_text(10, 710, f"Lives: {life}")
    draw_text(10, 690, f"Consecutive planet missed: {pl_miss_count} ")

    if over:
        draw_text(400, 400, "Game Over")
        draw_text(400, 380, f"Total Score: {score}")
        draw_text(400, 360, "Press 'r' to restart")
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing flares right click).
    """

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not over:
        fx, fy, fz, outx, outy, outz = get_flare_point()
        dx = outx * flare_sp  # flare type bullet velocity = direction * speed
        dy = outy * flare_sp
        dz = outz * flare_sp
        flare.append(Flare(fx, fy, fz, dx, dy, dz))


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs
    """
    global pers_view, cam_target, cam_x, cam_y, cam_z, fovY
    global life, score, pl_miss_count, flare, over, ang_pl, rot_pl, rot_sun

    if key == b'w':
        pers_view = 'first'
        cam_target =-1 #mane sun er 1st person view te jabe ga

    if key == b's':
        pers_view = 'third'
        cam_target =-1
        cam_x, cam_y, cam_z = 0, 80, 800

    if key == b'n':
        fovY -= 1
    if key == b'm':
        fovY += 1

    if key == b'a': #ekhan theke 8 ta planet er key shuru mercuy
        pers_view = 'first'
        cam_target = 0
    if key == b'b':
        pers_view = 'first'
        cam_target = 1
    if key == b'c':
        pers_view = 'first'
        cam_target = 2
    if key == b'd':
        pers_view = 'first'
        cam_target = 3
    if key == b'e':
        pers_view = 'first'
        cam_target = 4
    if key == b'f':
        pers_view = 'first'
        cam_target = 5
    if key == b'g':
        pers_view = 'first'
        cam_target = 6
    if key == b'h':
        pers_view = 'first'
        cam_target = 7

    # # Reset the game if R key is pressed
    if key == b'r':
        life = 3
        score = 0
        pl_miss_count = 0
        flare = []
        over = False
        rot_sun = 0.0
        for i in range(8): #ek ekta planet er jonno random ekta angle
            ang_pl[i] = random.uniform(0.0, 360.0)
            rot_pl[i] = 0

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global cam_x, cam_y, cam_z
    if pers_view == 'third':
    # Move camera up (UP arrow key)
       if key == GLUT_KEY_UP:
           cam_y += v_speed


    # # Move camera down (DOWN arrow key)
       if key == GLUT_KEY_DOWN:
           cam_y -= v_speed

    # moving camera left (LEFT arrow key)
       if key == GLUT_KEY_LEFT:
           cam_x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
       if key == GLUT_KEY_RIGHT:
        cam_x += 1  # Small angle increment for smooth movement





def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()



# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D Solar System OpenGL Game")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)
    glutMainLoop()  # Enter the GLUT main loop



if __name__ == "__main__":
    main()










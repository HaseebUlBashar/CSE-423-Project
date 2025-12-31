from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
cheat_mode = False
auto_fire_delay=0
#Power gaugle
gauge=760
count=0
dynamite_bullets=[]
electric_bullets=[]
#bullets
bullets=[]
#Shop information
electric_power=False
dynamite_power=False
#Level information
GAMEPAUSE=False
MARKET=False

#main Chicken Information
scores_earned=0
Enemies_killed=0
p_x=0
p_y=300
p_z=0
move_speed=10
body_angle = 0.0
beak_angle=0.0

#Enemies:
BLACK_LINE_Y = 50
lives = 50
game_over = False
enemies = []
level=1 #Ei line e problem hote pare
score = 0
ENEMIES_PER_LEVEL = {1: 5, 2: 20, 3: 30}
enemy_speed =0.05
kill_range = 40
#Camera-related variables
flag_cam=False
camera_angle = 0
camera_radius = 500
camera_height = 500
fovY = 120
#Grid Information 
TOTAL_LENGTH=1200
GRID_LENGTH = TOTAL_LENGTH/14
GRID_STARTING_POINT=(TOTAL_LENGTH/2,-TOTAL_LENGTH/2)
#Chicken information
chicken=[]
for i in range(15):
        x= random.randint(-590,590)
        y=random.randint(470,550)
        z=random.choice([True,False])
        chicken.append((x,y,z))
#Tree information
tree=[]
for i in range(10):
        x= random.randint(-590,590)
        y=random.randint(-590,50)
        
        tree.append((x,y))
#Tower Information:
tower=[]
t_x=0
t_y=100
t_z=0
def draw_chicken(x,y,z,flag=False):
     # LEGS (BLACK)
     glColor3f(1.0, 0.7, 0.2)
     
     glPushMatrix()
     glTranslatef(x+10, y,0)
     gluCylinder(gluNewQuadric(), 2, 2,10, 10, 3)
     glPopMatrix()
     glColor3f(1.0, 0.7, 0.2)
     
     glPushMatrix()
     glTranslatef(x-10, y,0)
     gluCylinder(gluNewQuadric(), 2, 2,10, 10, 3)
     glPopMatrix()
     
    # head
     glColor3f(1, 1, 0.8)
     glPushMatrix()
     glTranslatef(x, y, 40)
     gluSphere(gluNewQuadric(), 10, 20, 20)
     glPopMatrix()
     
    #Body
     glColor3f(1, 1, 0.8)
     glPushMatrix()
     glTranslatef(x, y, 20) #z=50 upor theke amra bullet shoot korbo
     gluSphere(gluNewQuadric(), 15, 20, 20)
     glPopMatrix()
     if flag==True:
          angle=90
          a=-8
          l=10
     else:
          angle=-90
          a=+8
          l=20
     #Beak
     glColor3f(1.0, 0.7, 0.2)
     glPushMatrix()
     glTranslatef(x, y+a,40)
     glRotatef(angle, 1, 0, 0)
     gluCylinder(gluNewQuadric(), 4, 0, l, 12, 3)
     glPopMatrix()
     
       
     glColor3f(0.95, 0.95, 0.75)

        # Left wing
     glPushMatrix()
     glTranslatef(x - 15, y, 22)
     glRotatef(20, 0, 0, 1)
     gluSphere(gluNewQuadric(), 7, 16, 16)
     glPopMatrix()

        # Right wing      
     glPushMatrix()
     glTranslatef(x + 15, y, 22)
     glRotatef(-20, 0, 0, 1)
     gluSphere(gluNewQuadric(), 7, 16, 16)
     glPopMatrix()
def spawn_enemies():
    global enemies
    enemies.clear()

    count = ENEMIES_PER_LEVEL[level]

    for i in range(count):
        x = random.uniform(-TOTAL_LENGTH//2 + 100, TOTAL_LENGTH//2 - 100)
        y = -600
        z = 60
        scale = random.uniform(0.25, 0.4)
        alive = True
        spawn_time = time.time()
        enemies.append([x, y, z, scale, alive, spawn_time])


flicker_interval = 0.5  # seconds for on/off

def enemy_visible(e):
    elapsed = time.time() - e[5]

    # Flicker only for first 1 second
    if elapsed < 1:
         return int(elapsed * 10) % 2 == 0

    return e[4]


def update_enemies():
    global lives, game_over
    if game_over:
        return  # stop updating enemies if game is over

    for e in enemies:
        if not e[4]:
            continue

        # Move enemy upward
        e[1] += enemy_speed

        # Crossed black line
        if e[1] >= BLACK_LINE_Y:
            lives -= 1

            if lives <= 0:
                game_over = True
                return

            respawn_enemy(e)



def respawn_enemy(e):
    e[0] = random.uniform(-TOTAL_LENGTH//2 + 100, TOTAL_LENGTH//2 - 100)
    e[1] = -600
    e[2] = 60
    e[3] = random.uniform(0.25, 0.4)  # scale
    e[4] = True                       # alive
    e[5] = time.time()

def kill_enemy_at_position(x, y): # here we are taking the position of the bullet
    global Enemies_killed, scores_earned,kill_range,gauge

    for e in enemies:
        if not e[4]:
            continue

        dx = e[0] - x
        dy = e[1] - y
        if math.sqrt(dx*dx + dy*dy) <= kill_range: #we have determined the magnitude of the vector
            Enemies_killed += 1
            scores_earned += 5
            temp=gauge+15
            if temp<=950:
                gauge+=15
            else:
                gauge=950
            
            respawn_enemy(e)
            return True

    return False


def draw_enemy(e):
    x,y,z,scale,alive,spawn_time=e
    glPushMatrix()
    glTranslatef(x,y,z)
    glScalef(scale,scale,scale)
    glColor3f(1,0,0)
    glutSolidSphere(60,32,32)
    glColor3f(0,0,0)
    glPushMatrix()
    glTranslatef(0,0,90)
    glutSolidSphere(30,32,32)
    glPopMatrix()
    glPopMatrix()

def draw_main_chicken(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(body_angle, 0, 0, 1)  # Rotate around Z-axis
    # Beak
    glColor3f(1.0, 0.7, 0.2)
    glPushMatrix()
    glTranslatef(0, 8, 40)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 0, 15, 12, 3)
    glPopMatrix()

    # LEGS
    glColor3f(1.0, 0.7, 0.2)
    glPushMatrix()
    glTranslatef(10, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 10, 10, 3)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-10, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 10, 10, 3)
    glPopMatrix()

    # Body
    glColor3f(1, 1, 0.8)
    glPushMatrix()
    glTranslatef(0, 0, 20)
    gluSphere(gluNewQuadric(), 15, 20, 20)
    glPopMatrix()

    # Head
    glColor3f(1, 1, 0.8)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 10, 20, 20)
    glPopMatrix()


    # Wings
    glColor3f(0.95, 0.95, 0.75)
    glPushMatrix()
    glTranslatef(-15, 0, 22)
    glRotatef(20, 0, 0, 1)
    gluSphere(gluNewQuadric(), 7, 16, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(15, 0, 22)
    glRotatef(-20, 0, 0, 1)
    gluSphere(gluNewQuadric(), 7, 16, 16)
    glPopMatrix()

    glPopMatrix() 
 

def chicken_tower(x,y,h):
     glPushMatrix()
     glTranslatef(x,y,h)
     glColor3f(0.5, 0.5, 0.5)
     gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 10)
     glPopMatrix()
     
    #Beak
     glColor3f(1.0, 0.7, 0.2)
     glPushMatrix()
     glTranslatef(x, y-15,50+30)
     glRotatef(90, 1, 0, 0)
     gluCylinder(gluNewQuadric(), 4, 0, 12, 12, 3)
     glPopMatrix()
    # head
     glColor3f(0.8, 0.8, 0.8)
     glPushMatrix()
     glTranslatef(x, y, 50+30)
     gluSphere(gluNewQuadric(), 15, 20, 20)
     glPopMatrix()
     
    #Body
     glColor3f(0.75, 0.75, 0.75)
     glPushMatrix()
     glTranslatef(x, y, 50) #z=50 upor theke amra bullet shoot korbo
     gluSphere(gluNewQuadric(), 25, 20, 20)
     glPopMatrix()


     
def power_gauge():
    global gauge
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0,0,0)
    glBegin(GL_LINES)
    glVertex2f(750,750)
    glVertex2f(950,750)
    glVertex2f(950,750)
    glVertex2f(950,720)
    glVertex2f(950,720)
    glVertex2f(750,720)
    glVertex2f(750,720)
    glVertex2f(750,750)
    glEnd()
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(750, 750)
    glVertex2f(gauge, 750)
    glVertex2f(gauge, 720)
    glVertex2f(750, 720)
    glEnd()


    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
def draw_rewards():
    global electric_power
    

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Panel
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(10, 700)
    glVertex2f(300, 700)
    glVertex2f(300, 500)
    glVertex2f(10, 500)
    glEnd()
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(310, 700)
    glVertex2f(600, 700)
    glVertex2f(600, 500)
    glVertex2f(310, 500)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(610, 700)
    glVertex2f(900, 700)
    glVertex2f(900, 500)
    glVertex2f(610, 500)
    glEnd()

    # Text
    glColor3f(1, 1, 1)
    draw_text(20, 620, "ADD ONE CHICKEN TOWER")
    draw_text(20, 580, "TO SET-PRESS 'ENTER'")
    draw_text(20, 540, "Price-40")

    glColor3f(1, 1, 1)
    draw_text(320, 620, "INCREASE HEALTH BY 5")
    draw_text(320, 580, "Price-60")
    if electric_power==False:
        glColor3f(1, 1, 1)
        draw_text(620, 620, "UNLOCK ELECTRIC POWER")
        draw_text(620, 580, "Price-80")
    if electric_power==True:
        glColor3f(1, 1, 1)
        draw_text(620, 620, "UNLOCK Dynamite POWER")
        draw_text(620, 580, "Price-80")
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def keyboardListener(key, x, y):
    global scores_earned,Enemies_killed,GAMEPAUSE,level,MARKET,tower
    global p_x, p_y,body_angle,beak_angle,bullets,dynamite_bullets,count,gauge,electric_power,cheat_mode,GAMEPAUSE,move_speed,p_z,dynamite_power,electric_bullets,game_over,lives,enemy_speed
    if key==b'r':

        enemy_speed=0.05
        tower.clear()
        lives=50
        game_over=False
        cheat_mode=False
        level=1
        gauge=760
        count=0
        dynamite_bullets=[]
        electric_bullets=[]
        #bullets
        bullets=[]
        #Shop information
        electric_power=False
        dynamite_power=False
        #Level information
        GAMEPAUSE=False
        MARKET=False

        #main Chicken Information
        scores_earned=0
        Enemies_killed=0
        p_x=0
        p_y=300
        p_z=0
        move_speed=10
        body_angle = 0.0
        beak_angle=0.0
        spawn_enemies()

    if key==b'c':
        cheat_mode=not cheat_mode
    speed = 10.0
    rotate_speed = 5.0
    if key==b"1" and GAMEPAUSE==True:
        GAMEPAUSE=False
        MARKET=False
        Enemies_killed=0
        spawn_enemies()
        cheat_mode=False
        if level==1:
            level=2
        elif level==2:
            level=3
    if key == b'\r':
         for i in tower:
              if i[3]==True:
                   i[3]=False
                   i[4]=[i[0],i[1]-50,i[2]+50]
                   break
    if not GAMEPAUSE and not game_over:
        if key == b'a':
            body_angle += rotate_speed
            beak_angle += rotate_speed
        elif key == b'd':
            body_angle -= rotate_speed
            beak_angle -= rotate_speed
        body_angle %= 360 # The angle is clamped to 360 degree 

        # Move along beak direction
        rad = math.radians(body_angle)
        dx = speed * -math.sin(rad)
        dy = speed * math.cos(rad)
        if key == b'w':
            p_x += dx
            p_y += dy
        elif key == b's':
            p_x -= dx
            p_y -= dy

        # ---- CLAMP inside red line and fence ----
        p_x = max(-600, min(600, p_x))
        p_y = max(60, min(450, p_y))
        # FIRE BULLET
        if key == b'p':
            beak_offset_x = 0 #We have considered this with respect to the origin
            beak_offset_y = 8
            beak_offset_z = 60
            rad = math.radians(body_angle)
            bullet_x = p_x + beak_offset_x * math.cos(rad) - beak_offset_y * math.sin(rad) # Here we used the rotation matrix
            bullet_y = p_y + beak_offset_x * math.sin(rad) + beak_offset_y * math.cos(rad)
            bullet_z = p_z + beak_offset_z
            bullets.append({'x': bullet_x, 'y': bullet_y, 'z': bullet_z, 'angle': body_angle})
        #Electric bullet:
        if key == b'o' and gauge == 950 and electric_power == True:
            count += 1
            if count >= 5:
                count = 0
                gauge = 760

            beak_offset_x = 0
            beak_offset_y = 8
            beak_offset_z = 60
            rad = math.radians(body_angle)
            electric_bullet_x = p_x + beak_offset_x * math.cos(rad) - beak_offset_y * math.sin(rad)
            electric_bullet_y = p_y + beak_offset_x * math.sin(rad) + beak_offset_y * math.cos(rad)
            electric_bullet_z = p_z + beak_offset_z
            electric_bullets.append({'x': electric_bullet_x, 'y': electric_bullet_y, 'z': electric_bullet_z, 'angle': body_angle})
        # FIRE BULLET
        if key == b'i' and gauge==950 and dynamite_power==True:
            count+=1
            if count>=5:
                count=0
                gauge=760
            

            beak_offset_x = 0
            beak_offset_y = 20
            beak_offset_z = 60
            rad = math.radians(body_angle)
            dynamite_bullets_x = p_x + beak_offset_x * math.cos(rad) - beak_offset_y * math.sin(rad)
            dynamite_bullets_y = p_y + beak_offset_x * math.sin(rad) + beak_offset_y * math.cos(rad)
            dynamite_bullets_z = p_z + beak_offset_z
            dynamite_bullets.append({'x': dynamite_bullets_x, 'y': dynamite_bullets_y, 'z': dynamite_bullets_z, 'angle': body_angle})


def specialKeyListener(key, x, y):
    global camera_angle,camera_height,GAMEPAUSE,tower
    if not GAMEPAUSE:
        if key == GLUT_KEY_LEFT:
            camera_angle-=1

        if key == GLUT_KEY_RIGHT:
            camera_angle+=1

        if key == GLUT_KEY_DOWN:
            camera_height = max(100, camera_height - 5)
        if key == GLUT_KEY_UP:
            camera_height = min(1000, camera_height + 5)
    else:
        for i in tower:
             if i[3]==True:
                if key == GLUT_KEY_LEFT:
                    i[0] = min(600, i[0] + 5)
                if key == GLUT_KEY_RIGHT:
                    i[0] = max(-600, i[0] - 5)

                if key == GLUT_KEY_DOWN:
                    i[1] = min(450, i[1] + 5)
                if key == GLUT_KEY_UP:
                    i[1] = max(60, i[1] - 5) 
         
         

def mouseListener(button, state, x, y):
    global flag_cam,MARKET,scores_earned,t_x,t_y,t_z,tower,lives,electric_power,dynamite_power
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            flag_cam=not flag_cam
    # global tower,build_tower

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
         if MARKET==True :
              store_x=x
              store_y=800-y
              if 10<store_x<300 and 500<store_y<700 and scores_earned>=40:
                   tower.append([t_x, t_y, t_z,True,None])
                   scores_earned -= 40
              if 310<store_x<600 and 500<store_y<700 and scores_earned>=60:
                  lives+=10
                  scores_earned -= 60
              if 610<store_x<900 and 500<store_y<700 and scores_earned>=80 and electric_power==False and dynamite_power==False:
                  electric_power=True
                  scores_earned -= 80
              elif 610<store_x<900 and 500<store_y<700 and scores_earned>=80 and dynamite_power==False and electric_power==True:
                  dynamite_power=True
                  scores_earned -= 80

                   

def setupCamera():

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x = -camera_radius * math.sin(math.radians(camera_angle))
    y = camera_radius * math.cos(math.radians(camera_angle))
    z = camera_height

    if flag_cam:
            angle = math.radians(body_angle)

            hand_x = p_x + 30 * (-math.sin(angle))
            hand_y = p_y + 30 * ( math.cos(angle))
            hand_z = p_z +90

            gluLookAt(
                p_x, p_y, p_z + 110,
                hand_x, hand_y, hand_z,
                0, 0, 1 )
    else:
            gluLookAt(x, y, z,
                0, 0, 0,
                0, 0, 1)
last_cheat_fire_time=0
cheat_fire_rate=0.1
def idle():

    global level, Enemies_killed, body_angle, bullets, p_x, p_y
    global auto_fire_delay, enemies, game_over,last_cheat_fire_time, cheat_mode

    if not GAMEPAUSE and not game_over:
        update_enemies()
        update_tower_bullets()


    if cheat_mode and not GAMEPAUSE and not game_over: #Cheat mode will always fire the closest enemies at first
        current_time = time.time()
        # Find the nearest alive enemy
        closest_enemy = None
        min_dist = float('inf')
        for e in enemies:
            if not e[4]:  # skip dead enemies
                continue
            dx = e[0] - p_x
            dy = e[1] - p_y
            dist = math.hypot(dx, dy)
            if dist < min_dist:
                min_dist = dist
                closest_enemy = e # Here we determine which enemy is the closest to us

        if closest_enemy:
            rotation_speed = 3  # Degrees per frame
            body_angle += rotation_speed
            if body_angle >= 360:
                body_angle -= 360
            elif body_angle < 0:
                body_angle += 360
    
            dx = closest_enemy[0] - p_x
            dy = closest_enemy[1] - p_y
            target_angle_math = math.degrees(math.atan2(dy, dx))
            angle_to_enemy = 90 - target_angle_math
            if angle_to_enemy < 0:
                angle_to_enemy += 360
            elif angle_to_enemy >= 360:
                angle_to_enemy -= 360
            angle_difference = abs(body_angle - angle_to_enemy)
            
            angle_difference = min(angle_difference, 360 - angle_difference)
            if angle_difference < 1.5 and current_time - last_cheat_fire_time > cheat_fire_rate:
                rad = math.radians(body_angle)
                
                # Same formula as pressing 'p'
                bullet_x = p_x + 0 * math.cos(rad) - 8 * math.sin(rad)
                bullet_y = p_y + 0 * math.sin(rad) + 8 * math.cos(rad)
                bullet_z = p_z + 60
                bullets.append({
                    'x': bullet_x, 
                    'y': bullet_y, 
                    'z': bullet_z, 
                    'angle': body_angle,
                    'target_x': closest_enemy[0],
                    'target_y': closest_enemy[1],
                    'homing': True
                })
                
                last_cheat_fire_time = current_time


    if not GAMEPAUSE and not game_over:
        update_enemies()
        update_tower_bullets()

    glutPostRedisplay()


def update_tower_bullets():
    global tower 
    
    ###########################        

    bullet_speed = 1

    for t in tower:
        if t[4] is not None:  # check if bullet exists
            t[4][1] -= bullet_speed
            if kill_enemy_at_position(t[4][0], t[4][1]):
                t[4] = [t[0], t[1], t[2]+50]
            elif t[4][1] <= -600:
                t[4] = [t[0], t[1], t[2]+50]

def drawtrees():
     for x,y in tree:
        glPushMatrix()
        glColor3f(0.55, 0.27, 0.07)
        glTranslatef(x,y , 0)
        gluCylinder(gluNewQuadric(), 10, 10, 100, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.13, 0.55, 0.13)
        glTranslatef(x,y,100)
        gluSphere(gluNewQuadric(),50, 5, 5)
        glPopMatrix()
def showScreen():
    global GAMEPAUSE,MARKET,t_x,t_y,t_z,flag_cam,enemy_speed,kill_range

    glClearColor(0.53,0.81,0.98,1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()
    x,y=GRID_STARTING_POINT
    temp='Green'
    glBegin(GL_QUADS)
    for i in range(14):
        temp1=x
        for j in range(14):

            if temp=='Green':
                glColor3f(0.2,0.6,0.2)
                temp='Light green'
            else:
                glColor3f(0.25,0.7,0.25)
                temp="Green"
            glVertex3f(temp1,y,0)
            glVertex3f(temp1-GRID_LENGTH,y,0)
            glVertex3f(temp1-GRID_LENGTH,y+GRID_LENGTH,0)
            glVertex3f(temp1,y+GRID_LENGTH,0)

            temp1-=GRID_LENGTH
        y+=GRID_LENGTH
    glEnd()
    #Fence drawing starts here
    x,y=GRID_STARTING_POINT
    glBegin(GL_QUADS)
    glColor3f(0.36, 0.25, 0.20)
    glVertex3f(x,-y-150,50)
    glVertex3f(-x,-y-150,50)
    glVertex3f(-x,-y-150,45)
    glVertex3f(x,-y-150,45)

    glVertex3f(x,-y-150,10)
    glVertex3f(-x,-y-150,10)
    glVertex3f(-x,-y-150,5)
    glVertex3f(x,-y-150,5)
    temp=x
    for i in range(115):
        glVertex3f(temp-20,-y-150,60)
        glVertex3f(temp-25,-y-150,60)
        glVertex3f(temp-25,-y-150,0)
        glVertex3f(temp-20,-y-150,0)
        temp-=10
    #Fence information
    glColor3f(0.7,0,0)
    glVertex3f(x,50,0)
    glVertex3f(-x,50,0)
    glVertex3f(-x,60,0)
    glVertex3f(x,60,0)
    glEnd()
    for p,q,z in chicken:
         draw_chicken(p,q,0,z)
    drawtrees()
    draw_main_chicken(p_x, p_y, 20)
    for e in enemies:
        if e[4] and enemy_visible(e):
            draw_enemy(e)
    for tx, ty, tz,flag,bullet in tower:
        chicken_tower(tx, ty, tz)
    for t in tower:
            if t[3]==False and t[4]!=None:
                glPushMatrix()
                glColor3f(1, 1, 0)  # yellow bullet
                glTranslatef(t[4][0], t[4][1], t[4][2])
                gluSphere(gluNewQuadric(), 10, 8, 8)  # small sphere
                glPopMatrix()


    # Display game info text at a fixed screen position
    if game_over==False:
        if GAMEPAUSE==False:
    
                if cheat_mode:
                    glColor3f(1, 0, 0)
                    draw_text(790, 100, "CHEAT MODE: ON")
                    glColor3f(1, 1, 1) 
                glColor3f(1,1,1)
                draw_text(10, 770, f"Level {level}")
                draw_text(10, 740, f"POINTS EARNED: {scores_earned}")
                draw_text(10, 710, f"ENEMIES KILLED: {Enemies_killed}")
                draw_text(10, 710-30, f"LIVES REMAINING: {lives}")
                draw_text(800, 770, f"POWER GAUGE : {gauge}")
                power_gauge()
                if gauge==950 and electric_power==True:
                    draw_text(750, 700, f"PRESS 'O' for Fire Power ")
                if gauge==950 and dynamite_power==True:
                    draw_text(750, 650, f"PRESS 'I' for Dynamite Power ")
                    
                if Enemies_killed==20 and level==1:
                    GAMEPAUSE=True
                    if flag_cam==True:
                        flag_cam=False
                    MARKET=True
                    enemy_speed=0.1
                elif Enemies_killed==30 and level==2:
                    GAMEPAUSE=True
                    if flag_cam==True:
                        flag_cam=False
                    MARKET=True
                    enemy_speed=0.15
                elif Enemies_killed==40 and level==3:
                    if flag_cam==True:
                        flag_cam=False
                    GAMEPAUSE=True
        else:
            if level!=3:
                glColor3f(1,1,1)
                draw_text(10, 770, f"Congrats you have survived LEVEL {level}")
                draw_text(10, 740, f"YOUR CURRENT SCORE POINT {scores_earned}")
                draw_text(500, 740, f"LIVES REMAINING {lives}")
                glColor3f(1,0,0)
                draw_text(10, 710, f"Pick the reward given below")
                draw_rewards()
            else:
                glColor3f(1,1,1)
                draw_text(10, 770, f"CONGRATS YOU HAVE WON THE GAME")
                glColor3f(1,0,0)
                draw_text(10, 740, f"Press'R'to restrat the game")
    else:
        glColor3f(1,0,0)
        draw_text(10, 710, f"GAME OVER. Press 'R' to play again")
        flag_cam=False
    #Common Bullet
    new_bullets = []
    for b in bullets:
        kill_range=40
        rad = math.radians(b['angle'])
        if cheat_mode and 'homing' in b and b['homing']:
            dx = b.get('target_x', 0) - b['x']
            dy = b.get('target_y', 0) - b['y']
            dist = math.hypot(dx, dy)
            if dist > 10:
                dx /= dist
                dy /= dist
                b['x'] += dx * 10
                b['y'] += dy * 10
                b['angle'] = 90 - math.degrees(math.atan2(dy, dx))

            else:
                 b['x'] += 5 * -math.sin(rad)
                 b['y'] += 5 * math.cos(rad)

            
        else:        
            b['x'] += 5 * -math.sin(rad) # Here 5 is the bullet speed
            b['y'] += 5 * math.cos(rad)

        
        if kill_enemy_at_position(b['x'], b['y']):
                 continue  
        if not (-TOTAL_LENGTH/2 <= b['x'] <= TOTAL_LENGTH/2 and \
            -TOTAL_LENGTH/2 <= b['y'] <= TOTAL_LENGTH/2):
                     continue 
        if cheat_mode and 'homing' in b and b['homing']:
            dist_from_start = math.hypot(b['x'] - p_x, b['y'] - p_y)
            if dist_from_start > 750: 
                    continue

        # DRAW BULLET
        glPushMatrix()
        glTranslatef(b['x'], b['y'], b['z'])
        glColor3f(1, 1, 0.8)
        glutSolidSphere(5, 12, 12)
        glPopMatrix()
        new_bullets.append(b)
        

    bullets[:] = new_bullets
    #Electric bullets:
    kill_range=90
    new_electric_bullets = []
    for e in electric_bullets:
        rad = math.radians(e['angle'])
        e['x'] += 1.5 * -math.sin(rad)
        e['y'] += 1.5 * math.cos(rad)

    
        if kill_enemy_at_position(e['x'], e['y']):
            pass  

        glPushMatrix()
   
        jitter_x = e['x'] + random.uniform(-10, 10)
        jitter_y = e['y'] + random.uniform(-10, 10)
        jitter_z = e['z'] + random.uniform(-10, 10)
        glTranslatef(jitter_x, jitter_y, jitter_z)
        
        for i in range(3): 
            if i == 0:
                glColor3f(0.6, 0.8, 1)  
                radius = 20+ random.uniform(-10, 1)
            elif i == 1:
                glColor3f(0.3, 0.6, 1) 
                radius = 30+ random.uniform(-10, 10)
            else:
                glColor3f(0.0, 0.3, 1)  #
                radius = 40 + random.uniform(-10, 100)
            glutSolidSphere(radius, 12, 12)
        glPopMatrix()

        # Keep bullets in bounds
        if -TOTAL_LENGTH/2 <= e['x'] <= TOTAL_LENGTH/2 and \
        -TOTAL_LENGTH/2 <= e['y'] <= TOTAL_LENGTH/2:
            new_electric_bullets.append(e)

    electric_bullets[:] = new_electric_bullets
    #Dynamite bullet:
    new_dynamite_bullets = []

    for c in dynamite_bullets:
        kill_range=120
        rad = math.radians(c['angle'])
        c['x'] += 1.5* -math.sin(rad)   
        c['y'] += 1.5 *  math.cos(rad)

       
        if kill_enemy_at_position(c['x'], c['y']):
            pass   

      
        glPushMatrix()

        jx = random.uniform(-10, 10)
        jy = random.uniform(-10, 10)
        glTranslatef(c['x'] + jx, c['y'] + jy, c['z'])
        trail_steps = 5
        trail_gap = 50
        for t in range(1, trail_steps + 1):
            glPushMatrix()
            glTranslatef(
                -t * trail_gap * -math.sin(rad),
                -t * trail_gap *  math.cos(rad),
                0
            )
            glColor3f(1, 0.4, 0)
            glutSolidSphere(15 - t, 8, 8)
            glPopMatrix()

       
        for i in range(3):
            if i == 0:
                glColor3f(1, 1, 0)      
                radius = 18 + random.uniform(-10, 10)
            elif i == 1:
                glColor3f(1, 0.5, 0)   
                radius = 28 + random.uniform(-20, 20)
            else:
                glColor3f(1, 0, 0)      
                radius = 38 + random.uniform(-30, 30)

            glutSolidSphere(radius, 14, 14)

        glColor3f(1, 0.3, 0.1)
        glutSolidSphere(45, 18, 18)

        glPopMatrix()

      
        if -TOTAL_LENGTH/2 <= c['x'] <= TOTAL_LENGTH/2 and \
        -TOTAL_LENGTH/2 <= c['y'] <= TOTAL_LENGTH/2:
            new_dynamite_bullets.append(c)

    dynamite_bullets[:] = new_dynamite_bullets
    #Aura
    if gauge==950:
        for _ in range(30):
            a,b,c=p_x,p_y,p_z

            a=random.uniform(a+20,a-20)
            b=random.uniform(b+20,b-20)
            c=random.uniform(0,80)
            glPushMatrix()
            glBegin(GL_QUADS)
            glColor3f(0,0,1)
            glVertex3f(a,b,c)
            glVertex3f(a,b,c-5)
            glVertex3f(a+1,b,c-5)
            glVertex3f(a+1,b,c)
            glEnd()
            glPopMatrix()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Murgi VS Zombies Game")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    spawn_enemies()
    glutMainLoop()

if __name__ == "__main__":
    main()



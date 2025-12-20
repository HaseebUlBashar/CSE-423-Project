# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import math
# import random

# # -----------------------------
# #          GAME STATE
# # -----------------------------
# PLAY = True
# CHEAT = False
# TOGGLE_FOLLOW = False
# temp_angle = 0
# auto_fire_delay = 0

# # Camera variables
# camera_angle = 0
# camera_radius = 500
# camera_height = 500
# flag_cam = False
# fovY = 120

# # Grid
# TOTAL_LENGTH = 1200
# GRID_LENGTH = TOTAL_LENGTH / 13
# GRID_STARTING_POINT = (TOTAL_LENGTH / 2, -TOTAL_LENGTH / 2)

# # Player
# theta = 0
# p_x = 0
# p_y = 0
# p_z = 0
# PLAYER_LIFE = 5
# GAME_SCORE = 0
# BULLET_MISSED = 0
# bullet = []

# # Enemies
# NUM_ENEMIES = 5
# enemies = []
# for i in range(NUM_ENEMIES):
#     enemies.append({
#         "x": random.uniform(-TOTAL_LENGTH/2, TOTAL_LENGTH/2),
#         "y": random.uniform(-TOTAL_LENGTH/2, TOTAL_LENGTH/2),
#         "z": 0,
#         "size": random.uniform(0.3, 1),
#         "shrink": True
#     })

# # Explosions (particle systems)
# explosions = []


# # ===============================================================
# #                      VISUAL ENHANCEMENTS
# # ===============================================================

# def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
#     """Outlined HUD text for readability."""
#     glDisable(GL_LIGHTING)

#     # black border
#     glColor3f(0, 0, 0)
#     for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
#         glRasterPos2f(x + dx, y + dy)
#         for ch in text:
#             glutBitmapCharacter(font, ord(ch))

#     # white text
#     glColor3f(1, 1, 1)
#     glRasterPos2f(x, y)
#     for ch in text:
#         glutBitmapCharacter(font, ord(ch))

#     glEnable(GL_LIGHTING)


# def draw_sky():
#     """Simple sky gradient."""
#     glDisable(GL_LIGHTING)
#     glBegin(GL_QUADS)

#     glColor3f(0.25, 0.45, 0.9)  # top
#     glVertex3f(-2000, -2000, 2000)
#     glVertex3f(2000, -2000, 2000)

#     glColor3f(0.95, 0.95, 1.0)  # horizon
#     glVertex3f(2000, 2000, 200)
#     glVertex3f(-2000, 2000, 200)

#     glEnd()
#     glEnable(GL_LIGHTING)


# def draw_ground():
#     """Enhanced grid with soft colors and border."""
#     glDisable(GL_LIGHTING)
#     glBegin(GL_QUADS)

#     for i in range(13):
#         for j in range(13):
#             if (i + j) % 2 == 0:
#                 glColor3f(0.90, 0.93, 1.0)
#             else:
#                 glColor3f(0.75, 0.82, 1.0)

#             x = GRID_STARTING_POINT[0] - j * GRID_LENGTH
#             y = GRID_STARTING_POINT[1] + i * GRID_LENGTH

#             glVertex3f(x, y, 0)
#             glVertex3f(x - GRID_LENGTH, y, 0)
#             glVertex3f(x - GRID_LENGTH, y + GRID_LENGTH, 0)
#             glVertex3f(x, y + GRID_LENGTH, 0)

#     glEnd()

#     # Border
#     glColor3f(0, 0, 0.4)
#     glLineWidth(6)
#     glBegin(GL_LINE_LOOP)
#     glVertex3f(600, -600, 1)
#     glVertex3f(-600, -600, 1)
#     glVertex3f(-600, 600, 1)
#     glVertex3f(600, 600, 1)
#     glEnd()

#     glEnable(GL_LIGHTING)


# # ===============================================================
# #                     EXPLOSION SYSTEM
# # ===============================================================

# def create_explosion(x, y, z):
#     """Spawn particles when an enemy dies."""
#     particles = []
#     for i in range(25):
#         angle = random.uniform(0, 2 * math.pi)
#         speed = random.uniform(1, 5)

#         particles.append({
#             "x": x,
#             "y": y,
#             "z": z,
#             "vx": math.cos(angle) * speed,
#             "vy": math.sin(angle) * speed,
#             "vz": random.uniform(1, 4),
#             "life": 1.0,
#             "decay": random.uniform(0.02, 0.05)
#         })

#     explosions.append(particles)


# def draw_explosions():
#     glDisable(GL_LIGHTING)

#     for explosion in explosions:
#         for p in explosion:
#             if p["life"] > 0:
#                 glPushMatrix()
#                 glTranslatef(p["x"], p["y"], p["z"])
#                 glColor4f(1, p["life"], 0, p["life"])  # fades out
#                 glutSolidSphere(4, 8, 8)
#                 glPopMatrix()

#     glEnable(GL_LIGHTING)


# # ===============================================================
# #                       PLAYER MODEL
# # ===============================================================

# def human():
#     """Improved player model with helmet + visor."""
#     global p_x, p_y, p_z, theta, PLAY

#     glPushMatrix()
#     glTranslatef(p_x, p_y, p_z)
#     glRotatef(theta, 0, 0, 1)

#     if not PLAY:
#         glRotatef(90, 1, 0, 0)

#     # Helmet
#     glPushMatrix()
#     glColor3f(0.2, 0.2, 0.25)
#     glTranslatef(0, 0, 95)
#     gluSphere(gluNewQuadric(), 15, 20, 20)
#     glPopMatrix()

#     # Visor
#     glPushMatrix()
#     glColor3f(0.4, 0.8, 1.0)
#     glTranslatef(0, 10, 95)
#     gluSphere(gluNewQuadric(), 8, 20, 20)
#     glPopMatrix()

#     # Body
#     glPushMatrix()
#     glColor3f(0, 0.6, 0.1)
#     glTranslatef(0, 0, 55)
#     glScalef(1.2, 0.7, 2.2)
#     glutSolidCube(25)
#     glPopMatrix()

#     # Legs
#     for side in [10, -10]:
#         glPushMatrix()
#         glColor3f(0, 0, 0.7)
#         glTranslatef(side, 0, 20)
#         gluCylinder(gluNewQuadric(), 5, 5, 30, 15, 15)
#         glPopMatrix()

#     # Gun
#     glPushMatrix()
#     glColor3f(0.8, 0.8, 0.8)
#     glTranslatef(0, 15, 75)
#     glRotatef(-90, 1, 0, 0)
#     gluCylinder(gluNewQuadric(), 4, 3, 40, 10, 10)
#     glPopMatrix()

#     glPopMatrix()


# # ===============================================================
# #                ENEMIES AND BULLETS (VISUAL)
# # ===============================================================

# def draw_enemies():
#     """Pulsating sphere + glowing core."""
#     for e in enemies:
#         glPushMatrix()
#         glTranslatef(e["x"], e["y"], 40 + math.sin(glutGet(GLUT_ELAPSED_TIME)/300)*4)
#         glScalef(e["size"], e["size"], e["size"])

#         # Outer shell
#         glColor3f(1, 0.3, 0.3)
#         gluSphere(gluNewQuadric(), 35, 20, 20)

#         # Glowing core
#         glColor3f(1, 1, 0.3)
#         gluSphere(gluNewQuadric(), 18, 20, 20)

#         glPopMatrix()


# def draw_bullet():
#     """Bullet with glowing trail."""
#     glDisable(GL_LIGHTING)
#     for b in bullet:
#         glPushMatrix()
#         glTranslatef(b['x'], b['y'], 75)

#         # trail
#         glBegin(GL_LINES)
#         glColor3f(1, 0.8, 0)
#         glVertex3f(0, 0, -10)
#         glColor3f(1, 0, 0)
#         glVertex3f(0, 0, -40)
#         glEnd()

#         # bullet
#         glColor3f(1, 0.3, 0.1)
#         glutSolidSphere(7, 12, 12)

#         glPopMatrix()
#     glEnable(GL_LIGHTING)
# # ===============================================================
# #                     CAMERA SYSTEM
# # ===============================================================

# def setupCamera():
#     global CHEAT, flag_cam, TOGGLE_FOLLOW, temp_angle, theta

#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(fovY, 1.25, 0.1, 2500)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

#     # Base camera position (orbit camera)
#     target_cam_x = -camera_radius * math.sin(math.radians(camera_angle))
#     target_cam_y =  camera_radius * math.cos(math.radians(camera_angle))
#     target_cam_z =  camera_height

#     # Smooth interpolation
#     smoothing = 0.1

#     if not hasattr(setupCamera, "cx"):
#         setupCamera.cx = target_cam_x
#         setupCamera.cy = target_cam_y
#         setupCamera.cz = target_cam_z

#     setupCamera.cx = setupCamera.cx * (1 - smoothing) + target_cam_x * smoothing
#     setupCamera.cy = setupCamera.cy * (1 - smoothing) + target_cam_y * smoothing
#     setupCamera.cz = setupCamera.cz * (1 - smoothing) + target_cam_z * smoothing

#     cx = setupCamera.cx
#     cy = setupCamera.cy
#     cz = setupCamera.cz

#     # Cheat camera system
#     if CHEAT:
#         if flag_cam:
#             if TOGGLE_FOLLOW:
#                 angle = math.radians(theta)
#             else:
#                 angle = math.radians(temp_angle)

#             hand_x = p_x + 30 * (-math.sin(angle))
#             hand_y = p_y + 30 * ( math.cos(angle))
#             hand_z = p_z + 75

#             gluLookAt(
#                 p_x, p_y + 11, p_z + 101,
#                 hand_x, hand_y, hand_z,
#                 0, 0, 1
#             )
#         else:
#             gluLookAt(cx, cy, cz, 0, 0, 0, 0, 0, 1)
#     else:
#         if flag_cam:
#             angle = math.radians(theta)
#             hand_x = p_x + 30 * (-math.sin(angle))
#             hand_y = p_y + 30 * ( math.cos(angle))
#             hand_z = p_z + 75

#             gluLookAt(
#                 p_x, p_y + 11, p_z + 101,
#                 hand_x, hand_y, hand_z,
#                 0, 0, 1
#             )
#         else:
#             gluLookAt(cx, cy, cz, 0, 0, 0, 0, 0, 1)


# # ===============================================================
# #                     INPUT LISTENERS
# # ===============================================================

# def keyboardListener(key, x, y):
#     global p_x, p_y, p_z, theta, PLAY, PLAYER_LIFE
#     global GAME_SCORE, BULLET_MISSED, bullet
#     global NUM_ENEMIES, enemies, CHEAT, TOGGLE_FOLLOW, temp_angle

#     angle_rad = math.radians(theta)
#     step = 10

#     if PLAY:
#         if key == b'w':  # move forward
#             p_x += step * (-math.sin(angle_rad))
#             p_y += step * ( math.cos(angle_rad))
#         if key == b's':  # backward
#             p_x -= step * (-math.sin(angle_rad))
#             p_y -= step * ( math.cos(angle_rad))

#         # clamp within world
#         p_x = max(-TOTAL_LENGTH/2, min(TOTAL_LENGTH/2, p_x))
#         p_y = max(-TOTAL_LENGTH/2, min(TOTAL_LENGTH/2, p_y))

#         if key == b'a':
#             theta += 5
#             if theta >= 360:
#                 theta = 0
#         if key == b'd':
#             theta -= 5
#             if theta < 0:
#                 theta += 360

#         if key == b'c':
#             CHEAT = not CHEAT

#         if key == b'v':
#             TOGGLE_FOLLOW = not TOGGLE_FOLLOW
#             temp_angle = theta

#     if key == b'r':  # restart
#         PLAY = True
#         theta = 0
#         p_x = p_y = p_z = 0
#         PLAYER_LIFE = 5
#         GAME_SCORE = 0
#         BULLET_MISSED = 0
#         bullet = []

#         enemies.clear()
#         for i in range(NUM_ENEMIES):
#             enemies.append({
#                 "x": random.uniform(-TOTAL_LENGTH/2, TOTAL_LENGTH/2),
#                 "y": random.uniform(-TOTAL_LENGTH/2, TOTAL_LENGTH/2),
#                 "z": 0,
#                 "size": random.uniform(0.3, 1),
#                 "shrink": True
#             })


# def specialKeyListener(key, x, y):
#     global camera_angle, camera_height

#     if key == GLUT_KEY_LEFT:
#         camera_angle -= 1
#     if key == GLUT_KEY_RIGHT:
#         camera_angle += 1
#     if key == GLUT_KEY_UP:
#         camera_height += 5
#     if key == GLUT_KEY_DOWN:
#         camera_height -= 5


# def mouseListener(button, state, x, y):
#     global flag_cam, bullet, theta, PLAY

#     if PLAY:
#         if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#             angle = math.radians(theta)
#             bx = p_x + 30 * (-math.sin(angle))
#             by = p_y + 30 * ( math.cos(angle))
#             bullet.append({"x": bx, "y": by, "angle": angle})

#         if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#             flag_cam = not flag_cam


# # ===============================================================
# #                     GAME LOOP LOGIC
# # ===============================================================

# def idle():
#     global enemies, p_x, p_y, bullet, theta
#     global PLAYER_LIFE, GAME_SCORE, BULLET_MISSED, PLAY
#     global CHEAT, auto_fire_delay

#     speed = 0.01

#     # ---------------------------
#     #      CHEAT AUTO FIRE
#     # ---------------------------
#     if CHEAT:
#         theta += 1
#         if theta >= 360:
#             theta = 0

#         angle = math.radians(theta)

#         # cooldown
#         if auto_fire_delay > 0:
#             auto_fire_delay -= 1
#         else:
#             for e in enemies:
#                 dx = e["x"] - p_x
#                 dy = e["y"] - p_y
#                 enemy_angle = math.atan2(-dx, dy)

#                 diff = abs((enemy_angle - angle + math.pi) % (2*math.pi) - math.pi)

#                 if diff < math.radians(1):
#                     bx = p_x + 30 * (-math.sin(angle))
#                     by = p_y + 30 * ( math.cos(angle))
#                     bullet.append({"x": bx, "y": by, "angle": angle})
#                     auto_fire_delay = 50
#                     break

#     # ---------------------------
#     #         NORMAL GAMEPLAY
#     # ---------------------------
#     if PLAY:
#         # Enemy movement toward player
#         for e in enemies[:]:
#             dx = p_x - e["x"]
#             dy = p_y - e["y"]
#             dist = math.hypot(dx, dy)

#             if dist <= 15:
#                 PLAYER_LIFE -= 1

#                 enemies.remove(e)
#                 enemies.append({
#                     "x": random.uniform(-600, 600),
#                     "y": random.uniform(-600, 600),
#                     "z": 0,
#                     "size": random.uniform(0.3, 1),
#                     "shrink": True
#                 })

#                 if PLAYER_LIFE == 0:
#                     PLAY = False
#                 continue

#             if dist != 0:
#                 e["x"] += speed * dx / dist
#                 e["y"] += speed * dy / dist

#             # pulsation
#             if e["shrink"]:
#                 e["size"] -= 0.001
#                 if e["size"] <= 0.5:
#                     e["shrink"] = False
#             else:
#                 e["size"] += 0.001
#                 if e["size"] >= 1:
#                     e["shrink"] = True

#         # Move bullets
#         for b in bullet[:]:
#             b["x"] += 10 * (-math.sin(b["angle"]))
#             b["y"] += 10 * ( math.cos(b["angle"]))

#             if abs(b["x"]) > TOTAL_LENGTH/2 or abs(b["y"]) > TOTAL_LENGTH/2:
#                 bullet.remove(b)
#                 BULLET_MISSED += 1
#                 if BULLET_MISSED >= 10:
#                     PLAY = False

#         # Collision detection
#         for b in bullet[:]:
#             for e in enemies[:]:
#                 dx = e["x"] - b["x"]
#                 dy = e["y"] - b["y"]
#                 dist = math.hypot(dx, dy)

#                 if dist < 40:
#                     GAME_SCORE += 1

#                     # 💥 CREATE EXPLOSION HERE
#                     create_explosion(e["x"], e["y"], 40)

#                     bullet.remove(b)
#                     enemies.remove(e)

#                     enemies.append({
#                         "x": random.uniform(-600, 600),
#                         "y": random.uniform(-600, 600),
#                         "z": 0,
#                         "size": random.uniform(0.3, 1),
#                         "shrink": True
#                     })

#                     break

#     # ---------------------------
#     #   UPDATE EXPLOSIONS
#     # ---------------------------
#     for explosion in explosions[:]:
#         for p in explosion:
#             p["x"] += p["vx"]
#             p["y"] += p["vy"]
#             p["z"] += p["vz"]

#             p["vz"] -= 0.15  # gravity
#             p["life"] -= p["decay"]

#         if all(p["life"] <= 0 for p in explosion):
#             explosions.remove(explosion)

#     glutPostRedisplay()


# # ===============================================================
# #                          RENDERING
# # ===============================================================

# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     glViewport(0, 0, 1000, 800)

#     # sky first
#     draw_sky()

#     # camera
#     setupCamera()

#     # ground
#     draw_ground()

#     # player
#     human()

#     if PLAY:
#         draw_enemies()
#         draw_bullet()
#         draw_explosions()

#         draw_text(10, 770, f"Player Life: {PLAYER_LIFE}")
#         draw_text(10, 740, f"Score: {GAME_SCORE}")
#         draw_text(10, 710, f"Misses: {BULLET_MISSED}")
#     else:
#         draw_text(10, 770, f"GAME OVER – Final Score: {GAME_SCORE}")
#         draw_text(10, 740, "Press 'R' to Restart")

#     glutSwapBuffers()
# # ===============================================================
# #                        LIGHTING
# # ===============================================================

# def initLighting():
#     glEnable(GL_LIGHTING)
#     glEnable(GL_LIGHT0)

#     # Soft white light from above
#     light_pos = [0, 0, 300, 1]
#     glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

#     diffuse = [0.9, 0.9, 0.9, 1.0]
#     ambient = [0.4, 0.4, 0.4, 1.0]
#     glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
#     glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)

#     glEnable(GL_COLOR_MATERIAL)
#     glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


# # ===============================================================
# #                     OPENGL INITIALIZATION
# # ===============================================================

# def init():
#     glClearColor(0.5, 0.8, 1.0, 1.0)  # sky blue
#     glEnable(GL_DEPTH_TEST)
#     initLighting()


# # ===============================================================
# #                           MAIN
# # ===============================================================

# def main():
#     glutInit()
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
#     glutInitWindowSize(1000, 800)
#     glutCreateWindow(b"3D Survival Shooter (Enhanced + Explosions)")

#     init()

#     glutDisplayFunc(showScreen)
#     glutIdleFunc(idle)

#     glutKeyboardFunc(keyboardListener)
#     glutSpecialFunc(specialKeyListener)
#     glutMouseFunc(mouseListener)

#     glutMainLoop()


# if __name__ == "__main__":
#     main()
# Made by

# 22301068 - Mushfique Tajwar
# 22301130 - Aryan Rayeen Rahman
# 22301327 - Md. Obaidullah Ahrar

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Setup
GRID_LENGTH       = 1500
region            = 600
castle_region     = 250

# Camera
camera_position   = (0, 600, 600)
camera_angle      = 0
camera_distance   = 600
camera_height     = 550
camera_min_height = 400
camera_max_height = 1400

# Flags
cheat             = False
v_enable          = False
game_end          = False
round_pause       = False
round_choice_made = False
first_person_view = False

# Player
player_position   = [0, 0, 0]
player_speed      = 10
player_score      = 0
player_health     = 100
player_rotation   = 5
player_max_health = 100

# Gun
gun_rotation      = 180
gun_position      = [30, 15, 80]
shots             = []
misses            = 0
max_miss          = 50

# Target
targets           = []
target_number     = 5
target_speed      = 0.025
target_pulse      = 1.0
target_pulse_t    = 0
enemy_count_per_round = [5, 7, 9, 11, 13, 15, 17, 19, 21]

# Enemy shots
enemy_shots       = []
enemy_shot_timer  = {}
enemy_shot_damage = 1
enemy_shot_cooldown = 300

# Tower shots
towers            = []
tower_shots       = []
tower_shot_timers = {}
tower_shot_range  = 600
tower_shot_damage = 3
tower_shot_cooldown = 200

current_round     = 1
castle_radius     = 60
enemies_killed    = 0
kills_to_advance  = 10

tower_placement_mode = False
placement_marker_position = [400, 400]
GLUT_BITMAP_HELVETICA_18 = GLUT_BITMAP_HELVETICA_18
tree_count = 0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 650)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(font, ord(character))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():
    arena()
    castle()
    draw_trees()
    for tx, ty in towers:
        glPushMatrix()
        glTranslatef(tx, ty, 10)

        # Base Cylinder Tower
        glColor3f(0.5, 0.5, 0.5)
        gluCylinder(gluNewQuadric(), 40, 45, 180, 20, 20)

        # Top Battlements
        glTranslatef(0, 0, 180)
        for i in range(8):
            angle = i * 45
            x = 50 * math.cos(math.radians(angle))
            y = 50 * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, y, 0)
            glRotatef(angle, 0, 0, 1)
            glColor3f(0.4, 0.4, 0.4)
            glScalef(1, 1, 1.5)
            glutSolidCube(15)
            glPopMatrix()

        # Flagpole
        glColor3f(0.6, 0.3, 0.1)
        gluCylinder(gluNewQuadric(), 1.5, 1.5, 40, 10, 10)

        # Flag
        glTranslatef(0, 0, 40)
        glColor3f(1, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(20, 8, 0)
        glVertex3f(0, 16, 0)
        glEnd()
        glPopMatrix()

    if not game_end:
        for t in targets:
            enemies(*t)
        for s in shots:
            bullets(s[0], s[1], s[2])
        for es in enemy_shots:
            enemy_bullet(es[0], es[1], es[2])
        for ts in tower_shots:
            tower_bullet(ts[0], ts[1], ts[2])

def arena():
    # Draw arena floor
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH + 1, 100):
        for j in range(-GRID_LENGTH, GRID_LENGTH + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(0, 0.2, 0)
            else:
                glColor3f(0, 0.3, 0)
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)
    glEnd()

    # Draw conquered region
    glBegin(GL_QUADS)
    for i in range(-region, region + 1, 100):
        for j in range(-region, region + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(0, 0.4, 0)
            else:
                glColor3f(0, 0.5, 0)
            glVertex3f(i, j, 2)
            glVertex3f(i + 100, j, 2)
            glVertex3f(i + 100, j + 100, 2)
            glVertex3f(i, j + 100, 2)
    glEnd()

    # Draw castle region
    glBegin(GL_QUADS)
    for i in range(-castle_region, castle_region, 100):
        for j in range(-castle_region, castle_region, 100):
            if (i + j) % 200 == 0:
                glColor3f(0.8, 0.8, 0.8)
            else:
                glColor3f(1, 1, 1)
            glVertex3f(i, j, 9)
            glVertex3f(i + 100, j, 9)
            glVertex3f(i + 100, j + 100, 9)
            glVertex3f(i, j + 100, 9)
    glEnd()
    # Boundary

    glBegin(GL_QUADS)
    glColor3f(0, 0, 0)

    glVertex3f(-region, -region, 0)
    glVertex3f(-region, region + 100, 0)
    glVertex3f(-region, region + 100, 30)
    glVertex3f(-region, -region, 30)

    glVertex3f(region + 100, -region, 0)
    glVertex3f(region + 100, region + 100, 0)
    glVertex3f(region + 100, region + 100, 30)
    glVertex3f(region + 100, -region, 30)

    glVertex3f(-region, region + 100, 0)
    glVertex3f(region + 100, region + 100, 0)
    glVertex3f(region + 100, region + 100, 30)
    glVertex3f(-region, region + 100, 30)

    glVertex3f(-region, -region, 0)
    glVertex3f(region + 100, -region, 0)
    glVertex3f(region + 100, -region, 30)
    glVertex3f(-region, -region, 30)
    glEnd()
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)

    # Walls
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH + 100, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH + 100, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)

    glVertex3f(GRID_LENGTH + 100, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH + 100, GRID_LENGTH + 100, 0)
    glVertex3f(GRID_LENGTH + 100, GRID_LENGTH + 100, 100)
    glVertex3f(GRID_LENGTH + 100, -GRID_LENGTH, 100)

    glVertex3f(-GRID_LENGTH, GRID_LENGTH + 100, 0)
    glVertex3f(GRID_LENGTH + 100, GRID_LENGTH + 100, 0)
    glVertex3f(GRID_LENGTH + 100, GRID_LENGTH + 100, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH + 100, 100)

    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH + 100, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH + 100, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()

def draw_trees():
    rng = random.Random(42)
    tree_count = 70
    for i in range(tree_count):
        x = rng.randint(-GRID_LENGTH + 200, GRID_LENGTH - 200)
        y = rng.randint(-GRID_LENGTH + 200, GRID_LENGTH - 200)
        if math.sqrt(x**2 + y**2) >= 500:
            glPushMatrix()
            glTranslatef(x, y, 0)
            glColor3f(0.4*i/70, 0.2*i/70, 0.1)
            gluCylinder(gluNewQuadric(), 12, 12, 70, 10, 10)
            glTranslatef(0, 0, 70)
            glColor3f(0.0, 0.6*i/70, 0.0)
            gluSphere(gluNewQuadric(), 40, 15, 15)
            glPopMatrix()

def castle():
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    for dx, dy in [(-60, -60), (60, -60), (-60, 60), (60, 60)]:
        glPushMatrix()
        glTranslatef(dx, dy, 0)
        glScalef(1, 1, 2)
        glutSolidCube(100)
        glPopMatrix()
    glPopMatrix()
    glColor3f(0.6, 0.6, 0.6)
    for dx, dy in [(-100, 0), (100, 0), (0, -100), (0, 100)]:
        glPushMatrix()
        glTranslatef(dx, dy, 50)
        glScalef(1.2, 1.2, 2.2)
        glutSolidCube(60)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(dx, dy, 120)
        for i in range(8):
            angle = i * 45
            x = 35 * math.cos(math.radians(angle))
            y = 35 * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, y, 0)
            glColor3f(0.5, 0.5, 0.5)
            glutSolidCube(12)
            glPopMatrix()
        glPopMatrix()
    glColor3f(1, 0, 0)  # Red flags
    for dx, dy in [(-100, 0), (100, 0), (0, -100), (0, 100)]:
        glPushMatrix()
        glTranslatef(dx, dy, 150)
        # Flag pole
        glColor3f(0.6, 0.3, 0.1)
        gluCylinder(gluNewQuadric(), 1.5, 1.5, 40, 10, 10)
        # Flag
        glTranslatef(0, 0, 40)
        glColor3f(1, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(25, 10, 0)
        glVertex3f(0, 20, 0)
        glEnd()
        glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glColor3f(0.4, 0.4, 0.9)
    gluCylinder(gluNewQuadric(), 40, 50, 200, 20, 20)
    glTranslatef(0, 0, 200)
    for i in range(12):
        angle = i * 30
        x = 50 * math.cos(math.radians(angle))
        y = 50 * math.sin(math.radians(angle))
        glPushMatrix()
        glTranslatef(x, y, 0)
        glColor3f(0.5, 0.5, 0.6)
        glutSolidCube(12)
        glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,0,200)
    glRotatef(gun_rotation, 0, 0, 1)
    # Legs
    glTranslatef(0, 0, 0)
    glColor3f(0.1, 0.1, 0.7)
    gluCylinder(gluNewQuadric(), 6, 12, 45, 10, 10)
    glTranslatef(30, 0, 0)
    glColor3f(0.1, 0.1, 0.7)
    gluCylinder(gluNewQuadric(), 6, 12, 45, 10, 10)
    # Body
    glTranslatef(-15, 0, 70)
    glColor3f(0.7, 0.7, 0)
    glutSolidCube(40)
    # Head
    glTranslatef(0, 0, 40)
    glColor3f(0.95, 0.85, 0.75)
    gluSphere(gluNewQuadric(), 20, 12, 12)
    # Arms
    glTranslatef(20, -60, -30)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.95, 0.85, 0.75)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    glRotatef(90, 1, 0, 0)
    glTranslatef(-45, 60, -40)
    glRotatef(0, 1, 0, 0)
    glColor3f(0.95, 0.85, 0.75)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    # Hat
    glColor3f(1, 1, 0)
    glTranslatef(25, 0, 87)
    glutSolidCone(12, 40, 16, 16)  # Base radius = 12, height = 40
    glTranslatef(-10, -15, -17)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 5, 12, 12)
    glTranslatef(20, 0, 0)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 5, 12, 12)
    glPopMatrix()

def spawn_tower():
    while True:
        x = random.randint(-region + 100, region - 100)
        y = random.randint(-region + 100, region - 100)
        if math.sqrt(x**2 + y**2) > 200:  # Avoid center
            return (x, y)

def enemies(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z + 35)
    if not round_pause:
        glScalef(target_pulse, target_pulse, target_pulse)
    # Lower Body (Upside-down Cone)
    glColor3f(0, 0, abs(target_pulse))
    glPushMatrix()
    glTranslatef(0,0,35)
    glRotatef(180, 1, 0, 0)  # Rotate the cone upside down
    glutSolidCone(25, 70, 16, 16)  # Base radius = 35, height = 50
    glPopMatrix()
    # Head
    glTranslatef(0, 0, 50)
    glColor3f(0, 0, 0)  # Black color for the head
    gluSphere(gluNewQuadric(), 15, 12, 12)
    # Hat
    glPushMatrix()
    glColor3f(0.5, 0, 0)  # Red color for the hat
    glTranslatef(0, 0, 20)
    glutSolidCone(12, 40, 16, 16)  # Base radius = 12, height = 40
    glPopMatrix()
    glPopMatrix()

def bullets(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 0.5, 0)
    glutSolidCube(8)
    glPopMatrix()

def tower_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0, 0.7, 1)  # Blue color for tower bullets
    glutSolidCone(4, 12, 8, 8)  # Cone shape for tower bullets
    glPopMatrix()

def enemy_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 0, 0)  # Red color for enemy bullets
    glutSolidSphere(5, 8, 8)  # Sphere for enemy bullets
    glPopMatrix()

def shoot():
    global shots
    if first_person_view:
        ang = math.radians(gun_rotation + 45)
        x = player_position[0] + (gun_position[0] + 5) * \
            math.sin(ang) - gun_position[1] * math.cos(ang)
        y = player_position[1] - (gun_position[0] + 5) * \
            math.cos(ang) - gun_position[1] * math.sin(ang)
        z = player_position[2] + gun_position[2]
        shot = [x, y, z, gun_rotation]
    else:
        ang = math.radians(gun_rotation - 90)
        off_x = gun_position[0] * \
            math.cos(ang) - gun_position[1] * math.sin(ang)
        off_y = gun_position[0] * \
            math.sin(ang) + gun_position[1] * math.cos(ang)
        x = player_position[0] + off_x
        y = player_position[1] + off_y
        z = player_position[2] + gun_position[2]
        shot = [x, y, z, gun_rotation]
    shots.append(shot)

def gun_shot_check():
    global shots, misses, targets, game_end
    if round_pause:
        return
    to_remove = []
    for s in shots:
        ang = math.radians(s[3] - 90)
        s[0] += 2 * math.cos(ang)
        s[1] += 2 * math.sin(ang)
        if (s[0] > region + 100 or s[0] < -region or
                s[1] > region + 100 or s[1] < -region):
            to_remove.append(s)
            if not cheat:
                misses += 1
    for s in to_remove:
        if s in shots:
            shots.remove(s)
    if misses >= max_miss:
        game_end = True

def enemy_shoot(x, y, z):
    global enemy_shots
    dx = player_position[0] - x
    dy = player_position[1] - y
    ang = math.atan2(dy, dx)
    ang += random.uniform(-0.1, 0.1)
    enemy_shots.append([x, y, z + 70, ang])

def update_enemies():
    global targets, player_health, game_end, target_speed, enemy_shot_timer
    if round_pause:
        return
    for t in targets:
        enemy_id = id(t)
        if enemy_id not in enemy_shot_timer:
            enemy_shot_timer[enemy_id] = random.randint(
                60, enemy_shot_cooldown)
    for t in targets[:]:
        dx = player_position[0] - t[0]
        dy = player_position[1] - t[1]
        dist = math.sqrt(dx*dx + dy*dy)
        enemy_id = id(t)
        if enemy_id in enemy_shot_timer:
            enemy_shot_timer[enemy_id] -= 1
            if enemy_shot_timer[enemy_id] <= 0 and not cheat:
                enemy_shoot(t[0], t[1], t[2])
                enemy_shot_timer[enemy_id] = enemy_shot_cooldown + \
                    random.randint(-30, 30)
        if dist < 50:
            if not cheat:
                player_health -= 5
                if player_health <= 0:
                    game_end = True
                    targets.clear()
                    shots.clear()
                    enemy_shots.clear()
                    break
            if t in targets:
                targets.remove(t)
                if enemy_id in enemy_shot_timer:
                    del enemy_shot_timer[enemy_id]
            spawn_enemies(1)
        else:
            ang = math.atan2(dy, dx)
            t[0] += target_speed * math.cos(ang)
            t[1] += target_speed * math.sin(ang)
    timer_keys = list(enemy_shot_timer.keys())
    for enemy_id in timer_keys:
        if not any(id(t) == enemy_id for t in targets):
            del enemy_shot_timer[enemy_id]
    if not targets:
        next_round()

def detect_target_hits():
    global shots, targets, player_score, enemies_killed
    if round_pause:
        return
    for s in shots[:]:
        s_x, s_y = s[0], s[1]
        for t in targets[:]:
            t_x, t_y = t[0], t[1]
            dx, dy = s_x - t_x, s_y - t_y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= 70:
                player_score += 1
                enemies_killed += 1
                if s in shots:
                    shots.remove(s)
                if t in targets:
                    targets.remove(t)
                max_enemies = (
                    enemy_count_per_round[current_round-1]
                    if current_round <= len(enemy_count_per_round)
                    else enemy_count_per_round[-1] + 2 * (current_round - len(enemy_count_per_round))
                )
                if enemies_killed >= kills_to_advance:
                    next_round()
                elif len(targets) < max_enemies:
                    spawn_enemies(1)
                break

def tower_shoot(tower_idx, tx, ty):
    global tower_shots, targets
    closest_enemy = None
    min_dist = tower_shot_range
    for t in targets:
        dx = tx - t[0]
        dy = ty - t[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < min_dist:
            min_dist = dist
            closest_enemy = t
    if closest_enemy:
        ex, ey, _ = closest_enemy
        dx = ex - tx
        dy = ey - ty
        ang = math.atan2(dy, dx)
        ang += random.uniform(-0.05, 0.05)
        tower_shots.append([tx, ty, 160, ang])
        return True
    return False

def update_towers():
    global tower_shot_timers, towers
    if round_pause:
        return
    for i, (tx, ty) in enumerate(towers):
        if i in tower_shot_timers:
            tower_shot_timers[i] -= 1
            if tower_shot_timers[i] <= 0:
                if tower_shoot(i, tx, ty):
                    tower_shot_timers[i] = tower_shot_cooldown
                else:
                    tower_shot_timers[i] = 60
        else:
            tower_shot_timers[i] = random.randint(60, tower_shot_cooldown)

def update_tower_shots():
    global tower_shots, targets, player_score, enemies_killed
    if round_pause:
        return
    to_remove_shots = []
    to_remove_targets = []
    for shot in tower_shots:
        shot[0] += 3 * math.cos(shot[3])
        shot[1] += 3 * math.sin(shot[3])
        if (shot[0] > region + 100 or shot[0] < -region or
                shot[1] > region + 100 or shot[1] < -region):
            to_remove_shots.append(shot)
            continue
        for t in targets:
            if t in to_remove_targets:
                continue
            dx = shot[0] - t[0]
            dy = shot[1] - t[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 40:
                player_score += 1
                enemies_killed += 1
                to_remove_shots.append(shot)
                to_remove_targets.append(t)
                break
    for shot in to_remove_shots:
        if shot in tower_shots:
            tower_shots.remove(shot)
    for t in to_remove_targets:
        if t in targets:
            targets.remove(t)
            if enemies_killed >= kills_to_advance:
                next_round()
            else:
                max_enemies = (
                    enemy_count_per_round[current_round-1]
                    if current_round <= len(enemy_count_per_round)
                    else enemy_count_per_round[-1] + 2 * (current_round - len(enemy_count_per_round))
                )
                if len(targets) < max_enemies:
                    spawn_enemies(1)

def enemy_pulse():
    global target_pulse_t, target_pulse
    target_pulse_t += 0.01
    target_pulse = 1.0 + 0.4 * math.cos(target_pulse_t)

def enemy_angle():
    angles = []
    for t in targets:
        dx, dy = player_position[0] - t[0], player_position[1] - t[1]
        ang = math.degrees(math.atan2(dy, dx)) - 90
        angles.append((ang + 360) % 360)
    return angles

def crosshair():
    if v_enable:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 650)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(400, 340)
        glVertex2f(400, 310)
        glVertex2f(380, 325)
        glVertex2f(400, 340)
        glVertex2f(420, 325)
        glVertex2f(400, 340)
        glEnd()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def spawn_enemies(count=target_number):
    global targets, n
    max_enemies = enemy_count_per_round[current_round - 1] if current_round <= len(enemy_count_per_round) else 15
    if len(targets) + count > max_enemies:
        count = max(0, max_enemies - len(targets))
    if current_round < 4:
        n = current_round
    for _ in range(count):
        x = random.uniform(-region + 50, region - 50)
        y = random.uniform(-region + 50, region - 50)
        z = random.uniform(0, 10)
        while abs(x) < 200:
            x = random.uniform(-region + (100*n), region - 100)
        while abs(y) < 200:
            y = random.uniform(-region + (100*n), region - 100)
        targets.append([x, y, z])

def update_enemy_shots():
    global enemy_shots, player_health, game_end
    if round_pause:
        return
    to_remove = []
    for shot in enemy_shots:
        shot[0] += 1.5 * math.cos(shot[3])
        shot[1] += 1.5 * math.sin(shot[3])
        if (shot[0] > GRID_LENGTH + 100 or shot[0] < -GRID_LENGTH or shot[1] > GRID_LENGTH + 100 or shot[1] < -GRID_LENGTH):
            to_remove.append(shot)
            continue
        dx = player_position[0] - shot[0]
        dy = player_position[1] - shot[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < castle_radius:
            if not cheat:
                player_health -= enemy_shot_damage
                if player_health <= 0:
                    game_end = True
                    targets.clear()
                    shots.clear()
                    enemy_shots.clear()
            to_remove.append(shot)
    for shot in to_remove:
        if shot in enemy_shots:
            enemy_shots.remove(shot)

def next_round():
    global current_round, castle_radius, target_number, enemies_killed, region, round_pause, target_speed
    global player_health, player_max_health, kills_to_advance
    current_round += 1
    enemies_killed = 0
    target_speed += 0.25
    round_pause = True
    kills_to_advance += 10
    player_health = player_max_health
    if current_round < 5:
        castle_radius += 20
        region += 300
    if current_round <= len(enemy_count_per_round):
        target_number = enemy_count_per_round[current_round-1]
    else:
        target_number = enemy_count_per_round[-1] + 2 * (current_round - len(enemy_count_per_round))

def reset_game():
    global game_end, first_person_view, cheat, v_enable, misses, region, towers, target_speed, current_round
    global player_health, player_max_health, player_score, player_position, gun_rotation, castle_radius
    global tower_shots, tower_shot_timers, round_pause, round_choice_made, kills_to_advance, enemies_killed
    game_end, first_person_view = False, False
    cheat, v_enable, round_pause, round_choice_made = False, False, False, False
    player_position = [0, 0, 0]
    towers = []
    region = 600
    player_max_health = 100
    target_speed = 0.025
    current_round = 1
    enemies_killed = 0
    castle_radius = 60
    kills_to_advance  = 10
    gun_rotation, player_health, player_max_health, player_score, misses = 180, 100, 100, 0, 0
    shots.clear()
    targets.clear()
    tower_shots.clear()
    tower_shot_timers.clear()
    spawn_enemies()

def keyboardListener(key, x, y):
    global cheat, first_person_view, game_end, v_enable, gun_rotation,camera_position, camera_angle
    global player_position, player_speed, player_rotation, player_health, player_max_health, player_score, misses
    global round_pause, round_choice_made, towers, tower_shot_timers, tower_placement_mode, placement_marker_position
    if round_pause:
        if tower_placement_mode:
            if key == b's' and placement_marker_position[1] < region - 50:
                placement_marker_position[1] += 50
            elif key == b'w' and placement_marker_position[1] > -region + 50:
                placement_marker_position[1] -= 50
            elif key == b'd' and placement_marker_position[0] > -region + 50:
                placement_marker_position[0] -= 50
            elif key == b'a' and placement_marker_position[0] < region - 50:
                placement_marker_position[0] += 50
            elif key == b'\r':
                if (abs(placement_marker_position[0]) > castle_region or
                        abs(placement_marker_position[1]) > castle_region):
                    if len(towers) < 5:
                        towers.append(tuple(placement_marker_position))
                        tower_shot_timers[len(towers)-1] = random.randint(60, tower_shot_cooldown)
                    tower_placement_mode = False
                    round_pause = False
                    round_choice_made = True
                    first_person_view = not first_person_view
                    v_enable = first_person_view
                    player_rotation = 2.5 if first_person_view else 5
                    spawn_enemies(target_number)
                    
            return

        if key == b'1':
            spawn_enemies(target_number)
            player_max_health += 100
            player_health = player_max_health
            round_pause = False
            round_choice_made = True
            return
        elif key == b'2':
            if current_round > 4:
                round_choice_made = True
                return
            tower_placement_mode = True
            placement_marker_position = [400, 400]
            first_person_view = False
            v_enable = False
            player_rotation = 2.5 if first_person_view else 5
            camera_position, camera_angle = (0, 600, 600), 0
            return
        return

    if game_end and key != b'r':
        return
    elif key == b'c' and cheat == True:
        shots.clear()
        cheat = False
    elif key == b'v':
        if first_person_view and cheat:
            v_enable = not v_enable
    elif key == b'r' and game_end:
        reset_game()
    if key == b'p':
        player_health = 1000
    gun_rotation %= 360
    if key == b'd':
        gun_rotation -= 5
    if key == b'a':
        gun_rotation += 5

def specialKeyListener(key, x, y):
    global camera_angle, camera_distance, camera_height, camera_min_height, camera_max_height
    if not game_end:
        if key == GLUT_KEY_UP:
            if camera_height > camera_min_height:
                camera_height -= 20
        elif key == GLUT_KEY_DOWN:
            if camera_height < camera_max_height:
                camera_height += 20
        elif key == GLUT_KEY_LEFT:
            camera_angle -= 5
        elif key == GLUT_KEY_RIGHT:
            camera_angle += 5

def mouseListener(button, state, x, y):
    global first_person_view, player_rotation, v_enable, game_end
    if game_end:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and cheat == False:
        shoot()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_view = not first_person_view
        v_enable = first_person_view
        player_rotation = 2.5 if first_person_view else 5

def setupCamera():
    global camera_position, camera_angle, camera_distance, camera_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100, 1.25, 0.3, 2700)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if first_person_view:
        angle = math.radians(gun_rotation)
        eye_x = player_position[0] + (gun_position[0]*1.2 *math.sin(angle)) - (gun_position[1]*0.6*math.cos(angle))
        eye_y = player_position[1] - (gun_position[0]*1.2 *math.cos(angle)) - (gun_position[1]*0.6*math.sin(angle))
        eye_z = player_position[2] + gun_position[2] + 200
        cen_x = eye_x - math.sin(-angle) * 100
        cen_y = eye_y - math.cos(-angle) * 100
        cen_z = eye_z
        gluLookAt(eye_x, eye_y, eye_z + 50, cen_x, cen_y, cen_z - 30, 0, 0, 1)
    else:
        angle = math.radians(camera_angle)
        x = camera_distance * math.sin(angle)
        y = camera_distance * math.cos(angle)
        z = camera_height
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)
        
def idle():
    global player_score
    enemy_pulse()
    if round_pause:
        targets.clear()
        glutPostRedisplay()
        return
    if not game_end:
        update_enemies()
        update_enemy_shots()
        update_towers()
        update_tower_shots()
        gun_shot_check()
        detect_target_hits()
    glutPostRedisplay()

def draw_gradient_background():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 650)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(0.63, 0.81, 0.98)
    glVertex2f(0, 650)
    glVertex2f(800, 650)
    glColor3f(0.07, 0.11, 0.21)
    glVertex2f(800, 0)
    glVertex2f(0, 0)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def showScreen():
    global game_end, player_health, player_max_health, player_score, misses, round_pause, tower_placement_mode
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 800, 650)
    draw_gradient_background()
    setupCamera()
    draw_shapes()
    if v_enable:
        crosshair()
    if round_pause:
        if tower_placement_mode:
            glPushMatrix()
            glTranslatef(placement_marker_position[0], placement_marker_position[1], 10)
            glScalef(target_pulse, target_pulse, target_pulse)
            glColor3f(0, 1, 1)
            glutSolidSphere(20, 16, 16)
            glPopMatrix()
            draw_text(200, 400, "Use W, A, S, D to move the marker", color=(1, 1, 0))
            draw_text(200, 350, "Press Enter to place the tower (Can't place on white tiles)", color=(0, 1, 0))
        else:
            if current_round < 5:
                draw_text(200, 400, f"Round {current_round-1} Completed! More region conquered and health restored.", color=(1, 1, 0))
                draw_text(200, 350, "Choose your reward:", color=(1, 0.7, 0.2))
                draw_text(200, 300, "Press [1] to increase base castle health by 100", color=(0, 1, 0))
                draw_text(200, 250, "Press [2] to add an archer tower inside the region", color=(0, 0.7, 1))
                draw_text(200, 200, "A new wave of invaders are coming and they are faster!!!", color=(1, 0, 0))
            else:
                draw_text(200, 400, f"Round {current_round-1} Completed! Max health increased by 100", color=(1, 1, 0))
                draw_text(200, 300, "Press [1] to continue", color=(0, 1, 0))
                draw_text(200, 250, "A new wave of invaders are coming and they are faster!!!", color=(1, 0, 0))
    elif not game_end:
        draw_text(10, 650 - 25, f"Castle Health: {player_health}/{player_max_health}", color=(0, 0, 0))
        draw_text(10, 650 - 55, f"Player Score: {player_score}")
        draw_text(10, 650 - 85, f"Shots Missed: {misses}")
        draw_text(350, 625, f"Round {current_round}", color=(0, 0, 0))
        remaining = kills_to_advance - enemies_killed
        color = (1, 0, 0) if remaining > 5 else (1, 0.5, 0) if remaining > 2 else (0, 1, 0)
        draw_text(580, 650 - 25, f"Enemies to Kill: {remaining}", color=(0, 0, 0))
        draw_text(580, 650 - 55, f"Total Enemies: {len(targets)}")
    else:
        draw_text(10, 650 - 25, f"Game Over! Your Score is {player_score}")
        draw_text(10, 650 - 55, 'Press "R" to RESTART the Game')
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 650)
glutCreateWindow(b"Tower Defense")
spawn_enemies()
glutDisplayFunc(showScreen)
glutIdleFunc(idle)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()

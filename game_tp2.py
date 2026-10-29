"""Devoir TP2: le jeu du TP1 reecrit en POO (memes regles, memes valeurs).

Lancer:  py game_tp2.py
Controles: fleches = bouger | ESPACE = tirer (visee auto) | R = rejouer | ECHAP = quitter

Classes (une responsabilite chacune):
  Player        -> le joueur (position, vie, deplacement)
  Monster       -> le monstre (position, vie, vitesse, poursuite)
  Bullet        -> une balle (position, direction, deplacement)
  GameBoard     -> les regles (tir, collisions, score, etat de la partie)
  GameRenderer  -> tout l'affichage
"""

import math
import random
import sys

import pygame

WIDTH, HEIGHT, FPS = 800, 600, 60


# ======================================================================
# Player
# ======================================================================
class Player:
    SIZE = 40
    SPEED = 5
    MAX_HEALTH = 100

    def __init__(self):
        self.x, self.y = 150, 275
        self.health = self.MAX_HEALTH

    @property
    def center(self):
        return self.x + self.SIZE / 2, self.y + self.SIZE / 2

    def handle_input(self, keys):
        """Meme logique que le TP1: on ne bouge que si on reste dans l'ecran."""
        if keys[pygame.K_LEFT] and self.x - self.SPEED >= 0:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT] and self.x + self.SPEED <= WIDTH - self.SIZE:
            self.x += self.SPEED
        if keys[pygame.K_UP] and self.y - self.SPEED >= 0:
            self.y -= self.SPEED
        if keys[pygame.K_DOWN] and self.y + self.SPEED <= HEIGHT - self.SIZE:
            self.y += self.SPEED

    def take_damage(self, amount):
        self.health -= amount

    @property
    def is_dead(self):
        return self.health <= 0


# ======================================================================
# Monster
# ======================================================================
class Monster:
    SIZE = 50
    MAX_HEALTH = 100
    START_SPEED = 2.0
    SPEED_BONUS = 0.2          # le monstre accelere apres chaque mort

    def __init__(self):
        self.x, self.y = 700, 275
        self.health = self.MAX_HEALTH
        self.speed = self.START_SPEED

    @property
    def center(self):
        return self.x + self.SIZE / 2, self.y + self.SIZE / 2

    def chase(self, target_x, target_y):
        dx, dy = target_x - self.x, target_y - self.y
        distance = math.hypot(dx, dy)
        if distance > 1:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def contains(self, px, py):
        return self.x < px < self.x + self.SIZE and self.y < py < self.y + self.SIZE

    def take_hit(self, damage):
        """Retourne True si le monstre meurt."""
        self.health -= damage
        return self.health <= 0

    def respawn(self):
        """Nouveau monstre hors de l'ecran a droite, un peu plus rapide."""
        self.health = self.MAX_HEALTH
        self.x = WIDTH + 50
        self.y = random.randint(50, HEIGHT - 100)
        self.speed += self.SPEED_BONUS


# ======================================================================
# Bullet
# ======================================================================
class Bullet:
    SPEED = 10
    RADIUS = 5
    DAMAGE = 25

    def __init__(self, x, y, vx, vy):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def off_screen(self):
        return self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0


# ======================================================================
# GameBoard: les regles du jeu (aucun dessin ici)
# ======================================================================
class GameBoard:
    WIN_SCORE = 5

    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.monster = Monster()
        self.bullets = []
        self.score = 0
        self.state = "PLAYING"            # PLAYING / GAME_OVER / WIN

    def fire(self):
        """Tir avec visee automatique vers le centre du monstre."""
        if self.state != "PLAYING":
            return
        bx, by = self.player.center
        mx, my = self.monster.center
        dx, dy = mx - bx, my - by
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.bullets.append(Bullet(bx, by,
                                       dx / distance * Bullet.SPEED,
                                       dy / distance * Bullet.SPEED))

    def update(self):
        if self.state != "PLAYING":
            return

        # le monstre poursuit le joueur
        self.monster.chase(self.player.x, self.player.y)

        # contact monstre / joueur
        if (abs(self.player.x - self.monster.x) < 40
                and abs(self.player.y - self.monster.y) < 40):
            self.player.take_damage(1)
            if self.player.is_dead:
                self.state = "GAME_OVER"

        # balles
        for bullet in list(self.bullets):
            bullet.update()
            if bullet.off_screen():
                self.bullets.remove(bullet)
            elif self.monster.contains(bullet.x, bullet.y):
                self.bullets.remove(bullet)
                if self.monster.take_hit(Bullet.DAMAGE):
                    self.score += 1
                    self.monster.respawn()

        if self.score >= self.WIN_SCORE:
            self.state = "WIN"


# ======================================================================
# GameRenderer: tout l'affichage
# ======================================================================
class GameRenderer:
    BG_COLOR = (30, 30, 40)
    GRID_COLOR = (45, 45, 60)
    PLAYER_COLOR = (50, 205, 50)
    MONSTER_COLOR = (220, 20, 60)
    BULLET_COLOR = (255, 215, 0)
    TEXT_COLOR = (255, 255, 255)

    def __init__(self):
        self.font_small = pygame.font.SysFont("arial", 20)
        self.font_large = pygame.font.SysFont("arial", 40)

    def draw(self, screen, board):
        self._background(screen)
        if board.state == "PLAYING":
            self._playing(screen, board)
        elif board.state == "GAME_OVER":
            self._message(screen, "GAME OVER - MONSTER GOT YOU!", (255, 50, 50),
                          "Press 'R' to Restart or 'ESC' to Quit")
        else:
            self._message(screen, "YOU WIN! SURVIVED!", (50, 255, 50),
                          "Press 'R' to Play Again or 'ESC' to Quit")

    def _background(self, screen):
        screen.fill(self.BG_COLOR)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, self.GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, self.GRID_COLOR, (0, y), (WIDTH, y))

    def _health_bar(self, screen, x, y, width, current_hp, max_hp):
        ratio = max(0, current_hp / max_hp)
        pygame.draw.rect(screen, (100, 100, 100), (x, y - 12, width, 6))
        pygame.draw.rect(screen, (0, 255, 0), (x, y - 12, width * ratio, 6))

    def _playing(self, screen, board):
        for b in board.bullets:
            pygame.draw.circle(screen, self.BULLET_COLOR, (int(b.x), int(b.y)), Bullet.RADIUS)

        p = board.player
        pygame.draw.rect(screen, self.PLAYER_COLOR, (p.x, p.y, Player.SIZE, Player.SIZE),
                         border_radius=8)
        self._health_bar(screen, p.x, p.y, Player.SIZE, p.health, Player.MAX_HEALTH)

        m = board.monster
        pygame.draw.rect(screen, self.MONSTER_COLOR, (m.x, m.y, Monster.SIZE, Monster.SIZE),
                         border_radius=8)
        self._health_bar(screen, m.x, m.y, Monster.SIZE, m.health, Monster.MAX_HEALTH)

        score = self.font_small.render(f"Score: {board.score} / {board.WIN_SCORE}",
                                       True, self.TEXT_COLOR)
        screen.blit(score, (20, 20))

    def _message(self, screen, text, color, hint):
        big = self.font_large.render(text, True, color)
        small = self.font_small.render(hint, True, self.TEXT_COLOR)
        screen.blit(big, (WIDTH // 2 - big.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(small, (WIDTH // 2 - small.get_width() // 2, HEIGHT // 2 + 10))


# ======================================================================
# Programme principal
# ======================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Shooting Game - Auto Aim (OOP)")
    clock = pygame.time.Clock()

    board = GameBoard()
    renderer = GameRenderer()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if board.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        board.fire()
                elif event.key == pygame.K_r:
                    board.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if board.state == "PLAYING":
            board.player.handle_input(pygame.key.get_pressed())
        board.update()

        renderer.draw(screen, board)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


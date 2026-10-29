import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from game_tp2 import Bullet, GameBoard, GameRenderer, Monster, Player


def test_initial_values_match_tp1():
    b = GameBoard()
    assert (b.player.x, b.player.y, b.player.health) == (150, 275, 100)
    assert (b.monster.x, b.monster.y, b.monster.health, b.monster.speed) == (700, 275, 100, 2.0)
    assert b.score == 0 and b.state == "PLAYING"


def test_monster_chases_player():
    b = GameBoard()
    d0 = abs(b.monster.x - b.player.x)
    b.update()
    assert abs(b.monster.x - b.player.x) < d0


def test_fire_aims_at_monster_center():
    b = GameBoard()
    b.fire()
    bullet = b.bullets[0]
    assert bullet.vx > 0                       # le monstre est a droite
    assert (bullet.vx ** 2 + bullet.vy ** 2) ** 0.5 == pytest.approx(10)


def test_four_hits_kill_monster_and_it_gets_faster():
    b = GameBoard()
    for _ in range(4):                         # 4 x 25 = 100
        b.monster.x, b.monster.y = 400, 275
        b.bullets.append(Bullet(b.monster.x + 10, b.monster.y + 10, 0, 0))
        b.update()
    assert b.score == 1
    assert b.monster.health == 100
    assert b.monster.x == pytest.approx(850, abs=3)   # reapparait hors ecran (WIDTH + 50)
    assert b.monster.speed == pytest.approx(2.2)


def test_win_after_five_kills():
    b = GameBoard()
    b.score = 4
    b.monster.x, b.monster.y = 400, 275
    b.monster.health = 25
    b.bullets.append(Bullet(410, 285, 0, 0))
    b.update()
    assert b.state == "WIN"


def test_contact_damage_and_game_over():
    b = GameBoard()
    b.monster.x, b.monster.y = b.player.x, b.player.y
    b.update()
    assert b.player.health == 99
    b.player.health = 1
    b.update()
    assert b.state == "GAME_OVER"


def test_bullet_removed_off_screen():
    b = GameBoard()
    b.bullets.append(Bullet(799, 10, 10, 0))
    b.update()
    assert b.bullets == []


def test_reset():
    b = GameBoard()
    b.score, b.state = 3, "GAME_OVER"
    b.reset()
    assert b.score == 0 and b.state == "PLAYING"


def test_renderer_draws_every_state_without_error():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    r = GameRenderer()
    b = GameBoard()
    for state in ("PLAYING", "GAME_OVER", "WIN"):
        b.state = state
        r.draw(screen, b)
    pygame.quit()


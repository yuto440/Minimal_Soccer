import pygame
import sys
import constants as c
from ball import Ball
from player import Player
from team import Team

class GameController:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Minimal Soccer")

        self.clock = pygame.time.Clock()

        self.ball = Ball(pygame.math.Vector2(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2))#ボールの生成

        self.teams = [Team(c.TeamID.TEAM_A, c.RED), Team(c.TeamID.TEAM_B, c.BLUE)]
        
        self.players = [Player(pygame.math.Vector2(c.SCREEN_WIDTH / 4, c.SCREEN_HEIGHT / 2)),
                          Player(pygame.math.Vector2(c.SCREEN_WIDTH / 4, 3 * c.SCREEN_HEIGHT / 4)),
                          Player(pygame.math.Vector2(3 * c.SCREEN_WIDTH / 4, c.SCREEN_HEIGHT / 4)),
                          Player(pygame.math.Vector2(3 * c.SCREEN_WIDTH / 4, 3 * c.SCREEN_HEIGHT / 4))]
        self.num_players = len(self.players)

        self.teams[0].add_player(self.players[0])
        self.teams[0].add_player(self.players[1])
        self.teams[1].add_player(self.players[2])
        self.teams[1].add_player(self.players[3])

        self.field_rect = pygame.Rect(0, 0, c.FIELD_WIDTH, c.FIELD_HEIGHT)
        self.field_rect.center = self.screen.get_rect().center

        self.post_poses = [pygame.math.Vector2(self.field_rect.left, self.field_rect.centery - c.GOAL_WIDTH / 2),
                    pygame.math.Vector2(self.field_rect.left, self.field_rect.centery + c.GOAL_WIDTH / 2),
                    pygame.math.Vector2(self.field_rect.right, self.field_rect.centery - c.GOAL_WIDTH / 2),
                    pygame.math.Vector2(self.field_rect.right, self.field_rect.centery + c.GOAL_WIDTH / 2)]

    def reset(self):
        for player in self.players:
            player.reset()
        self.ball.pos = pygame.math.Vector2(self.field_rect.center)
        self.ball.velocity = pygame.math.Vector2(0, 0)

    def resolve_collisions(self): #衝突をまとめて解決
        self._check_wall_and_ball()
        self._check_posts_and_ball()
        self._check_player_and_ball()
        self._check_player_and_player()

    def _check_wall_and_ball(self):
        #左右の壁との衝突。ゴールはすり抜ける
        if self.ball.pos.x - c.BALL_RADIUS < self.field_rect.left:
            if self.ball.pos.y < (c.SCREEN_HEIGHT - c.GOAL_WIDTH) / 2 or self.ball.pos.y > (c.SCREEN_HEIGHT + c.GOAL_WIDTH) / 2:
                self.ball.pos.x = self.field_rect.left + c.BALL_RADIUS
                self.ball.velocity.x = -self.ball.velocity.x
        elif self.ball.pos.x + c.BALL_RADIUS > self.field_rect.right:
            if self.ball.pos.y < (c.SCREEN_HEIGHT - c.GOAL_WIDTH) / 2 or self.ball.pos.y > (c.SCREEN_HEIGHT + c.GOAL_WIDTH) / 2:
                self.ball.pos.x = self.field_rect.right - c.BALL_RADIUS
                self.ball.velocity.x = -self.ball.velocity.x
        #上下の壁との衝突
        if self.ball.pos.y - c.BALL_RADIUS < self.field_rect.top:
            self.ball.pos.y = self.field_rect.top + c.BALL_RADIUS
            self.ball.velocity.y = -self.ball.velocity.y
        elif self.ball.pos.y + c.BALL_RADIUS > self.field_rect.bottom:
            self.ball.pos.y = self.field_rect.bottom - c.BALL_RADIUS
            self.ball.velocity.y = -self.ball.velocity.y

    def _check_posts_and_ball(self):
        for post_pos in self.post_poses:
            post_to_ball = self.ball.pos - post_pos
            distance = post_to_ball.length()

            if distance < c.BALL_RADIUS:
                print("post")

                if distance > 0:
                    n_post_to_ball = post_to_ball.normalize()
                else:
                    n_post_to_ball = pygame.math.Vector2(1, 0)

                overlap = c.BALL_RADIUS - distance
                self.ball.pos += n_post_to_ball * overlap

                v_dot_n = self.ball.velocity.dot(n_post_to_ball)
                if v_dot_n < 0:
                    self.ball.velocity -= 2 * v_dot_n * n_post_to_ball

    def _check_player_and_ball(self):
        for player in self.players:
            player_to_ball = self.ball.pos - player.pos
            distance = player_to_ball.length()

            min_distance = c.PLAYER_RADIUS + c.BALL_RADIUS

            if distance < min_distance:#衝突判定
                if distance > 0:#ゼロベクトルでなければ正規化
                    n_player_to_ball = player_to_ball.normalize()
                else:
                    n_player_to_ball = pygame.math.Vector2(1, 0)

                #重なっている分を移動
                overlap = min_distance - distance
                self.ball.pos += n_player_to_ball * overlap

                relative_velocity = self.ball.velocity - player.velocity

                #相対速度と正規化した相対位置の内積
                v_dot_n = relative_velocity.dot(n_player_to_ball)

                #遠ざかる方向へ、つまりv_dot_nがプラスになる方向へ速度を変更
                if v_dot_n < 0:
                    self.ball.velocity -= (1.0 + c.ELASTICITY) * n_player_to_ball * v_dot_n
                
                player.trigger_knockback(n_player_to_ball)
    def _check_player_and_player(self):
        for i in range(0, self.num_players - 1):
            for j in range(i + 1, self.num_players):#プレイヤー同士のすべての組み合わせを一度ずつ処理
                player_0 = self.players[i]
                player_1 = self.players[j]

                p0_to_p1 = player_1.pos - player_0.pos
                distance = p0_to_p1.length()

                min_distance = c.PLAYER_RADIUS * 2

                if distance < min_distance:
                    if distance > 0:
                        n_p0_to_p1 = p0_to_p1.normalize()
                    else:
                        n_p0_to_p1 = pygame.math.Vector2(1, 0)

                    overlap = min_distance - distance

                    player_0.pos -= n_p0_to_p1 * overlap / 2
                    player_1.pos += n_p0_to_p1 * overlap / 2

    def goal_check(self):
        if self.ball.pos.x + c.BALL_RADIUS < self.field_rect.left:
            self.teams[0].score +=1
            self.reset()
        elif self.ball.pos.x - c.BALL_RADIUS> self.field_rect.right:
            self.teams[1].score +=1
            self.reset()
                

    def display(self):
        self.screen.fill(c.GRASS_COLOR)
        for player in self.players:
            player.draw(self.screen)
        self.ball.draw(self.screen)

        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.topright, self.field_rect.topleft, 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.bottomright, self.field_rect.bottomleft, 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.topleft, self.post_poses[0], 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.bottomleft, self.post_poses[1], 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.topright, self.post_poses[2], 3)
        # pygame.draw.line(self.screen, c.WHITE, self.field_rect.bottomright, self.post_poses[3], 3)

        pygame.draw.rect(self.screen, c.WHITE, self.field_rect, 3)
        
        for post_pos in self.post_poses:
            pygame.draw.circle(self.screen, c.WHITE, post_pos, 10)
        
        pygame.display.flip()

    def play_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.resolve_collisions()
            self.goal_check()
            dt = self.clock.tick(c.FPS) / 1000.0
            self.ball.update(dt)
            
            for player in self.players:
                player.think(self.ball.pos)
                player.update(dt)

            self.display()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gm = GameController()
    gm.play_game()
from __future__ import print_function

import pygame
from ldpygame.screen import Screen
from ldpygame.game import Game
from ldpygame.event_responder import KeyUpResponder, TimerResponder, QuitResponder
from ldpygame.sprite import BounceSprite, AnimatedSprite

def exit_game(event):
    Game.active_game.exit()

# Make the game
g = Game()

t1 = g.timers.add(10000)
t2 = g.timers.add(20000)

t1.start()
t2.start()

# Add some global input handlers
g.event_manager.add_event_responder(KeyUpResponder((pygame.K_ESCAPE), None, 1, exit_game))
g.event_manager.add_event_responder(QuitResponder(exit_game))
g.event_manager.add_event_responder(TimerResponder(lambda event: print(event, "10 seconds"), t1))
g.event_manager.add_event_responder(TimerResponder(lambda event: print(event, "20 seconds"), t2))

# Main screen setup
s = Screen('main', (360,240))

# Screen-based input handlers; only called when screen is active
s.event_manager.add_event_responder(KeyUpResponder((pygame.K_1), None, -1, lambda event: Game.active_game.activate_screen('alt')))

# Make a bouncing box
sprite = BounceSprite(pygame.Rect((10,10), (48,48)),
                      pygame.Rect((0,0), (360,240)),
                      s.sprites, # This adds the sprite to the screen's sprite list
                      g.images.get('tree-live.png'))
sprite.set_velocity(0.1,2)

# Alt screen setup
white_background = pygame.Surface((360,240))
white_background.fill(pygame.Color(255,255,255))
s2 = Screen('alt', (360,240), background=white_background)

# Screen-based input handlers; only called when screen is active
s2.event_manager.add_event_responder(KeyUpResponder((pygame.K_2), None, -1, lambda event: Game.active_game.activate_screen('main')))

# Make an animated thing
sprite = AnimatedSprite(pygame.Rect((60,100), (40,40)),
                        pygame.Rect((0,0), g.size),
                        s2.sprites,
                        g.images.get('ball.png'),
                        6, 100) #num frames, framedelay_ms
sprite.set_velocity(0.3,0.08)

# Make this screen our active screen
g.add_screen(s2)
g.activate_screen(s)
g.sounds.load_and_play_song('bu-the-paths-birds.ogg', volume=0.4)

# And off we go
g.run()

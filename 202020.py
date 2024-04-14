import rumps
import pygame
import sys
import os
import time

tick_period = 60 # seconds
working_time = 20 # minutes
rest_time = 20 # seconds
bkg_color = (44, 44, 43)
text_colr = (255, 255, 255)
full_screen = False

def show_rest_screen():
    pygame.init()
    if full_screen:
      screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      screen = pygame.display.set_mode((640, 480))
    screen.fill(bkg_color)

    # Add "skip" text to the screen
    font = pygame.font.Font(None, 300)
    text = font.render('Skip!', True, text_colr)  # White text
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Update the display with the text
    pygame.display.update()

    while True:
        event = pygame.event.wait(int(rest_time*1e3))
        if event.type == pygame.NOEVENT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if text_rect.collidepoint(event.pos):
                    break

    pygame.quit()

class TimerApp(rumps.App):
    def __init__(self):
        super(TimerApp, self).__init__("20-20-20 Timer")
        self.menu = ["Start/Pause Timer"]
        self.timer = rumps.Timer(self.on_tick, tick_period)  # Tick every minute
        self.timer.start()
        self.counter = working_time  # 20 minutes in seconds
        self.is_running = True

    @rumps.clicked("Start/Pause Timer")
    def onoff(self, sender):
        if self.is_running:
            self.timer.stop()
            sender.title = "Resume Timer"
        else:
            self.counter = working_time
            self.timer.start()
            sender.title = "Pause Timer"
        self.is_running = not self.is_running

    def on_tick(self, _):
        self.counter -= 1
        self.title = f"{self.counter+1:02d} min"
        if self.counter < 0:
            show_rest_screen()
            self.counter = working_time  # reset timer

if __name__ == "__main__":
    TimerApp().run()

import pygame
import win32clipboard

Black = (0, 0, 0)
White = (255, 255, 255)
NeonBlue = (62, 204, 252)
DarkBlue = (0, 48, 143)
EmeraldGreen = (10, 221, 8)


def button(screen, text, x, y, w, h, click, inactive_colour=DarkBlue, active_colour=NeonBlue, text_colour=White):
    mouse = pygame.mouse.get_pos()
    return_value = False
    if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
        pygame.draw.rect(screen, active_colour, (x, y, w, h))
        if click and pygame.time.get_ticks() > 100:
            return_value = True
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, w, h))

    buttonFont = pygame.font.SysFont("comicsans", 30)
    buttonText = buttonFont.render(text, True, White)
    buttonTextRect = buttonText.get_rect()
    buttonTextRect.center = (x+w/2, y+h/2)
    screen.blit(buttonText, buttonTextRect)
    return return_value


class InputBox:  # simple solution for input box adapted from https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame

    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = DarkBlue
        self.text = text
        boxFont = pygame.font.SysFont("comicsans", 20)
        self.txt_surface = boxFont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        returnVal = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = NeonBlue if self.active else DarkBlue
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # print(self.text)
                    returnVal = self.text
                    self.text = ''
                elif pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_v]:  # copy/ paste
                    win32clipboard.OpenClipboard()
                    copyData = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    self.text += copyData
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                boxFont = pygame.font.SysFont("comicsans", 30)
                self.txt_surface = boxFont.render(self.text, True, self.color)
        return returnVal

    def update(self):
        # Resize the box if the text is too long.
        width = max(250, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.fill(Black, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

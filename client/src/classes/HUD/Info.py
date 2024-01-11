from .Font import Font


class Info:

    text_to_show = ""

    def __init__(self, screen_size):
        self.screen_size = screen_size

    def blit_text(self, window):
        if not self.text_to_show:
            return
        text = Font.get_font(self.screen_size[0] // 10).render(self.text_to_show, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_size[0] / 2, self.screen_size[1] * 1 / 4))
        window.blit(text, text_rect)

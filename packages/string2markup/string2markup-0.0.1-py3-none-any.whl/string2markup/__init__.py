class S2M:
    def __init__(self, text):
        self.text = str(text)

    @property
    def b(self):
        self.text = "[b]" + self.text + "[/b]"
        return self

    @property
    def u(self):
        self.text = "[u]" + self.text + "[/u]"
        return self

    @property
    def i(self):
        self.text = "[i]" + self.text + "[/i]"
        return self

    @property
    def s(self):
        self.text = "[s]" + self.text + "[/s]"
        return self

    @property
    def sub(self):
        self.text = "[sub]" + self.text + "[/sub]"
        return self

    @property
    def sup(self):
        self.text = "[sup]" + self.text + "[/sup]"
        return self

    def font(self, font):
        self.text = f"[font={font}]" + self.text + "[/font]"
        return self

    def font_context(self, font_context):
        self.text = f"[font_context={font_context}]" + self.text + "[/font_context]"
        return self

    def font_family(self, font_family):
        self.text = f"[font_family={font_family}]" + self.text + "[/font_family]"
        return self

    def font_features(self, font_features):
        self.text = f"[font_features={font_features}]" + self.text + "[/font_features]"
        return self

    def ref(self, ref):
        self.text = f"[ref={ref}]" + self.text + "[/ref]"
        return self

    def anchor(self, anchor):
        self.text = f"[anchor={anchor}]" + self.text + "[/anchor]"
        return self

    def text_language(self, text_language):
        self.text = f"[text_language={text_language}]" + self.text + "[/text_language]"
        return self

    def size(self, size):
        self.text = f"[size={size}]" + self.text + "[/size]"
        return self

    def color(self, color):
        if isinstance(color, tuple):
            color = list(color)
        if isinstance(color, list):
            color = color[:3]
            if (
                color[0] >= 0
                and color[0] <= 1
                and color[1] >= 0
                and color[1] <= 1
                and color[2] >= 0
                and color[2] <= 1
            ):
                color = [x * 255 for x in color]
            color = [int(x) for x in color]
            color = "#" + "".join(f"{i:02X}" for i in color).lower()
        self.text = f"[color={color}]" + self.text + "[/color]"
        return self

    def __str__(self):
        return self.text
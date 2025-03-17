from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class Title(MDLabel):
    pass


class ConflictOfInterest(MDBoxLayout):
    label = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.title = Title(text=self.label)
        self.add_widget(self.title)
        self.instances = MDBoxLayout(
            orientation='horizontal',
            adaptive_size=True,
            spacing="20dp"
        )
        self.add_widget(self.instances)

    def on_label(self, instance, value):
        self.title.text = value

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, Dataset):
            self.instances.add_widget(widget)
            return
        widget.fbind('pos_hint', self._trigger_layout)
        return super(BoxLayout, self).add_widget(widget, *args, **kwargs)


class Row(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Subject(MDCard):
    text = StringProperty()
    halign = StringProperty("center")
    is_selected = BooleanProperty(False)
    color = ColorProperty([0, 0, 0, 1])
    _previous_color = ColorProperty()
    role = StringProperty("subject")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_selected = False


    def on_is_selected(self, instance, value):
        if value:
            self._previous_color = self.color
            self.color = (1, 0, 0, 1)
        else:
            self.color = self._previous_color


class Dataset(Subject):
    role = StringProperty("Dataset")
    conflict_of_interest = StringProperty()

class BackgroundWidget(MDFloatLayout):
    pass

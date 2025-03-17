from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.tools.hotreload.app import original_argv
from kivymd.uix.boxlayout import MDBoxLayout
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
            adaptive_width=True,
            spacing="20dp"
        )
        self.add_widget(self.instances)

    def on_label(self, instance, value):
        self.title.text = value

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, Entry):
            self.instances.add_widget(widget)
            return
        widget.fbind('pos_hint', self._trigger_layout)
        return super(BoxLayout, self).add_widget(widget, *args, **kwargs)


class Row(MDBoxLayout):
    pass


class EntryGroup(MDBoxLayout):
    belongs_to = ObjectProperty()

    def add_widget(self, widget, *args, is_base=False, **kwargs):
        widget.fbind('pos_hint', self._trigger_layout)
        return super(BoxLayout, self).add_widget(widget, *args, **kwargs)


class Entry(MDLabel):
    pass

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

Window.clearcolor = (0.95, 0.95, 0.98, 1)
Window.size = (450, 750)

class ModernButton(Button):
    def __init__(self, bg_color=(0.2, 0.5, 0.9, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class StudentRow(BoxLayout):
    def __init__(self, index, name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(55)
        self.padding = [dp(5), dp(5), dp(5), dp(5)]
        self.spacing = dp(8)
        
        num_lbl = Label(text=str(index), size_hint_x=None, width=dp(30), bold=True, color=(0.3, 0.3, 0.3, 1))
        name_lbl = Label(text=name, halign='left', valign='middle', color=(0.1, 0.1, 0.1, 1))
        name_lbl.bind(size=name_lbl.setter('text_size'))
        
        self.grade_input = TextInput(
            text="", multiline=False, size_hint_x=None, width=dp(60),
            halign='center', font_size='18sp', input_filter='int',
            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1),
            padding_y=[dp(10), dp(10)]
        )
        
        self.attend_btn = ModernButton(
            text="Был", size_hint_x=None, width=dp(70), 
            bg_color=(0.2, 0.7, 0.3, 1), bold=True, font_size='14sp'
        )
        self.attend_btn.bind(on_press=self.toggle_attendance)
        
        self.add_widget(num_lbl)
        self.add_widget(name_lbl)
        self.add_widget(self.grade_input)
        self.add_widget(self.attend_btn)

    def toggle_attendance(self, instance):
        if self.attend_btn.text == "Был":
            self.attend_btn.text = "Н/Б"
            self.attend_btn.bg_color = (0.85, 0.2, 0.2, 1)
        else:
            self.attend_btn.text = "Был"
            self.attend_btn.bg_color = (0.2, 0.7, 0.3, 1)
        self.attend_btn.update_rect()

class JournalApp(App):
    def build(self):
        self.title = "Журнал 5 'А'"
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80), spacing=dp(5))
        title = Label(text="📚 5 'А' Класс", font_size='24sp', bold=True, color=(0.1, 0.2, 0.4, 1))
        
        subject_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        subject_layout.add_widget(Label(text="Предмет:", size_hint_x=None, width=dp(80), bold=True))
        self.subject_input = TextInput(
            text="Математика", multiline=False, background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1), padding_y=[dp(10), dp(10)]
        )
        subject_layout.add_widget(self.subject_input)
        header.add_widget(title)
        header.add_widget(subject_layout)
        main_layout.add_widget(header)

        table_header = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(8), padding=[dp(5), 0, dp(5), 0])
        table_header.add_widget(Label(text="№", size_hint_x=None, width=dp(30), bold=True, color=(0.4, 0.4, 0.4, 1)))
        table_header.add_widget(Label(text="Фамилия Имя", bold=True, color=(0.4, 0.4, 0.4, 1)))
        table_header.add_widget(Label(text="Оценка", size_hint_x=None, width=dp(60), bold=True, color=(0.4, 0.4, 0.4, 1), halign='center'))
        table_header.add_widget(Label(text="Посещ.", size_hint_x=None, width=dp(70), bold=True, color=(0.4, 0.4, 0.4, 1), halign='center'))
        main_layout.add_widget(table_header)

        self.scroll = ScrollView()
        self.students_grid = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.students_grid.bind(minimum_height=self.students_grid.setter('height'))
        
        self.students_list = [
            "Борисов Андрей", "Виноградов Артём", "Гуков Димитрий", 
            "Григорьев Александр", "Гроховский Давид", "Прокофьев Денис",
            "Смороеский Евгений", "Макачёва Ульяна", "Кожеметёнов Ина",
            "Рахматулин Дамиил", "Остапук Маргарита", "Радьева Эмма"
        ]
        
        for i, name in enumerate(self.students_list, 1):
            self.add_student_row(i, name)

        self.scroll.add_widget(self.students_grid)
        main_layout.add_widget(self.scroll)

        add_layout = BoxLayout(size_hint_y=None, height=dp(100), orientation='vertical', spacing=dp(10))
        self.new_student_input = TextInput(
            hint_text="Введите Фамилию и Имя (например: Иванов Иван)", 
            multiline=False, background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1), padding_y=[dp(12), dp(12)]
        )
        add_btn = ModernButton(
            text="➕ Добавить ученика", bg_color=(0.2, 0.6, 0.2, 1), 
            size_hint_y=None, height=dp(45), bold=True
        )
        add_btn.bind(on_press=self.add_new_student)
        add_layout.add_widget(self.new_student_input)
        add_layout.add_widget(add_btn)
        main_layout.add_widget(add_layout)
        return main_layout

    def add_student_row(self, index, name):
        row = StudentRow(index, name)
        self.students_grid.add_widget(row)

    def add_new_student(self, instance):
        name = self.new_student_input.text.strip()
        if name:
            self.students_list.append(name)
            self.add_student_row(len(self.students_list), name)
            self.new_student_input.text = ""
            self.scroll.scroll_y = 0

if __name__ == '__main__':
    JournalApp().run()
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import requests
from bs4 import BeautifulSoup
import re

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text="Stock Number:", font_size='20sp', size_hint_y=None, height=50)
        self.input_prompt = Label(text="Plz use English", font_size='16sp', color=(1, 0, 0, 1), size_hint_y=None, height=40)
        self.text_input = TextInput(multiline=False, font_size='18sp', size_hint_y=None, height=50)
        self.button = Button(text="Search", font_size='20sp', size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.8, 1))
        
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.result_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))#type:ignore
        self.scroll_view.add_widget(self.result_layout)

        self.button.bind(on_press=self.stock)#type:ignore
        self.text_input.bind(on_text_validate=self.stock)  # Bind Enter key to stock method#type:ignore
        self.text_input.bind(focus=self.on_focus)#type:ignore

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.input_prompt)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.scroll_view)

        return self.layout

    def on_focus(self, instance, value):
        if value:
            # When the TextInput gains focus, show the input prompt
            self.input_prompt.text = "Plz use English"
        else:
            # When the TextInput loses focus, hide the input prompt
            self.input_prompt.text = ""

    def stock(self, instance):
        stock_nums = self.text_input.text.split(',')
        self.result_layout.clear_widgets()

        for stock_num in stock_nums:
            stock_num = stock_num.strip()
            if not re.match("^[A-Za-z0-9]+$", stock_num):
                stock_find = f"Error :'{stock_num}' not found。"
                self.result_layout.add_widget(Label(text=stock_find, font_size='18sp', size_hint_y=None, height=50))
                continue

            url = f"https://tw.stock.yahoo.com/quote/{stock_num}"
            web = requests.get(url)
            soup = BeautifulSoup(web.text, "html.parser")
            title = soup.find("h1")  # Changed from h2 to h1, update based on the actual Yahoo page structure

            try:
                a = soup.select_one(".Fz\(32px\)").get_text()#type:ignore
                b = soup.select(".Fz\(20px\)")[1].get_text()#type:ignore
                c = soup.select_one(".Fz\(16px\)").get_text()#type:ignore
                trend = soup.select_one("#main-0-QuoteHeader-Proxy .C\\(\\$c-trend-up\\), #main-0-QuoteHeader-Proxy .C\\(\\$c-trend-down\\)")
                s = "+" if trend and "C($c-trend-up)" in trend['class'] else "-"
                stock_find = f"Stock {stock_num}: {a} ({s}{b}) : Today Trade Number: {c}"
            except Exception as e:
                stock_find = f"Error:can't find stock '{stock_num}'"

            self.result_layout.add_widget(Label(text=stock_find, font_size='18sp', size_hint_y=None, height=50))

if __name__ == "__main__":
    MyApp().run()

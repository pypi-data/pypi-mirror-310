from shiny import App, ui, reactive, render
from shinyswatch import theme

from dkdc_chat.ui.gui.chat import chat_page, chat_server

gui = ui.page_fluid(
    ui.output_ui("main"),
    theme=theme.pulse,
)


def gui_server(input, output, session):
    # setup reactive values
    _val = reactive.Value(None)

    # WARNING: hack for testing only (so you don't have to login/use a test user)
    # current_username.set("test")

    # callbacks
    def _whatever(u):
        _val.set(u)

    # servers
    chat_server("chat")

    # global effects
    @render.ui
    def main():
        elements = [
            ui.nav_panel("home", ui.markdown("home")),
            ui.nav_panel("chat", chat_page("chat")),
        ]
        elements += [
            ui.nav_spacer(),
            ui.nav_control(
                ui.input_dark_mode(),
            ),
        ]

        return ui.navset_bar(
            *elements,
            title=ui.a("dkdc-io", href="https://dkdc.io", class_="navbar-brand"),
            id="navbar",
            selected="chat",
        )


app = App(gui, gui_server)

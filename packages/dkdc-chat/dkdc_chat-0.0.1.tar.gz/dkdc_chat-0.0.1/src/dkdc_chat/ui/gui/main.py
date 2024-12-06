from shiny import App, ui, reactive, render
from shinyswatch import theme

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

    # global effects
    @render.ui
    def main():
        return ui.markdown("main")


app = App(gui, gui_server)

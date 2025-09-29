from slack_bolt import App
from .ask_command import ask_callback
from .summary_command import summary_callback
from .index_command import do_index_callback
from .progress_command import debbie_progress_callback


def register(app: App):
    app.command("/ask-debbie")(ask_callback)
    app.command("/debbie-summary")(summary_callback)
    app.command("/update-debbie")(do_index_callback)
    app.command("/debbie-progress")(debbie_progress_callback)

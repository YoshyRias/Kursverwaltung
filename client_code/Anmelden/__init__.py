from ._anvil_designer import AnmeldenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Anmelden(AnmeldenTemplate):
  def __init__(self, name:str, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.kid = anvil.server.call('query_database_kursid', name)[0][0]

    res = anvil.server.call('query_database_namen', self.kid)
    self.repeating_panel_1.items = [{'Name': i[0]} for i in res]

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Frontend')

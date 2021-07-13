from darts.base_games.BasePlayer import BasePlayer
from darts.base_gui.Button import Button
from darts.core_games.BaseParty import BaseParty
from darts.constants import PartyState
from darts.app_styles import app_styles


class PlayerButton(Button):
    def __init__(self, root, party: BaseParty, player: BasePlayer):
        self.party: BaseParty = party
        self.player: BasePlayer = player
        super().__init__(root, text=self.name, command=self.set_as_next_player)

        self.party.on('latest.set', self.update)

    def update(self, *_, **__):
        """Update the widget."""
        if self.player is self.party.get_next_player():
            app_styles.config(self, tag='selected')
        else:
            app_styles.config(self, tag='')

        self.update_idletasks()

    @property
    def name(self):
        """Return the formatted player name."""
        return '-'.join(sub.capitalize() for sub in self.player.name.split())

    def set_as_next_player(self):
        """Set player as the next to play in the party."""
        if self.party.state is PartyState.DURING:
            prev_player = self.party.get_player_before(self.player)
            self.party.set_latest_player(prev_player.name)
            self.party.do()

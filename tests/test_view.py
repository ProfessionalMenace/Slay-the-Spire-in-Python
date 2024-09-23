import effects
import items
import entities
import displayer
import player


def test_view_piles_on_all_cards(monkeypatch):
  all_cards = items.create_all_cards()
  entity = player.Player.create_player()
  entity.energy = 3
  all_conditions = [(lambda card: card.upgraded is True, "Upgraded"),
                    (lambda card: not card.upgraded and card.type not in ("Status", "Curse") or card.name == 'Burn', "Upgradeable"),
                    (lambda card: card.removable is False, "Removable"), (lambda card: card.type == 'Skill', "Skill"),
                    (lambda card: card.type == 'Attack', "Attack"), (lambda card: card.type == 'Power', "Power"),
                    (lambda card: card.energy_cost <= entity.energy, "Playable")]

  with monkeypatch.context() as m:
    # Patch sleeps so it's faster
    m.setattr(effects, 'sleep', lambda x: None)
    m.setattr(entities, 'sleep', lambda x: None)
    m.setattr(displayer, 'sleep', lambda x: None)

    for function, condition_name in all_conditions:
      print(f"===== Condition: {condition_name} ======")
      displayer.view_piles(pile=all_cards, end=False, validator=function)

    # Also test the default condition
    print(f"===== Condition: Default ======")
    displayer.view_piles(pile=all_cards, end=False)


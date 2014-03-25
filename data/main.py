"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare,tools
from .states import introsplash, managing, boarding, mountainguide
from .states import betting, deerracing, raceresults
from .states import elf_popup, building_popup, instructionsplash, bet_instructions
from .states import building_placement

def main():
    """Add states to control here."""
    
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {"INTROSPLASH": introsplash.IntroSplash(),
                         "INSTRUCTIONSPLASH": instructionsplash.InstructionSplash(),
                         "MANAGING": managing.Managing(),
                         "ELFPOPUP": elf_popup.ElfPopup(),
                         "BUILDINGPOPUP": building_popup.BuildingPopup(),
                         #"BUILDINGSELECTION": building_selection.BuildingSelection(), 
                         "BUILDINGPLACEMENT": building_placement.BuildingPlacement(),
                         "MOUNTAINGUIDE": mountainguide.MountainGuide(),
                         "BOARDING" : boarding.Boarding(),
                         "BETINSTRUCTIONS": bet_instructions.BettingSplash(),
                         "BETTING": betting.Betting(),
                         "DEERRACING": deerracing.DeerRacing(),
                         "RACINGRESULTS": raceresults.RaceResults()}
    run_it.setup_states(state_dict, "INTROSPLASH")
    run_it.main()

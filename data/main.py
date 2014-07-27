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
from .states import building_placement, golfing, building_type_selection, building_selection
from .states import elf_assignment, message_window, elf_selector, mine_construction, present_drop
from .states import deerpopup, deer_assignment, helpmenu


def main():
    """Add states to control here."""
    
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {"INTROSPLASH": introsplash.IntroSplash(),
                         "INSTRUCTIONSPLASH": instructionsplash.InstructionSplash(),
                         "MANAGING": managing.Managing(),
                         "ELFSELECTOR": elf_selector.ElfSelector(),
                         "ELFPOPUP": elf_popup.ElfPopup(),
                         "ELFASSIGNMENT": elf_assignment.ElfAssignment(),
                         "BUILDINGPOPUP": building_popup.BuildingPopup(),
                         "MINEBUILD": mine_construction.MineConstruction(),
                         "BUILDINGTYPESELECTION": building_type_selection.BuildingTypeSelection(), 
                         "BUILDINGSELECTION": building_selection.BuildingSelection(),
                         "BUILDINGPLACEMENT": building_placement.BuildingPlacement(),
                         "MESSAGEWINDOW": message_window.MessageWindow(),
                         "MOUNTAINGUIDE": mountainguide.MountainGuide(),
                         "BOARDING" : boarding.Boarding(),
                         "BETINSTRUCTIONS": bet_instructions.BettingSplash(),
                         "BETTING": betting.Betting(),
                         "DEERRACING": deerracing.DeerRacing(),
                         "RACINGRESULTS": raceresults.RaceResults(),
                         "GOLFING": golfing.Golfing(),
                         "PRESENTDROP": present_drop.PresentDrop(),
                         "DEERPOPUP": deerpopup.DeerPopup(),
                         "DEERASSIGNMENT": deer_assignment.DeerAssignment(),
                         "HELPMENU": helpmenu.HelpMenu()}
                         
    run_it.setup_states(state_dict, "INTROSPLASH")
    run_it.main()

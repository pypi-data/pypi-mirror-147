#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REPL Shell for PyCDSL"""

###############################################################################

import os
import cmd
import logging
from typing import List

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from .corpus import CDSLCorpus
from .utils import validate_scheme, validate_search_mode
from .constants import (
    INTERNAL_SCHEME,
    DEFAULT_SCHEME,
    SEARCH_MODES,
    DEFAULT_SEARCH_MODE
)
from . import __version__

###############################################################################


class BasicShell(cmd.Cmd):
    def emptyline(self):
        pass

    def do_shell(self, commad):
        """Execute shell commands"""
        os.system(commad)

    def do_exit(self, arg):
        """Exit the shell"""
        print("Bye")
        return True

    # do_EOF corresponds to Ctrl + D
    do_EOF = do_exit

###############################################################################


class CDSLShell(BasicShell):
    """REPL Interface to CDSL"""

    intro = "Cologne Sanskrit Digital Lexicon (CDSL)\n" \
            "---------------------------------------"
    desc = "Install or load dictionaries by typing `use [DICT_IDS..]` " \
           "e.g. `use MW`.\n" \
           "Type any keyword to search in the selected dictionaries. " \
           "(help or ? for list of options)"
    prompt = "(CDSL::None) "

    def __init__(
        self,
        data_dir: str = None,
        dict_ids: List[str] = None,
        search_mode: str = None,
        input_scheme: str = None,
        output_scheme: str = None
    ):
        """REPL Interface to CDSL

        Create an instance of CDSLCorpus as per the providd parameters.
        CDSLCorpus.setup() is called after the command-loop starts.

        Parameters
        ----------
        data_dir : str or None, optional
            Load a CDSL installation instance at the location `data_dir`.
            Passed to CDSLCorpus instance as a keyword argument `data_dir`.
        dict_ids : list or None, optional
            List of dictionary IDs to setup.
            Passed to a CDSLCorpus.setup() as a keyword argument `dict_ids`.
        search_mode : str or None, optional
            Search mode to query by `key`, `value` or `both`.
            The default is None.
        input_scheme : str or None, optional
            Transliteration scheme for input.
            If None, `DEFAULT_SCHEME` is used.
            The default is None.
        output_scheme : str or None, optional
            Transliteration scheme for output.
            If None, `DEFAULT_SCHEME` is used.
            The default is None.
        """
        super(self.__class__, self).__init__()
        self.debug = False
        self.schemes = [
            sanscript.DEVANAGARI,
            sanscript.IAST,
            sanscript.ITRANS,
            sanscript.VELTHUIS,
            sanscript.HK,
            sanscript.SLP1,
            sanscript.WX,
        ]
        self.search_modes = SEARCH_MODES

        self.search_mode = (
            validate_search_mode(search_mode) or DEFAULT_SEARCH_MODE
        )
        self.input_scheme = validate_scheme(input_scheme) or DEFAULT_SCHEME
        self.output_scheme = validate_scheme(output_scheme) or DEFAULT_SCHEME

        self.cdsl = CDSLCorpus(
            data_dir=data_dir,
            search_mode=None,
            input_scheme=None,
            output_scheme=None
        )
        self.dict_ids = dict_ids
        self.active_dicts = None

        # Search parameters
        self.limit = 50
        self.offset = None

        # Logging
        self.logger = logging.getLogger()  # root logger
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)

    # ----------------------------------------------------------------------- #
    # Debug Mode

    def do_debug(self, arg: str):
        """Turn debug mode on/off"""
        arg = arg.lower()
        if arg in ["true", "on", "yes"]:
            self.debug = True
            self.logger.setLevel(logging.DEBUG)
        if arg in ["false", "off", "no"]:
            self.debug = False
            self.logger.setLevel(logging.INFO)
        print(f"Debug: {self.debug}")

    # ----------------------------------------------------------------------- #
    # Input/Output Transliteration Scheme

    def complete_input_scheme(self, text, line, begidx, endidx):
        return [sch for sch in self.schemes if sch.startswith(text)]

    def complete_output_scheme(self, text, line, begidx, endidx):
        return [sch for sch in self.schemes if sch.startswith(text)]

    def do_input_scheme(self, scheme: str):
        """Change the input transliteration scheme"""
        if not scheme:
            print(f"Input scheme: {self.input_scheme}")
        else:
            if scheme not in self.schemes:
                print(f"Invalid scheme. (valid schemes are {self.schemes})")
            else:
                self.input_scheme = scheme
                print(f"Input scheme set to '{self.input_scheme}'.")

    def do_output_scheme(self, scheme: str):
        """Change the output transliteration scheme"""
        if not scheme:
            print(f"Output scheme: {self.output_scheme}")
        else:
            if scheme not in self.schemes:
                print(f"Invalid scheme. (valid schemes are {self.schemes}")
            else:
                self.output_scheme = scheme
                print(f"Output scheme set to '{self.output_scheme}'.")

    # ----------------------------------------------------------------------- #
    # Search Mode

    def complete_search_mode(self, text, line, begidx, endidx):
        return [sch for sch in self.search_modes if sch.startswith(text)]

    def do_search_mode(self, mode: str):
        """Change the search mode"""
        if not mode:
            print(f"Search mode: {self.search_mode}")
        else:
            if mode not in self.search_modes:
                print(f"Invalid mode. (valid modes are {self.search_modes})")
            else:
                self.search_mode = mode
                print(f"Search mode set to '{self.search_mode}'.")

    # ----------------------------------------------------------------------- #
    # Dictionary Information

    def do_info(self, text: str = None):
        """Display information about active dictionaries"""
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            print(f"Total {len(self.active_dicts)} dictionaries are active.")
            for active_dict in self.active_dicts:
                print(active_dict)

    def do_stats(self, text: str = None):
        """Display statistics about active dictionaries"""
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            print(f"Total {len(self.active_dicts)} dictionaries are active.")
            for active_dict in self.active_dicts:
                print("---")
                print(active_dict)
                print(active_dict.stats(output_scheme=self.output_scheme))

    # ----------------------------------------------------------------------- #

    def do_dicts(self, text: str = None):
        """Display a list of dictionaries available locally"""
        for _, cdsl_dict in self.cdsl.dicts.items():
            print(cdsl_dict)

    def do_available(self, text: str = None):
        """Display a list of dictionaries available in CDSL"""
        for _, cdsl_dict in self.cdsl.available_dicts.items():
            print(cdsl_dict)

    # ----------------------------------------------------------------------- #

    def do_update(self, text: str = None):
        """Update loaded dictionaries"""
        self.cdsl.setup(list(self.cdsl.dicts), update=True)

    # ----------------------------------------------------------------------- #

    def complete_use(self, text, line, begidx, endidx):
        last_word = text.upper().rsplit(maxsplit=1)[-1] if text else ""
        return [
            dict_id
            for dict_id in self.cdsl.available_dicts
            if dict_id.startswith(last_word)
        ]

    def do_use(self, line: str):
        """
        Load the specified dictionaries from CDSL.
        If not available locally, they will be installed first.

        * `all` to load all
        * `none` to unload all
        """
        line = line.upper().strip()
        if not line:
            print("Please provide dictionary ID(s) to use.")
            return
        if line == "NONE":
            self.active_dicts = []
        elif line == "ALL":
            status = self.cdsl.setup()
            if status:
                self.active_dicts = self.cdsl.dicts.values()
            else:
                self.logger.error("Couldn't setup some dictionary.")
        else:
            dict_ids = line.split()
            self.active_dicts = []
            for dict_id in dict_ids:
                status = (
                    dict_id in self.cdsl.dicts
                ) or self.cdsl.setup([dict_id])
                if status:
                    self.active_dicts.append(self.cdsl.dicts[dict_id])
                else:
                    self.logger.error(
                        f"Couldn't setup dictionary '{dict_id}'."
                    )

        active_count = len(self.active_dicts)
        active_ids = [active_dict.id for active_dict in self.active_dicts]

        print(f"Using {active_count} dictionaries: {active_ids}")

        if active_count == 0:
            active_prompt = "None"
        elif active_count <= 3:
            active_prompt = ",".join(active_ids)
        else:
            active_prompt = f"{active_ids[0]}+{active_count - 1}"
        self.prompt = f"(CDSL::{active_prompt}) "

    # ----------------------------------------------------------------------- #

    def do_show(self, entry_id: str):
        """Show a specific entry by ID"""
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            for active_dict in self.active_dicts:
                try:
                    result = active_dict.entry(entry_id)
                    print(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )
                    self.logger.debug(f"Data: {result.data}")
                except Exception:
                    result = None

                if result is None:
                    self.logger.warning(
                        f"Entry {entry_id} not found in '{active_dict.id}'."
                    )

    # ----------------------------------------------------------------------- #

    def do_limit(self, text: str):
        """Limit the number of search results per dictionary"""
        if text:
            try:
                self.limit = int(text.strip())
                if self.limit < 1:
                    self.limit = None
                print(f"Limit set to '{self.limit}'.")
            except Exception:
                self.logger.error("Limit must be an integer.")
        else:
            print(f"Limit: {self.limit}")

    # ----------------------------------------------------------------------- #

    def do_version(self, text: str = None):
        """Show the current version of PyCDSL"""
        print(f"PyCDSL v{__version__}")

    # ----------------------------------------------------------------------- #

    def do_search(self, line: str):
        """
        Search in the active dictionaries

        Note
        ----
        * Searching in the active dictionaries is also the default action.
        * In general, we do not need to use this command explicitly unless we
          want to search the command keywords, such as, `available` `search`,
          `version`, `help` etc. in the active dictionaries.
        """
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            for active_dict in self.active_dicts:
                search_pattern = transliterate(
                    line, self.input_scheme, INTERNAL_SCHEME
                ) if active_dict.transliterate_keys else line
                results = active_dict.search(
                    search_pattern,
                    mode=self.search_mode,
                    limit=self.limit
                )
                if not results:
                    continue

                print(f"\nFound {len(results)} results in {active_dict.id}.\n")

                for result in results:
                    print(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )

    # ----------------------------------------------------------------------- #

    def default(self, line: str):
        self.do_search(line)

    # ----------------------------------------------------------------------- #

    def cmdloop(self, intro: str = None):
        print(self.intro)
        print(self.desc)
        self.cdsl.setup(dict_ids=self.dict_ids)

        print(f"Loaded {len(self.cdsl.dicts)} dictionaries.")

        if self.dict_ids is not None:
            self.do_use(" ".join(self.dict_ids))

        while True:
            try:
                super(self.__class__, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")


###############################################################################

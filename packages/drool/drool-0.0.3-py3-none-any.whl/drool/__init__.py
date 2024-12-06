#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024  darryl mcculley

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Any, Optional
from pydantic import BaseModel

from .operators import operators

# = = = 

class rule (BaseModel):
    feature:str
    operator:str
    value:Optional[Any]=None

    def eval(self, id:str, input:dict, qualifier:bool=False, alias:str=None):
        op = operators.get(self.operator)
        if op is None: raise Exception(f'operator "{self.operator}" not found.')
        try: 
            return "pass" if op(input[self.feature], self.value) else "fail"
        except KeyError: raise Exception(f'"{self.feature}" not found in input data.')

# = = = 

class ruleset (BaseModel):
    qualifier: Optional[dict[str, rule]]=None
    rules: dict[str, rule]

    def eval(self, ruleset:str, input:dict):
        rules = {alias: rule.eval(ruleset, input, alias=alias) for alias, rule in self.rules.items()}
        n_failed = len([v for v in rules.values() if v == "fail"])
        if self.qualifier:
            qualifiers = {alias: rule.eval(ruleset, input, qualifier=True, alias=alias) for alias, rule in self.qualifier.items()}
            n_qualifier_failed = len([v for v in qualifiers.values() if v == "fail"])
            return dict(qualified="pass" if n_qualifier_failed == 0 else "fail", qualifiers=qualifiers, rules=rules, n_failed=n_failed)
        return dict(qualified=None, qualifiers={}, rules=rules, n_failed=n_failed)
    
class group (BaseModel):
    qualifier: Optional[dict[str, rule]]=None
    rulesets: dict[str, ruleset]
    
    def eval(self, group:str, input:dict):
        rulesets = {ruleset_key: ruleset.eval(ruleset_key, input) for ruleset_key, ruleset in self.rulesets.items()}
        if self.qualifier:
            qualifiers = {alias: rule.eval(group, input, qualifier=True, alias=alias) for alias, rule in self.qualifier.items()}
            n_qualifier_failed = len([v for v in qualifiers.values() if v == "fail"])
            return dict(qualified="pass" if n_qualifier_failed == 0 else "fail", qualifiers=qualifiers, **rulesets)
        return dict(qualified=None, qualifiers={}, **rulesets)

# = = =

class config (BaseModel):
    groups:dict[str, group]

    def eval(self, input:dict):
        return {group_key: group.eval(group_key, input) for group_key, group in self.groups.items()}
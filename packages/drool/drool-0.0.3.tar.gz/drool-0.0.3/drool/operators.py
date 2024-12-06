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

operators = dict(
                greater_than =lambda context, value: context > value,
    greater_than_or_equal_to =lambda context, value: context >= value,
                   less_than =lambda context, value: context < value,
       less_than_or_equal_to =lambda context, value: context <= value,
                    equal_to =lambda context, value: context == value,
                not_equal_to =lambda context, value: context != value,
                    contains =lambda context, value: value in context,
                        isin =lambda context, value: context in value,
                    not_null =lambda context, _: context != None,
                        true =lambda context, _: context == True,
                       false =lambda context, _: context == False,
)
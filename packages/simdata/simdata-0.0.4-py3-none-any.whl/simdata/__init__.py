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

from pydantic import BaseModel, ConfigDict

from .sim import simd_func

class simd (BaseModel):
    model_config = ConfigDict(extra="allow")

    def __init__(self, **data):
        super().__init__(**data)
        simd_funcs = {f.__name__:f for f in simd_func.__subclasses__()}
        for field, value in self.__pydantic_extra__.items():
            if isinstance(value, dict) and "func" in value:
                func_type = value["func"]
                func_class = simd_funcs.get(func_type)
                if func_class: 
                    setattr(self, field, func_class(**value))

    def simulate(self, n:int=1):
        sim_data = [{ 
            field: getattr(self, field).simulate()
            for field in sorted(self.model_fields_set)
        } for _ in range(n)]
        if n == 1: return sim_data[0]
        else: return sim_data
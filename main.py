# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# Copyright (c) 2008-2020 pyglet contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# KeyFire Engine
# Copyright 2019 - 2020 Alessandro Salerno (Tzyvoski)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------


from locals import *
from os import system
import os
import tzylang as translate

system("cls") if os.name == "nt" else system("clear")


# Eval the contens of the options file
with open("options.kson", "r") as preferences:
    global options
    _options = preferences.read()
    options  = eval(compile(source=_options, filename="options", mode="eval", optimize=1))


# Read the code contained in the main file and run some checks
if options["main file"] is not None:
    with open(options["main file"], "r") as file:
        global source

        if options["language"] == "tzylang":
            source = translate.build(file.read())
            Log.successful("Parsed tzylang script")
        elif options["language"] == "python":
            source = file.read()
            Log.successful("Loaded python script")
        else:
            Log.critical("The specified language is not supported!")
else:
    Log.critical("No main file specified!")
    input()


# Compiles all the code
exec(compile(source=source, filename="", mode="exec", optimize=1))

try: 
    # Enable KeyFire Transparency if required
    if options["use transparency"]:
        engine.main_window.enable(KFE_TRANSPARENCY)

    # Enable KeyFire Basic Lighting if required
    if options["use basic lighting"]:
        engine.main_window.enable(KFE_LIGHTING)

    # Set OpenGL Clear Color
    engine.main_window.set_clear_color(options["clear color"])

    # Set the render distance
    engine.main_window.set_render_distance(options["render distance"])

    # Set Fog color
    engine.main_window.set_fog_color(options["fog color"])

    # Enable Fog if required
    if options["enable fog"]   == "default":
        engine.main_window.enable(KFE_FOG)
    elif options["enable fog"] == "nice":
        engine.main_window.enable(KFE_NICE_FOG)

    # Enable HUD if required
    if options["use dynamic hud"]:
        engine.main_window.enable(KFE_DYNAMIC_HUD)
    if options["use static hud"]:
        engine.main_window.enable(KFE_STATIC_HUD)
except:
    _errcam = OrthographicCamera()
    _errwin = Window3D(camera=_errcam)
    Log.critical("Something went wrong while setting up your game. This is usually caused by the absence of a default window and/or camera")


# Runs all the code3
engine.run()

# Random print() to make the output look cleaner
print()

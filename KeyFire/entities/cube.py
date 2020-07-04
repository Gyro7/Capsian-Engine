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


class Cube(Object):
    """
    A Cube object is 3D Cube.
    This object uses Batched rendering for high performance and KeyFire materials for texturing.

    """

    def __init__(self, size=[1, 1, 1], pos=[0, 0, 0], rot=[0, 0, 0], scene=None, lis=[], material=None):
        """
        Creates a cube in the world

        :param size: The size of the cube (Array [x, y, z])
        :param pos: The position of the cube in 3D space (Array [x, y, z])
        :param rot: Nothing
        :param scene: The scene in which the cube needs to be rendered (Scene(), KFE_3D_SCENE)
        :param lis: Can be used for greedy meshes (Not supported in this version)
        :param material: The material the cube is made out of (Texture3D()/SmartTexture3D, Material())
        """

        Object.__init__(self, size=size, pos=pos, rot=rot, batch=scene)

        self.next_pos = [[pos[0] + 1, pos[1], pos[2]],
                         [pos[0] - 1, pos[1], pos[2]],
                         [pos[0], pos[1], pos[2] + 1],
                         [pos[0], pos[1], pos[2] - 1],
                         [pos[0], pos[1] + 1, pos[2]],
                         [pos[0], pos[1] - 1, pos[2]]]

        self.pos_list = lis
        self.texture = material.texture

        self.add_block(self.pos[0], self.pos[1], self.pos[2])


    # Get coordinates of near by cubes
    def get_coords(self, face):
        """
        :param face: String
        :return: Array [x, y, z]
        """

        coords = {
            "left": self.next_pos[1],
            "right": self.next_pos[0],
            "back": self.next_pos[3],
            "front": self.next_pos[2],
            "top": self.next_pos[4],
            "bottom": self.next_pos[5]
        }

        return coords[face]


    # Check if there is any cube near by
    def new_check(self, face):
        """
        Calls Cube.get_coords()

        :param face: String
        :return: Boolean
        """

        if self.get_coords(face) in self.pos_list:
            return True
        else:
            return False


    # Add faces to batch
    def add_block(self, x, y, z):
        """
        Adds the cube to the specified scene

        :param x: X position in 3D Space (Float/int)
        :param y: Y position in 3D space (Float/int)
        :param z: Z position in 3D space (Float/int)
        :return: Nothing
        """

        X, Y, Z = x + self.size[0], y + self.size[1], z + self.size[2]

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        if not self.new_check("back"): self.batch.add(4, OpenGL.GL_QUADS, self.texture,
                                                         ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z)),
                                                         tex_coords)  # back

        if not self.new_check("front"): self.batch.add(4, OpenGL.GL_QUADS, self.texture,
                                                          ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
                                                          tex_coords)  # front

        if not self.new_check("left"): self.batch.add(4, OpenGL.GL_QUADS, self.texture,
                                                         ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
                                                         tex_coords)  # left

        if not self.new_check("right"): self.batch.add(4, OpenGL.GL_QUADS, self.texture,
                                                          ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z)),
                                                          tex_coords)  # right

        if not self.new_check("bottom"): self.batch.add(4, OpenGL.GL_QUADS, self.texture,
                                                           ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)),
                                                           tex_coords)  # bottom

        if not self.new_check("top"): self.batch.add(4, OpenGL.GL_QUADS, self.texture,
                                                        ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)),
                                                        tex_coords)  # top


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty,FloatProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from math import *

middle_point_cache = {}
def add_object(self, context):
    #scale_x = self.scale.x
    #scale_y = self.scale.y
    #scale_z = self.scale.z

    ico =Icosphere()
    ico.baseicosahedron(1)
    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(ico.verts,[],ico.faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh)
# -----------------------------------------------------------------------------
# Settings
class Icosphere():
    def __init__(self):
        self.name = 'Icosomething'
        self.scale=2
        self.subdiv=2
        self.verts=[]
        self.faces=[]


# -----------------------------------------------------------------------------
# Functions

    


    def vertex(self,x, y, z):
        """ Return vertex coordinates fixed to the unit sphere """

        length = sqrt(x**2 + y**2 + z**2)

        return [(i * self.scale) / length for i in (x,y,z)]


    def middle_point(self,point_1, point_2):
        """ Find a middle point and project to the unit sphere """

        # We check if we have already cut this edge first
        # to avoid duplicated verts
        smaller_index = min(point_1, point_2)
        greater_index = max(point_1, point_2)

        key = '{0}-{1}'.format(smaller_index, greater_index)

        if key in middle_point_cache:
            return middle_point_cache[key]

        # If it's not in cache, then we can cut it
        vert_1 = self.verts[point_1]
        vert_2 = self.verts[point_2]
        middle = [sum(i)/2 for i in zip(vert_1, vert_2)]

        self.verts.append(self.vertex(*middle))

        index = len(self.verts) - 1
        middle_point_cache[key] = index

        return index


# -----------------------------------------------------------------------------
# Make the base icosahedron

# Golden ratio
    def baseicosahedron(self,scale):
        PHI = (1 + sqrt(5)) / 2

        self.verts = [
                  self.vertex(-1,  PHI, 0),
                  self.vertex( 1,  PHI, 0),
                  self.vertex(-1, -PHI, 0),
                  self.vertex( 1, -PHI, 0),

                  self.vertex(0, -1, PHI),
                  self.vertex(0,  1, PHI),
                  self.vertex(0, -1, -PHI),
                  self.vertex(0,  1, -PHI),

                  self.vertex( PHI, 0, -1),
                  self.vertex( PHI, 0,  1),
                  self.vertex(-PHI, 0, -1),
                  self.vertex(-PHI, 0,  1),
                ]


        self.faces = [
                 # 5 faces around point 0
                 [0, 11, 5],
                 [0, 5, 1],
                 [0, 1, 7],
                 [0, 7, 10],
                 [0, 10, 11],

                 # Adjacent faces
                 [1, 5, 9],
                 [5, 11, 4],
                 [11, 10, 2],
                 [10, 7, 6],
                 [7, 1, 8],

                 # 5 faces around 3
                 [3, 9, 4],
                 [3, 4, 2],
                 [3, 2, 6],
                 [3, 6, 8],
                 [3, 8, 9],

                 # Adjacent faces
                 [4, 9, 5],
                 [2, 4, 11],
                 [6, 2, 10],
                 [8, 6, 7],
                 [9, 8, 1],
                ]
        

# -----------------------------------------------------------------------------
    # Subdivisions
    def Subdivisions(self,subdiv):
        for i in range(subdiv):
            faces_subdiv = []

            for tri in self.faces:
                v1 = self.middle_point(tri[0], tri[1])
                v2 = self.middle_point(tri[1], tri[2])
                v3 = self.middle_point(tri[2], tri[0])

                faces_subdiv.append([tri[0], v1, v3])
                faces_subdiv.append([tri[1], v2, v1])
                faces_subdiv.append([tri[2], v3, v2])
                faces_subdiv.append([v1, v2, v3])

            self.faces = faces_subdiv

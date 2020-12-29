import bpy
from math import *
import mathutils
    
    
class celestial_body():
    ibodycount = {}
    def __init__(self,mass,Vini,obj,celestialBodyName):
        celestial_body.ibodycount[celestialBodyName] =  obj
        self.G = 6.67e-11
        self.celestialBodyName = celestialBodyName
        self.fps = bpy.context.scene.render.fps
        self.timestep = 1
        self.cbn = {}
        self.distdicc = {}
        self.gravitydicc = {}
        self.vectordicc = {}
        self.veldicc ={}
        self.obj = bpy.data.objects[obj].location
        self.name = str(obj)
        self.mass = mass
        self.Vini = Vini

    def UpdateVariables(self,mass,Vini):
        self.mass = mass
        self.Vini = Vini

    def Distance(self,name):
        obj2loc = bpy.data.objects[str(name)].location       
        self.distdicc[name] = sqrt((self.obj[0]-obj2loc[0])**2+(self.obj[1]-obj2loc[1])**2+(self.obj[2]-obj2loc[2])**2)
            
        #debugg print(self.name, "distance to ", self.distdicc)
           
    def Gravity(self,name,mass):
        #for key in self.distdicc:
        
        gravity = self.G*mass/(self.distdicc[name])**2
        self.gravitydicc[name] = gravity
            
        #debugg print(self.name, " gravity to ", self.gravitydicc)
    
    def UVector(self,name):
        
        obj2loc = bpy.data.objects[str(name)].location
        self.vectordicc[name] = (self.obj - obj2loc)/(self.distdicc[name])
        
        #print(self.name, " uvector to ", self.vectordicc)
        
    def UpdateVelocity(self,name):
        
        if int(bpy.context.scene.frame_current) <= 3:
            print("dentro")
            self.veldicc[name] = self.Vini + (self.timestep/self.fps)*self.gravitydicc[name]*self.vectordicc[name]
        else:
            self.veldicc[name] = self.veldicc[name] + (self.timestep/self.fps)*self.gravitydicc[name]*self.vectordicc[name]
        #print(self.name, " velocity to ", self.veldicc)
    
    def UpdatePosition(self,name):
         
        bpy.data.objects[name].location = bpy.data.objects[name].location + (self.timestep/self.fps)*self.veldicc[name] + (self.timestep/(self.fps))**2*0.5**self.gravitydicc[name]*self.vectordicc[name]
        return self.Vini
    
    def SetVelocity(self,vel):
        
        self.Vini = vel        
    
    def UpdateDicc(self):
        #self.Gravity(i.name,mass)
        for i in bpy.data.objects:
            
            if self.name != i.name:
                self.Distance(i.name)
                self.Gravity(i.name,self.mass)
                self.UVector(i.name)
                self.UpdateVelocity(i.name)
                self.UpdatePosition(i.name)
        print("----------------------------------",self.celestialBodyName,"----------------------------------")        
        print(self.name, "distance to ", self.distdicc)
        print(self.name, " gravity to ", self.gravitydicc)
        print(self.name, " uvector to ", self.vectordicc)
        print(self.name, " velocity to ", self.veldicc)
#############################################################################################################################


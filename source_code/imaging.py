import random
import numpy as np 

from numpy.random import rand

pixel_id  = 0
pixel_lvl = 0

orb_offset = 0.0005 # 0.01%

class Pixel():
    def __init__(self,problem,orbit, parent = None, offset = 0):

        if orbit is None:

            if parent is None:
                self.parent_id = None
                self.position = problem.lower_bounds + ((rand(problem.dimension) + rand(problem.dimension)) * (problem.upper_bounds - problem.lower_bounds) / 2)
                # self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
            else:
                self.parent_id = parent.id
                self.position = parent.position + ( np.random.uniform(-1, 1, problem.dimension) * offset )
                # self.position = np.array([parent.position[0]+((-1) ** (bool(random.getrandbits(1))) * random.random() * offset), parent.position[1]+((-1)**(bool(random.getrandbits(1))) * random.random() * offset)])

        else:
            if parent is None:
                self.parent_id = None
                self.position = orbit + ( np.random.uniform(-1, 1, problem.dimension) * orb_offset )
                # self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
            else:
                self.parent_id = parent.id
                self.position = parent.position + ( np.random.uniform(-1, 1, problem.dimension) * offset )
                # self.position = np.array([parent.position[0]+((-1) ** (bool(random.getrandbits(1))) * random.random() * offset), parent.position[1]+((-1)**(bool(random.getrandbits(1))) * random.random() * offset)])

        #self.fitness = float('inf')
        if  not problem.final_target_hit :
            self.fitness = problem(self.position)
        else:
            self.fitness = 999999
        # self.fitness = self.position[0] ** 2 + self.position[1] ** 2 + 1
        global pixel_id,pixel_lvl
        self.id = pixel_id
        self.lvl = pixel_lvl
        pixel_id += 1
        # print(pixel_id)
        # print("-")

    def __str__(self):
        # print( self.position )
        print( self.id )
        # print("I am at ", self.position, ", value is ", self.fitness)
        # print( self.id,self.parent_id , self.lvl , '%.2f'% self.fitness)

class Image():
    def __init__(self,problem,orbit, n_pixels, target = None):
        self.problem = problem
        self.orbit = orbit

        global pixel_id,pixel_lvl
        pixel_id  = 0
        pixel_lvl = 0

        self.n_pixels = n_pixels
        self.pixels = []
        self.target = target
        if target is None:
            self.sort_pixels = self.sort_pixels_descending
        else:
            self.sort_pixels = self.sort_pixels_on_target

        self.pixels = [Pixel(self.problem,self.orbit) for _ in range(self.n_pixels)]
        self.sort_pixels()

    def print_pixels(self):
        print([x.id for x in self.pixels])
        # for pixel in self.pixels:
            # pixel.__str__()

    def print_pixel_range(self,pixels):
        for pixel in pixels:
            pixel.__str__()

    def sort_pixels_descending(self):
        # self.pixels.sort(key=lambda x: x.fitness, reverse=True)
        self.pixels.sort(key=lambda x: x.fitness)

    def sort_pixels_on_target(self):
        self.pixels.sort(key=lambda x: abs(x.fitness-self.target))

    def branch_pixels(self,n_pixels,n_sparks, offset = 0):
        global pixel_lvl
        pixel_lvl += 1
        for i in range(n_pixels):
            for j in range(n_sparks):
                self.pixels.append(Pixel(self.problem,self.orbit,self.pixels[i],offset))
        self.sort_pixels()

class Mapping_Instrument():
    def __init__(self,problem,orbit = None):
        self.problem = problem
        self.orbit = orbit
        pass

    def print_summary(self,search_space):
        # search_space.print_pixels()
        # print(search_space.pixels[0].fitness)
        # print(search_space.pixels[0].fitness)
        # search_space.print_pixel_range(search_space.pixels[0:3])
        pass

    def Starry_Night(self, n_pixels, r_pixels, target = None):
        # print("--- Starry_Night ---")
        search_space = Image(self.problem,self.orbit,n_pixels,target)
        # self.print_summary(search_space)
        return search_space.pixels[0:r_pixels]

    def Lanterns(self, n_pixels, n_sparks, r_pixels, offset = 0, target = None):
        # print("--- Lanterns ---")
        search_space = Image(self.problem,self.orbit,n_pixels,target)
        search_space.branch_pixels(n_pixels,n_sparks,offset)
        # self.print_summary(search_space)
        return search_space.pixels[0:r_pixels]

    def Fireworks(self, n_pixels, n__spark_pixels, n_sparks, r_pixels, offset = 0, target = None):
        # print("--- Fireworks ---")
        search_space = Image(self.problem,self.orbit,n_pixels,target)
        search_space.branch_pixels(n__spark_pixels,n_sparks,offset)
        # self.print_summary(search_space)
        return search_space.pixels[0:r_pixels]

    def Constellation (self, n_pixels, r_pixels, offset = 0, target = None):
        # print("--- Constellation ---")
        search_space = Image(self.problem,self.orbit,1,target)
        for i in range(n_pixels-1):
            search_space.branch_pixels(1,1,offset)

            try:
                search_space.pixels.pop(r_pixels)
            except:
                pass

        # self.print_summary(search_space)
        return search_space.pixels[0:r_pixels]
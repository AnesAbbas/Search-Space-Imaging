import random
import numpy as np 
from numpy.random import rand

import imaging as mp 
import math

W = 0.9
c1 = 1.49445
c2 = 1.49445
# W = 0.5
# c1 = 0.8
# c2 = 0.9 
    #   double w = 0.729; // inertia weight
    #   double c1 = 1.49445; // cognitive/local weight
    #   double c2 = 1.49445; // social/global weight

'''
target_error = float(input("Inform the target error: "))
n_particles = int(input("Inform the number of particles: "))
'''

target_error = 1e-6

# problem = None
# def set_problem(p):
#     global problem
#     problem = p

class Particle():
    def __init__(self,problem,px = None):
        self.initfit = 1
        if px is None:
            self.position = problem.lower_bounds + ((rand(problem.dimension) + rand(problem.dimension)) * (problem.upper_bounds - problem.lower_bounds) / 2)
            # self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        else:
            self.position = px.position 
            self.ft = px.fitness

        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = problem.initial_solution
        # self.velocity = np.array([0,0])

    def __str__(self):
        # print("I am at ", self.position, " meu pbest is ", self.pbest_position)
        # print('%.2f'% self.pbest_value)
        pass

    def move(self):
        self.position = self.position + self.velocity

class Space():

    def __init__(self, target, target_error, n_particles,problem):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = problem.lower_bounds + ((rand(problem.dimension) + rand(problem.dimension)) * (problem.upper_bounds - problem.lower_bounds) / 2)

        self.problem = problem

        self.initfit = 1
        # self.gbest_position = np.array([random.random()*50, random.random()*50])

        #self.gbest_particle = []

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()

    def fitness(self, particle):
        if  not self.problem.final_target_hit :
            particle.ft = self.problem(particle.position)
        else:
            particle.ft = 999999

        return particle.ft
        # return particle.position[0] ** 2 + particle.position[1] ** 2 + 1

    def set_pbest(self):
        if self.initfit:
            for particle in self.particles:
                fitness_cadidate = self.fitness(particle)
                if(particle.pbest_value > fitness_cadidate):
                    particle.pbest_value = fitness_cadidate
                    particle.pbest_position = particle.position
        else:
            for particle in self.particles:
                fitness_cadidate = particle.ft
                if(particle.pbest_value > fitness_cadidate):
                    particle.pbest_value = fitness_cadidate
                    particle.pbest_position = particle.position
            self.initfit = 1

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = particle.ft
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position
                self.gbest_particle = particle

    def move_particles(self):
        for particle in self.particles:
            global W
            new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                            (random.random()*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()

def run(n_iterations,n_particles,problem,mode):

    search_space = Space(10, target_error, n_particles,problem)

    if mode in ["iSN","iLN","iFW","iCN"]:
        Scope = mp.Mapping_Instrument(problem)
        search_space.initfit = 0
 
    mbudget = n_iterations/10
    
    # print(n_iterations,mbudget,n_iterations - mbudget , (n_iterations - mbudget)/n_particles )
    # return 

    if mode == "iSN":
        data = Scope.Starry_Night(mbudget,n_particles)
    elif mode == "iLN":
        # data = Scope.Lanterns(36,4,n_particles,2)
        data = Scope.Fireworks(mbudget/5,mbudget/5,4,n_particles,offset=0.25) # 5 px # 5%
        # data = Scope.Fireworks(mbudget/10,mbudget/10,9,n_particles,offset=0.25) # 10 px
    elif mode == "iFW":
        # data = Scope.Fireworks(12*10,12,5,n_particles,2)
        data = Scope.Fireworks(8*mbudget/10,2*mbudget/50,5,n_particles,offset=0.25) # 5 spr # 5%
        # data = Scope.Fireworks(8*mbudget/10,2*mbudget/100,10,n_particles,offset=0.25) # 10 spr
    elif mode == "iCN":
        data = Scope.Constellation(mbudget,n_particles,offset=0.25) # 5%
    
    if mode in ["iSN","iLN","iFW","iCN"]:
        for pixel in data: search_space.particles.append(Particle(problem,pixel))
    else:
        search_space.particles = [Particle(problem) for _ in range(search_space.n_particles)]

    # 750 + 8 * 25 200
    # 750 + 180 - 30 150
    search_space.print_particles()
    # input("")

    if mode in ["iSN","iLN","iFW","iCN"]:
        n_iterations -= mbudget
    
    if mode in ["mSN","mLN","mFW","mCN"]:
        n_iterations = n_iterations / ( n_particles + 1 )
    else:
        n_iterations = n_iterations / n_particles

    n_iterations = math.ceil(n_iterations)

    if mode == "PSO":
        n_iterations -= 1
    
    iteration = 0
    # n_iterations = 25
    while(iteration <= n_iterations  and not problem.final_target_hit):

        search_space.set_pbest()
        search_space.set_gbest()
        # print(  iteration )
        # if iteration == 1:
        #     # print("Ep: ","%02d"% iteration ," Val: ", '%.2f'% search_space.gbest_value)
        #     # print([round(x,2) for x in search_space.gbest_position] )
        #     pass
        #     # search_space.print_particles()

        if mode in ["mSN","mLN","mFW","mCN"] and iteration % 10 == 0 and iteration <>  0:
            # print( search_space.gbest_position )
            Scope = mp.Mapping_Instrument(problem,search_space.gbest_position)
 
            if mode == "mSN":
                data = Scope.Starry_Night(10,1)
            elif mode == "mLN":
                data = Scope.Lanterns(5,1,1,0.00005) # 0.001%
            elif mode == "mFW":
                data = Scope.Fireworks(6,2,2,1,0.00005) # 0.001%
            elif mode == "mCN":
                data = Scope.Constellation(10,1,0.00005) # 0.001%

            for pixel in data:

                if(search_space.gbest_value > pixel.fitness):
                    # print( 'bingo' )
                    search_space.gbest_value = pixel.fitness
                    search_space.gbest_position = pixel.position
                    search_space.gbest_particle.pbest_value = pixel.fitness
                    search_space.gbest_particle.pbest_position = pixel.position  

        # if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
        # if(search_space.gbest_value < search_space.target):
        #     break

        search_space.move_particles()
        iteration += 1
        global W
        W = 0.9 - 0.8 * (iteration/n_iterations)

    #print("The best solution is: ", search_space.gbest_position, " in n_iterations: ", iteration)
    # print("The best position is ", search_space.gbest_position, "in iteration number ", iteration, "Fitness:" , search_space.gbest_value , search_space.target,search_space.target_error)
    
    # print("Ep: ","%02d"% iteration ," Val: ", '%.2f'% search_space.gbest_value)
    # print([round(x,2) for x in search_space.gbest_position] )            
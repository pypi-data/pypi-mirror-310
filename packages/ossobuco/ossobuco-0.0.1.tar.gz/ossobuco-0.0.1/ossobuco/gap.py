import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import curve_fit

class Gap:
    """To simulate filling of gap between two surfaces by discrete particles.

    Args:
        imput_parameters (`dict`): dictionary with input parameters
        
    """
    
    def __init__(self, input_parameters: dict):
        
        ### GET PARAMETERS
        # params for x axis discretization
        self.xmax = input_parameters.get('xmax')
        self.res = input_parameters.get('xaxis_resolution')

        # params for curvature of surfaces
        self.amplitude_up = input_parameters.get('amplitude_up')
        self.amplitude_low = input_parameters.get('amplitude_low')
        self.phi_up = input_parameters.get('phi_up')
        self.phi_low = input_parameters.get('phi_low')

        # params for altitude of surfaces
        self.alt_up = input_parameters.get('alt_up')
        self.alt_low = input_parameters.get('alt_low')

        # param for height of unit product you form
        self.hprod = input_parameters.get('h_prod')

        # compute width or unit product formed
        self.wprod = self.xmax/self.res

        # params for interaction
        self.interaction_touch = input_parameters.get('interaction_touch')

        # seed for reproducibility of sim but repetitions
        self.seed = input_parameters.get('seed')


        ### SET GAP GEOMETRY from parameters
        
        # set your x axis with given resolution
        self.xaxis = np.linspace(0, self.xmax, self.res * self.xmax)
        self.xaxis_indices = np.arange(len(self.xaxis))
        
        # function to set surfaces
        def sinusoidal(x, amplitude, phi, altitude):
            return amplitude*(np.sin(x + phi)) + altitude - amplitude
        
        def step(x, y1):
            return np.full_like(x, y1)
            

        fct = input_parameters.get('fct')           

        if fct == 'flat':
            pass

        if fct == 'keil':
            pass

        if fct == 'quadratic':
            pass

        if fct == 'sin':
            # define upper and lower surfaces
            self.h_up = sinusoidal(self.xaxis, self.amplitude_up, self.phi_up, self.alt_up)
            self.h_low = sinusoidal(self.xaxis, self.amplitude_low, self.phi_low, self.alt_low)

            # define dummy surfaces for the gifs
            self.h_up_gif = sinusoidal(self.xaxis, self.amplitude_up, self.phi_up, self.alt_up)
            self.h_low_gif = sinusoidal(self.xaxis, self.amplitude_low, self.phi_low, self.alt_low)


        if fct == 'step':
            # define upper and lower surfaces
            self.h_up = step(self.xaxis, self.alt_up)
            self.h_low = step(self.xaxis, 0)

            # define dummy surfaces for the gifs
            self.h_up_gif = step(self.xaxis, self.alt_up)
            self.h_low_gif = step(self.xaxis, 0)

            
        # compute gap between surfaces at each point and store in list
        self.gaps_list = self.h_up - self.h_low

        # initialise lists for plotting output
        self.npart_plotlist = [0]
        self.gapineraction_plotlist = [0]

        # initialise lists amd tracker for gifs
        self.filling_displayer_up = [np.array(self.h_up_gif)] # access value not memory address
        self.filling_displayer_low = [np.array(self.h_low_gif)] # access value not memory address

        self.k_tracker = []
    
        # compute width or unit product you form from xmax and xaxis_resolution
        self.wprod = self.xmax/self.res
     

    def display_geometry(self, **kwargs):

        ax = kwargs.get('ax', None)
        new_figure = True if ax is None else False

        if new_figure:
            fig, ax = plt.subplots()

        ax.plot(self.xaxis, self.h_up, marker='x', label=r"$h_{up}$", c='0.6')
        ax.plot(self.xaxis, self.h_low, marker='x', label=r"$h_{low}$", c='0.1')

        ax.vlines(self.xaxis, self.h_low, 
                  self.h_up, color='0.4', 
                  label=r"D(x)", lw=1)


        ax.set_xlabel('x')
        ax.set_ylabel('h(x)')
        ax.legend()




    def fill(self):
        # set a seed for reproducibility
        random.seed(self.seed)

        # initialise number of particles and current gap interaction
        n_part = 0
        gap_interaction = 0

    
        # initialise an interaction tracker, has len(x) and starts with zeroes only
        # at each x position it will keep track of the contribution of gap(x) towards the total interaction
        interaction_tracker = np.zeros(len(self.xaxis))

        d_updt = self.gaps_list
        d_sum = sum(d_updt)


        # while gap not full
        THRESHOLD = self.hprod*1e-5
        while d_sum > THRESHOLD:
            # pick a surface at random, 1 is low, 2 is up
            k = random.randint(1,2)
            # print(f"k = {k}")

            rnd_idx = random.randint(0, self.xaxis.size - 1)
            # print(f"random index = {rnd_idx}")

            # print(f"up: {self.h_up_gif}")
            # print(f"low: {self.h_low_gif}")


            d_chosen_x = d_updt[rnd_idx]

            # if I can still place particles at this x position
            if d_chosen_x > 0:

                # you can still place a particle, so you will have to display it
                # track the surface to display
                self.k_tracker.append(k)
                # update filling displayer
                if k == 1:
                    self.h_low_gif[rnd_idx] += self.hprod
                elif k == 2:
                    self.h_up_gif[rnd_idx] -= self.hprod


                l = np.array(self.h_low_gif) # get value not address in memory lol
                self.filling_displayer_low.append(l)
                
                m = np.array(self.h_up_gif) # get value not address in memory lol
                self.filling_displayer_up.append(m)

                # print(f"self filling displayer up {self.filling_displayer_up}")
                # print(f"self filling displayer low {self.filling_displayer_low}")                
                # print()



                # add the size of a particle
                d_chosen_x -= self.hprod
                diff = self.hprod

                # count the added particle
                n_part += 1
                self.npart_plotlist.append(n_part)
                

                # regarding the interaction to count, depends if you bridged the gap or not
                # if you bridged the gap, add a touch interaction

                if d_chosen_x <= 0:
                    # set distance to zero and update gaps list
                    diff = d_updt[rnd_idx]
                    d_chosen_x = 0
                    d_updt[rnd_idx] = d_chosen_x 
                    
                    interaction_tracker[rnd_idx] = self.interaction_touch


                    # compute and update total gap interaction
                    gap_interaction = sum(interaction_tracker)
                    
                    # update gap interaction list for plot
                    self.gapineraction_plotlist.append(gap_interaction)

                    d_sum -= abs(diff)


                    

                # if you are not close to bridging, just add a particle
                else:

                    # # compute and update total gap interaction
                    gap_interaction = sum(interaction_tracker)
                    
                    # update gap interaction list for plot
                    self.gapineraction_plotlist.append(gap_interaction)

                    # update gaps list
                    d_updt[rnd_idx] = d_chosen_x 
                    

                    # faaaaast
                    d_sum -= abs(diff)

                
                


    def extract_results(self):
        return np.array(self.npart_plotlist), np.array(self.gapineraction_plotlist)



    def plot_output(self, **kwargs):
        ax = kwargs.get('ax', None)
        new_figure = True if ax is None else False

        if new_figure:
            fig, ax = plt.subplots()
        

        norm = kwargs.get('norm', False)
        if not norm:
            x = np.array(self.npart_plotlist)
            y = np.array(self.gapineraction_plotlist)
        elif norm:
            V_current = np.array(self.npart_plotlist)*self.hprod
            V_gap = self.xmax*self.res*(self.alt_up-self.alt_low)
            max_interaction = self.xmax*self.res*self.interaction_touch
            x = V_current/V_gap
            y = np.array(self.gapineraction_plotlist)/max_interaction


        ax.plot(x, y, label='output')


        fit = kwargs.get('fit', False)
        if fit:

            def fit(x, a, b):
                return a*np.exp(b*x) - a

            p, pc = curve_fit(fit, x, y,
                              p0=([0.1,0.1]))

            print(p)

            ax.plot(x, fit(np.array(self.npart_plotlist), *p), label='fit')

        ax.set_xlabel(r"Number of particles added")
        ax.set_ylabel(r"Gap Interaction")
        ax.legend()
    
    
    def display_gap_at_timestep(self, **kwargs):

        # set base figure setup
        ax = kwargs.get('ax', None)
        new_figure = True if ax is None else False

        if new_figure:
            fig, ax = plt.subplots()

        ax.plot(self.xaxis, (self.h_up), c='0.3')
        ax.plot(self.xaxis, (self.h_low), c='0.3')

        # plot cement surfaces - grey
        ax.fill_between(np.sort(self.xaxis), (self.h_up), max((self.h_up)) + 1, color='0.5')
        ax.fill_between(np.sort(self.xaxis), (self.h_low), -max(abs((self.h_low))) - 1, color='0.5')

        # print max number of timesteps
        max_timesteps = len(self.k_tracker) 

        print(f"max number of timesteps = {max_timesteps}")
        print(f"By default, displaying gap at half the simulation")

        tstep = kwargs.get('timestep', int(max_timesteps/2))

        if tstep > max_timesteps or tstep < 0:
            tstep = max_timesteps

        ax.fill_between(np.sort(self.xaxis), (self.h_low), (self.filling_displayer_low[tstep]), color='0.7')
        ax.fill_between(np.sort(self.xaxis), (self.h_up), (self.filling_displayer_up[tstep]), color='0.7')
        
        # # uncomment if you want contour of products
        # ax.plot(np.sort(self.xaxis), (self.filling_displayer_low[tstep]), color='0.2', alpha=0.3)
        # ax.plot(np.sort(self.xaxis), (self.filling_displayer_up[tstep]), color='0.2', alpha=0.3)

        plt.show()




    def generate_gap_and_plot_gif(self, output_filename='gif.gif', interval=400, repeat_delay=1200):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6,4))
        

        max_timesteps = len(self.k_tracker) + 1
        print(f"Max number of timesteps = {max_timesteps -1 }")

        def update(frame):
            ax1.clear()
            ax2.clear()
            
            # Plot gap filling on ax1
            ax1.plot(self.xaxis, self.h_up, c='0.3')
            ax1.plot(self.xaxis, self.h_low, c='0.3')

            ax1.fill_between(np.sort(self.xaxis), self.h_up, max(self.h_up) + 1, color='0.5')
            ax1.fill_between(np.sort(self.xaxis), self.h_low, -max(abs(self.h_low)) - 1, color='0.5')


            ax1.fill_between(np.sort(self.xaxis), self.h_low, self.filling_displayer_low[frame], color='0.7')
            ax1.fill_between(np.sort(self.xaxis), self.h_up, self.filling_displayer_up[frame], color='0.7')


            # Plot n against j on ax2
            ax2.plot(self.npart_plotlist[0:frame+1], self.gapineraction_plotlist[0:frame+1])
            ax2.set_xlim(-1, 1.05*max(self.npart_plotlist))
            ax2.set_ylim(-2, 1.05*max(self.gapineraction_plotlist))
            ax2.set_xlabel('Number of particles added')
            ax2.set_ylabel('Gap interaction')

            fig.suptitle(f'Timestep {frame}/{max_timesteps -1}')

            plt.tight_layout()

        # Create the animation with a lower interval (increase interval value for slower speed)
        animation = FuncAnimation(fig, update, frames=max_timesteps, interval=interval, repeat=False, repeat_delay=repeat_delay)


        # Save the animation as a GIF
        animation.save(output_filename, writer='imagemagick')

        plt.show()















    def store_sim_in_db(self):
        pass

    def postprocess(self):
        # from ossobuco entry
        # but not sure here is the correct place to do it
        pass


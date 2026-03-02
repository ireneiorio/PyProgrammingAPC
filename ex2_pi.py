#!/usr/bin/env python3
"""
	Moduel to compute numerically pi
"""

import sys

import random

## global rvariable setting the radius to 1
THRESHOLD = 1.

def extract_coords(lower:float=0., higher:float=1.)->list:
    """
        Function to extract two random numbers from a uniform distribution on an interval between lower bound equal to lower and upper bound equal to higher
        
        Parameters:
        -----------
                   lower: float, default = 0. Lower bound on extraction of the coordinate couple
                   higher: float, default = 1. Upper bound on extraction of the coordinate couple
        Returns:
        -----------
                [x, y]: list. Coordinate tuple with x random float number from uniform distribution between lower (0. by default) and higher (1. by default), y random float number from uniform
                               distribution between lower (0. by default) and higher (1. by default)
    """
    x = random.uniform(lower, higher)
    y = random.uniform(lower, higher)

    return [x, y]


def extract_full_coords(nsteps:int, lower:float=0., higher:float=1.)->list:
    """
        Function to extract nsteps couples of random numbers from uniform distribution with lower bound equal to lower and higher bound equal to higher
        
        Parameters:
        -----------
                   nsteps: integer. Number of times the process has to be repeated (number of couples you will extract)
		   lower: float, default = 0. Lower bound on extraction of the radius
                   higher: float, default = 1. Upper bound on extraction of the radius
        Returns:
        -----------
                   coords: list. Coordinate list. Each element of the list is a couple [x, y], with with x random float number from uniform distribution
                                 between lower and higher, y random float number from uniform distribution between lower and higher
    """
    coords = [] #empty list
    for i in range(0, nsteps, 1):
        #extract each coordinate couple and append it to the empty list
        coords.append(extract_coords(lower, higher))
    
    return coords  



def compute_radius(lower:float = 0., higher:float = 1.)->float:
    """
        Extract two values of x, y coordinates from uniform distribution on interval between lower na higher, then compute the radius
        from the two coordinates x, y as r = sqrt(x^2 + y^2)
        
        Parameters:
        -----------
                   lower: float, default = 0. Lower bound over which the x and y coordinates were extracted = lower bound on the radius
                   higher: float, default = 1. Upper bound over which the x and y coordinates were extracted = lower bound on the radius
        Returns:
        -----------
                   r: float. Radius computed as square mean root of the sum between x to the power of two and y to the power of two
    """
    #unpack the couple output from the function extract_coords
    xcoord, ycoord = extract_coords(lower, higher)
    #compute r as sqrt(x**2 + y**2)
    rsquared = xcoord**2 + ycoord**2
    
    return rsquared



def check_internal(nsteps:int, lower:float= 0., higher:float=1., threshold:float=1.)->tuple:
    """
        Function that computes radii and saves only those that are smaller than the value contained in threshold.
        This is done by extracting one radisu, checking if it is smaller than threshold. If it is appending it to a list of accepted radii.
        The operation is repeated nsteps times.

        Parameters:
        -----------
                    nsteps: integer. Number of times the operation must be executed
                    lower: float, default = 0. Lower bound over on the radius
                    higher: float, default = 1. Upper bound over on the radius
                    threshold: float, default = 1. Maximum value of the radius. For the estimate of pi, it is by default set to 1.
        Returns:
        ----------
                    j: integer. The number of accepted radii
    """
    #check if one radius is within the circle of radius 1, the repeat the operation nsteps times:
    #accepted_r = [] #list of accepted rs
    j = 0
    for i in range(0, nsteps, 1):
        rsquared = compute_radius(lower, higher)
        
        if (rsquared <= threshold):
	    #too memory expensive
            #accepted_r.append(r)
            j += 1 #counter
    
    return j



def estimate_pi(nsteps:int, lower:float= 0., higher:float=1., threshold:float=1.)->float:
    """
         Compute pi from the formula: pi/4 = r^2, with r = 1, then pi = 4*(r^2). In this case, r = number of accepted radii/total number of extracted radii

         Parameters:
        -----------
                    nsteps: integer. Number of times the operation must be executed
                    lower: float, default = 0. Lower bound on the radius
                    higher: float, default = 1. Upper bound on the radius
                    threshold: float, default = 1. Maximum value of the radius. For the estimate of pi, it is by default set to 1.
        Returns:
        ----------
                    pi_est: float. Estimate of pi.

    """
    number = check_internal(nsteps, lower, higher, threshold)
    
    #old consistency check but now no more raddi as outout
    #if len(radii) != number:
    #    #safety check
    #    raise ValueError('The number of accepted points is not as long as the list of saved radii')
    pi_est = (number/nsteps)*4.

    
    return pi_est


def compute_mean(list_arg:list)->float:
    """
        Function to compute the mean value of the elements of a list. The mean is computed as the sum of all the elements of the list,
        divided by its lenght

        Parameters:
        -----------
                    list_arg: list. List of floats
        Returns:
        -----------
                    mean: float. Mean of the list: sum of all the elements in the list, divided by its length
    """
    summed = sum(list_arg)
    mean = summed/len(list_arg)
    
    return mean

def jack_knife(nsteps:int, ntimes:int, lower:float=0., higher:float=1., threshold:float=1.)->tuple:
    """
        Fuction that computes pi and the error associated with its numerical estimate through jackknife resampling. Given an array of elements n,
        Jackknife resampling works by taking one out one element at a time, getting an array of n-1 elements each time and considering each subset
        of the original array as an independent dataset. The statistics are computed on each 'independent' subset, then they are combined to give the
        overall estimate of the mean. The variance is computed with the usual variance formula (for informal + detailed explanation of the Jackknife
        see Geek for Geeks [http://www.geeksforgeeks.org/data-science/jackknife-resampling/]).
        In this specific function, then, one estimates the value of pi nsteps times, then computes the average value of pi by applying
        Jackknife resampling ntimes times, and the error associated with it through the variance. The parameters lower, higher, threshold are
        necessary for the functions that are used to estimate the radii and compute pi.

        Parameters:
        -----------
                    nsteps: integer. Number of times that the fuction estimates the value of pi.
                    ntimes: integer. Number of times for which the original array is resampled in the jackkinfe sample. Must be equal to nsteps
                                    for correct statistical analysi. The two values are distinguished to make it easier to test the functioning
                    lower: float, default = 0. Lower bound on the radius
                    higher: float, default = 1. Upper bound on the radius
                    threshold: float, default = 1. Maximum value of the radius. For the estimate of pi, it is by default set to 1.
        Returns:
        --------
                  mean_jack, var_jack, means: tuple. The tuple is formed by:
                  
                        *** mean_jack: float. Final result for the mean value of pi, computed through jackknife resampling
                        *** var_jack: float. Variance of the array of values of pi
                        *** means: array of floats. Contains the means of the values of pi, each computed on a subset of elements
                                  of the original array, obtained by taking one element out through jackknife resampling.
    """
    #the parameter ntimes is good to test the functioning of jackknife on long arrays but it must always be set to be equal to ntimes to get statistically correct results
    pi_estimates = [] #list for pi estimates
    
    for step in range(0, nsteps, 1): #compute the mean
        pi_estimates.append(estimate_pi(nsteps, lower, higher, threshold))
    
    means = []

    #mean over the entire dataset, so over the array of length n: (theta hat)
    mean_overall = sum(pi_estimates)/len(pi_estimates)
    
    l0 = len(pi_estimates) #initial length of pi_estimates
    print('initial length', l0)

    for i in range(0, l0, 1):
        #take the original (array) list in this case, the element i, then take the elements of the list UP to i, and the elements AFTER i, and append them otether in a new list
        #this is a new data set of n-1 elements that does not contain the ith element. Repeat the operation for each element of the list.
        #like this, jackknife has new samples of size n-1 from the same original data set
        reduced = pi_estimates[:i] + pi_estimates[i+1:]
        means.append(compute_mean(reduced))
    
    mean_jack = sum(means)/len(means) #since means is as long as pi_estimates, this is right

    addends = [(elem - mean_jack)**2 for elem in means]
    #variance computation:
    var_jack = (len(means)/(len(means)-1))*sum(addends)
    
    print('Estimate of mean:', mean_jack)
    print('Estimate of variance:', var_jack)
    
    return mean_jack, var_jack, means

#############################################################################################################################################################################################
#main
def main():
    #first error handling: if user does not give the proper arguments
    if len(sys.argv) !=6:
        print('**** This function computes numerically the value of pi. To use it, run: ex2_pi.py <nsteps> <ntimes> <lower> <higher> <threshold>')
        sys.exit(1) #to signal an error
    nsteps = int(sys.argv[1])
    ntimes = int(sys.argv[2])
    lower =  float(sys.argv[3])
    higher = float(sys.argv[4])
    threshold = float(sys.argv[5])
	    
    mean_pi, var_pi, means = jack_knife(
					nsteps, ntimes, lower, higher, threshold
    )

if __name__=='__main__':
	main()

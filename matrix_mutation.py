#mutation function with only three calls, much faster than a for loop
#sample parameters, but easy to swap in for our data
mat_size = 2000
l = 200
z = np.zeros((mat_size,l))

def matrix_mutation () :
        #r is a frame sized 2D array of randommly assigned booleans
        r = np.random.random(size=(mat_size,l))<0.5
        #v is a frame sized 2D array of random values
        v = np.random.random(size=(mat_size,l))
        #values of k will either be the intital z value (0 in this case), or the value of the corresponding v
        k = r*v + np.logical_not(r)*z
        print(v)
        print(k)
matrix_mutation()

from matplotlib import pyplot as plt

def plot(best_values):
    
    # Saves the best values for each generation into the respective generation number (x), and the value itself (y)
    y = best_values
    x = [0, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    
    # Creates a scatter plot with x & y values
    plt.scatter(x, y, color='blue')
    
    # Variables for the plot
    plt.title('Best Values Per Generation')
    plt.ylabel('Value')
    plt.xlabel('Generation Number')
    plt.axis([-5, 25, 0.983, 0.9865])
    
    plt.show()
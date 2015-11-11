from matplotlib import pyplot as plt

def plot(best_values):
    
    # Saves the best values for each generation into the respective generation number (x), and the value itself (y)
    y = best_values
    x = []
    count = 0
    for i in best_values:
        x.append(count)
        count += 1
        
    # Creates a scatter plot with x & y values
    plt.scatter(x, y, color='blue')
    
    # Variables for the plot
    plt.title('Best Values per Generation')
    plt.ylabel('Value')
    plt.xlabel('Generation Number')
    plt.axis([-5, 25, 0.983, 0.988])
    
    plt.show()
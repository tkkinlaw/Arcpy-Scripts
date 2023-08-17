from tqdm import tqdm
import time

# Define the total number of iterations/steps in your task
total_iterations = 100

# Create a progress bar object using tqdm with the specified total iterations
progress_bar = tqdm(total=total_iterations, desc="Processing", unit="iteration")

# Simulate some task that takes time for each iteration (you can replace this with your own code)
for i in range(total_iterations):
    # Perform some task here...
    time.sleep(0.1)  # Simulating delay

    # Update the progress bar by incrementing its value
    progress_bar.update(1)

# Close the progress bar once the loop is finished
progress_bar.close()
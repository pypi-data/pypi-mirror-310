import numpy as np
import time
import psutil
import threading
import pandas as pd
import os
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
# from tensorflow.keras.datasets import mnist
# from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns

class EnergyConsumptionDL:
    def __init__(self, model, pcpu_idle, pcpu_full):
        """
        Initialize the class for tracking energy efficiency during training.
        
        :param model: The Keras model to train.
        :param pcpu_idle: Idle power consumption of the CPU (in watts).
        :param pcpu_full: Full load power consumption of the CPU (in watts).
        """
        self.model = model
        self.pcpu_idle = pcpu_idle  # CPU power when idle
        self.pcpu_full = pcpu_full  # CPU power at full utilization
        self.cpu_logs = []
        self.memory_logs = []
        self.power_logs = []  # New list to track power consumption
        self.energy_logs = []  # New list to track energy consumption
        self.start_time = None
        self.end_time = None
        self.monitor_thread = None
        self.monitoring = False

    def _monitor_system_usage(self):
        """
        Monitors the system CPU and memory utilization in the background.
        """
        while self.monitoring:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            self.cpu_logs.append(cpu_percent / 100)  # Store CPU utilization as α (0 to 1)
            self.memory_logs.append(memory_percent)

            # Calculate power consumption
            power_consumption = ((1 - (cpu_percent / 100)) * self.pcpu_idle) + ((cpu_percent / 100) * self.pcpu_full)
            self.power_logs.append(power_consumption)

            # Calculate energy consumption (in Joules) during the 1-second interval
            energy_consumption = power_consumption  # Since it's for one second
            if self.energy_logs:
                self.energy_logs.append(self.energy_logs[-1] + energy_consumption)
            else:
                self.energy_logs.append(energy_consumption)

    def fit(self, x_train, y_train, epochs=5, batch_size=64, validation_split=0.2):
        """
        Train the model while tracking CPU and memory utilization.
        
        :param x_train: Training data.
        :param y_train: Training labels.
        :param epochs: Number of epochs to train the model.
        :param batch_size: Size of batches to use for training.
        :param validation_split: Fraction of training data to use for validation.
        """
        # Start monitoring system usage in a separate thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_system_usage)
        self.monitor_thread.start()

        self.start_time = time.time()
        
        # Train the model
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

        self.end_time = time.time()
        
        # Stop monitoring and wait for the monitoring thread to finish
        self.monitoring = False
        self.monitor_thread.join()

    def evaluate(self, x_test, y_test):
      """
      Evaluate the model on the test set.
      
      :param x_test: Test data.
      :param y_test: Test labels.
      :return: Test loss and accuracy.
      """
      results = self.model.evaluate(x_test, y_test, verbose=1)
  
      # Ensure only the first two metrics (loss and accuracy) are returned
      test_loss = results[0]
      test_acc = results[1]
  
      print(f"Evaluation Results: {results}")
      return test_loss, test_acc


    def generate_report(self, x_train, y_train, x_test, y_test, epochs=5, batch_size=64, validation_split=0.2, backgroundColor='#f0f0f0'):
        """
        Generate a report on CPU and memory utilization, power, energy, and model performance.
        """
        # Train the model
        self.fit(x_train, y_train, epochs, batch_size, validation_split)

        # Calculate average CPU and memory utilization
        self.avg_cpu_utilization = np.mean(self.cpu_logs)
        self.avg_memory_utilization = np.mean(self.memory_logs)

        # Calculate total training time
        self.training_time = self.end_time - self.start_time

        # Power consumption calculation
        self.power_consumption = ((1 - self.avg_cpu_utilization) * self.pcpu_idle) + (self.avg_cpu_utilization * self.pcpu_full)

        # Energy consumption calculation
        self.energy_consumption = self.training_time * self.power_consumption

        # Evaluate the model
        test_loss, test_acc = self.evaluate(x_test, y_test)

        # Print the final report
        print(f"--- Training Report ---")
        print(f"Training Time: {self.training_time:.2f} seconds")
        print(f"Average CPU Utilization: {self.avg_cpu_utilization * 100:.2f}%")
        print(f"Average Memory Utilization: {self.avg_memory_utilization:.2f}%")
        print(f"Power Consumption: {self.power_consumption:.2f} W")
        print(f"Energy Consumption: {self.energy_consumption:.2f} J (Joules)")
        print(f"Test Accuracy: {test_acc:.4f}")
        
        # Sample data (replace these with your actual report variables)
        training_time = self.training_time  # Replace with actual value
        avg_cpu_utilization = self.avg_cpu_utilization * 100  # Replace with actual value
        avg_memory_utilization = self.avg_memory_utilization  # Replace with actual value
        power_consumption = self.power_consumption  # Replace with actual value
        energy_consumption = self.energy_consumption  # Replace with actual value
        test_accuracy = test_acc  # Replace with actual value
        
        # File name
        file_name = 'ResultsDL.csv'
        
        # Create a DataFrame with the new data
        new_data = pd.DataFrame({
            "Training Time (s)": [training_time],
            "Average CPU Utilization (%)": [avg_cpu_utilization],
            "Average Memory Utilization (%)": [avg_memory_utilization],
            "Power Consumption (W)": [power_consumption],
            "Energy Consumption (J)": [energy_consumption],
            "Test Accuracy": [test_accuracy]
        })
        
        # Check if the file exists
        if os.path.isfile(file_name):
            # If the file exists, append the data without writing the header
            new_data.to_csv(file_name, mode='a', header=False, index=False)
        else:
            # If the file doesn't exist, write the data with the header
            new_data.to_csv(file_name, mode='w', index=False)
        
        print(f"Report saved to {file_name}")

        # Plot usage metrics
        self.plot_metrics(backgroundColor)
    
    def plot_metrics(self, backgroundColor = '#f0f0f0'):
        """
        Plots CPU utilization, power consumption, energy consumption, and memory utilization with modern styling.
        """
    
        sns.set(style="darkgrid", palette="muted", rc={'figure.figsize': (12, 8)})  # Dark grid style

        # Create subplots
        fig, axs = plt.subplots(2, 2, sharex=True)
        fig.suptitle("System Utilization During Model Training", fontsize=20, fontweight='bold', color='black')

        # CPU Utilization Plot
        min_val = min(self.cpu_logs)
        max_val = max(self.cpu_logs)
        
        # Normalizing the CPU logs to be between 0 and 100
        normalized_cpu_logs = [val * 100 for val in self.cpu_logs]
        
        axs[0, 0].plot(normalized_cpu_logs, color='blue', linewidth=2, marker='o', markersize=5, label=f'Avg. CPU Utilization {round(self.avg_cpu_utilization * 100, 2)}%')
        axs[0, 0].fill_between(range(len(normalized_cpu_logs)), normalized_cpu_logs, color='cyan', alpha=0.1)
        axs[0, 0].set_title("CPU Utilization (0 to 100%)", fontsize=16, color='black')
        axs[0, 0].set_ylabel("(%)", fontsize=14, fontweight='bold', color='black')
        axs[0, 0].grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
        axs[0, 0].legend()
        axs[0, 0].set_facecolor(backgroundColor)

        # Memory Utilization Plot
        axs[0, 1].plot(self.memory_logs, color='lime', linewidth=2, marker='o', markersize=5, label=f'Avg. Memory Utilization {self.avg_memory_utilization:.2f}%')
        axs[0, 1].fill_between(range(len(self.memory_logs)), self.memory_logs, color='lime', alpha=0.1)
        axs[0, 1].set_title("Memory Utilization (%)", fontsize=16, color='black')
        axs[0, 1].set_ylabel("(%)", fontsize=14, fontweight='bold', color='black')
        axs[0, 1].grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
        axs[0, 1].legend()
        axs[0, 1].set_facecolor(backgroundColor)

        # Power Consumption Plot
        axs[1, 0].plot(self.power_logs, color='orange', linewidth=2, marker='o', markersize=5, label=f'Avg. Power Consumption {self.power_consumption:.2f} W')
        axs[1, 0].fill_between(range(len(self.power_logs)), self.power_logs, color='orange', alpha=0.1)
        axs[1, 0].set_title("Power Consumption (W)", fontsize=16, color='black')
        axs[1, 0].set_ylabel("(W)", fontsize=14, fontweight='bold', color='black')
        axs[1, 0].set_xlabel("Time (seconds)", fontsize=14, fontweight='bold', color='black')
        axs[1, 0].grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
        axs[1, 0].legend()
        axs[1, 0].set_facecolor(backgroundColor)

        # Energy Consumption Plot
        axs[1, 1].plot(self.energy_logs, color='purple', linewidth=2, marker='o', markersize=5, label=f'Max. Energy Consumption {self.energy_consumption:.2f} J')
        axs[1, 1].fill_between(range(len(self.energy_logs)), self.energy_logs, color='purple', alpha=0.1)
        axs[1, 1].set_title("Energy Consumption (J)", fontsize=16, color='black')
        axs[1, 1].set_ylabel("(J)", fontsize=14, fontweight='bold', color='black')
        axs[1, 1].set_xlabel("Time (seconds)", fontsize=14, fontweight='bold', color='black')
        axs[1, 1].grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
        axs[1, 1].legend()
        axs[1, 1].set_facecolor(backgroundColor)

        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.subplots_adjust(hspace=0.2)  # Add space between subplots
        plt.show()

    def plot_relationships(self, backgroundColor='#f0f0f0'):
        """
        Plots the relationships between system metrics (CPU vs Power, CPU vs Energy, Energy vs Power)
        with enhanced visibility and density contours for highlighting areas with more dots.
        """
        sns.set(style="whitegrid", palette="muted", rc={'figure.figsize': (10, 6)})  # Modern styling

        # Function to plot scatter with density highlights
        def plot_with_density(x, y, xlabel, ylabel, title, color):
            plt.figure()
            sns.scatterplot(x=x, y=y, color=color, alpha=0.7, edgecolor='black', s=50, label="Data Points")
            sns.kdeplot(x=x, y=y, levels=5, color='red', linewidths=1.5, alpha=0.6, label="Density Contours")
            plt.title(title, fontsize=18, fontweight='bold', color='black')
            plt.xlabel(xlabel, fontsize=14, fontweight='bold', color='black')
            plt.ylabel(ylabel, fontsize=14, fontweight='bold', color='black')
            plt.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
            plt.legend(fontsize=12)
            plt.gca().set_facecolor(backgroundColor)
            plt.tight_layout()
            plt.show()

        # CPU Utilization vs Power Consumption
        plot_with_density(
            x=self.cpu_logs,
            y=self.power_logs,
            xlabel="CPU Utilization (%)",
            ylabel="Power Consumption (W)",
            title="CPU Utilization vs Power Consumption",
            color="blue"
        )

        # CPU Utilization vs Energy Consumption
        plot_with_density(
            x=self.cpu_logs,
            y=self.energy_logs,
            xlabel="CPU Utilization (%)",
            ylabel="Energy Consumption (J)",
            title="CPU Utilization vs Energy Consumption",
            color="orange"
        )

        # Energy Consumption vs Power Consumption
        plot_with_density(
            x=self.energy_logs,
            y=self.power_logs,
            xlabel="Energy Consumption (J)",
            ylabel="Power Consumption (W)",
            title="Energy Consumption vs Power Consumption",
            color="green"
        )





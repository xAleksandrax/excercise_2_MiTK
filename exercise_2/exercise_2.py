import hashlib
import time
import tkinter as tk
from tkinter import filedialog
import timeit
import plotly.graph_objects as go

class Exercise_2:
    def __init__(self, root, algorithm_var, entry, result_text):
        """
        :param root: Object of the application window
        :param algorithm_var: Variable holding the selected hashing algorithm by the user
        :param entry: Text field where the user can input the file path
        :param result_text: Text field where hashing results and messages are displayed
        """
        self.root = root
        self.algorithm_var = algorithm_var
        self.entry = entry
        self.result_text = result_text

    def hash_file(self, filename, algorithm):
        """
        Function to hash the file selected by the user using the chosen hashing algorithm

        :param filename: Path to the file to be hashed
        :param algorithm: Hashing algorithm selected by the user
        :return: Hash result or None if the file is not found
        """
        try:
            with open(filename, 'rb') as f:
                hash_obj = hashlib.new(algorithm)
                while chunk := f.read(4096):
                    hash_obj.update(chunk)
                return hash_obj.hexdigest()
        except FileNotFoundError:
            return None

    def browse_file(self):
        """
        Function to open a dialog window for the user to choose the file to hash
        """
        filename = filedialog.askopenfilename()
        if filename:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, filename)

    def hash_and_display(self):
        """
        Function for interaction with the interface; Displays messages in the window - hashing time, result.
        """
        selected_algorithm = self.algorithm_var.get()
        filename = self.entry.get()

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Hashing...")
        self.root.update()

        start_time = time.time()
        hash_result = self.hash_file(filename, selected_algorithm)
        end_time = time.time()

        if hash_result:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Selected algorithm: {selected_algorithm}\nHash: {hash_result}\n")
            self.result_text.insert(tk.END, f"Hashing time: {end_time - start_time:.5f}")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "File not found.")

    def hash_message(self, message, algorithm):
        """
        Function to hash a text message using the selected algorithm.

        :param message: Text message to be hashed
        :param algorithm: Hashing algorithm selected by the user
        :return: Hash result
        """
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(message.encode('utf-8'))
        return hash_obj.hexdigest()

    def measure_hashing_time(self, message_sizes, algorithm):
        """
        Function to measure hashing time for different message sizes.

        :param message_sizes: List with different message sizes from the plot_time() function
        :param algorithm: Hashing algorithm selected by the user
        :return: List with hashing times for each size provided in the plot_time() function
        """
        times = []
        for size in message_sizes:
            message = 'a' * size
            time_taken = timeit.timeit(lambda: self.hash_message(message, algorithm), number=10) / 10
            times.append(time_taken)
        return times

    def run_app(self):
        """
        Function to run the application window.
        """
        self.root.title("File Hashing")

        algorithm_label = tk.Label(self.root, text="Choose hashing algorithm:")
        algorithm_label.pack()

        self.algorithm_var.set("md5")
        algorithm_menu = tk.OptionMenu(self.root, self.algorithm_var, *hashlib.algorithms_available)
        algorithm_menu.pack()

        file_label = tk.Label(self.root, text="File path:")
        file_label.pack()

        self.entry.pack()

        browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        browse_button.pack()

        hash_button = tk.Button(self.root, text="Hash File", command=self.hash_and_display)
        hash_button.pack()

        self.result_text.pack()

        def plot_time():
            message_sizes = [10, 100, 1000, 10000, 100000]
            algorithm = self.algorithm_var.get()
            times = self.measure_hashing_time(message_sizes, algorithm)

            fig = go.Figure(data=go.Scatter(x=message_sizes, y=times, mode='lines+markers'))
            fig.update_layout(title='Hashing Time vs Message Size',
                              xaxis_title='Message Size',
                              yaxis_title='Time (s)')
            fig.show()

        plot_button = tk.Button(self.root, text="Show Hashing Time Plot", command=plot_time)
        plot_button.pack()

        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    algorithm_var = tk.StringVar()
    entry = tk.Entry(root, width=50)
    result_text = tk.Text(root, height=5, width=50)
    app = Exercise_2(root, algorithm_var, entry, result_text)
    app.run_app()

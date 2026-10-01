import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

appliances = []

# Function to add appliance
def add_appliance():
    name = entry_name.get()
    power = entry_power.get()
    hours = entry_hours.get()
    days = entry_days.get()
    unit_type = var_type.get()

    if not name or not power or not hours or not days:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        power = float(power)
        hours = float(hours)
        days = float(days)

        # Convert HP to Watts if needed
        if unit_type == "HP":
            power = power * 746

        appliances.append((name, power, hours, days))

        listbox.insert(tk.END, f"{name} - {power}W, {hours}h/day, {days} days")

        # Clear fields
        entry_name.delete(0, tk.END)
        entry_power.delete(0, tk.END)
        entry_hours.delete(0, tk.END)
        entry_days.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Invalid input")


# Function to calculate bill
import matplotlib
matplotlib.use('TkAgg')  # IMPORTANT FIX
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

def calculate():
    rate = entry_rate.get()

    if not rate:
        messagebox.showerror("Error", "Enter electricity rate")
        return

    try:
        rate = float(rate)
        total_units = 0

        names = []
        units_list = []
        cost_list = []

        # 🔢 Calculate units & cost
        for app in appliances:
            name, power, hours, days = app
            units = (power * hours * days) / 1000
            cost = units * rate

            names.append(name)
            units_list.append(units)
            cost_list.append(cost)

            total_units += units

        total_cost = total_units * rate

        # 📝 Result text
        result_text = f"Total Units: {total_units:.2f} kWh\nTotal Cost: ₹{total_cost:.2f}\n\n"

        # 💰 Cost per appliance
        result_text += "Cost Breakdown:\n"
        for i in range(len(names)):
            result_text += f"{names[i]} → ₹{cost_list[i]:.2f}\n"

        result_text += "\n"

        # 💡 Smart suggestions
        if units_list:
            max_units = max(units_list)
            max_index = units_list.index(max_units)
            max_appliance = names[max_index]

            percent = (max_units / total_units) * 100

            result_text += f"⚠️ Highest Usage: {max_appliance} ({percent:.1f}%)\n"

            if percent > 50:
                result_text += f"💡 Tip: Reduce usage of {max_appliance}\n"

        result_label.config(text=result_text)

        # 🧹 Clear old graphs
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # 📊 Embed graphs
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 2, figsize=(8, 4))

        # BAR GRAPH
        ax[0].bar(names, units_list)
        ax[0].set_title("Usage")
        ax[0].set_xlabel("Appliances")
        ax[0].set_ylabel("Units")

        # PIE CHART
        ax[1].pie(units_list, labels=names, autopct='%1.1f%%')
        ax[1].set_title("Distribution")

        # Show inside Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except:
        messagebox.showerror("Error", "Invalid input")

# GUI Setup
root = tk.Tk()
root.title("⚡ Smart Electricity Calculator")
root.geometry("550x650")
root.configure(bg="#f5f5f5")

title = tk.Label(root, text="Electricity Cost Calculator", font=("Arial", 18, "bold"), bg="#f5f5f5")
title.pack(pady=10)

frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=10)

# Inputs
tk.Label(frame, text="Appliance Name", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Power (W or HP)", bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5)
entry_power = tk.Entry(frame)
entry_power.grid(row=1, column=1)

var_type = tk.StringVar(value="W")
tk.Radiobutton(frame, text="Watts", variable=var_type, value="W", bg="#f5f5f5").grid(row=2, column=0)
tk.Radiobutton(frame, text="HP", variable=var_type, value="HP", bg="#f5f5f5").grid(row=2, column=1)

tk.Label(frame, text="Hours/day", bg="#f5f5f5").grid(row=3, column=0, padx=5, pady=5)
entry_hours = tk.Entry(frame)
entry_hours.grid(row=3, column=1)

tk.Label(frame, text="Days/month", bg="#f5f5f5").grid(row=4, column=0, padx=5, pady=5)
entry_days = tk.Entry(frame)
entry_days.grid(row=4, column=1)

tk.Button(root, text="Add Appliance", bg="#4CAF50", fg="white", width=20, command=add_appliance).pack(pady=10)

listbox = tk.Listbox(root, width=50, height=8)
listbox.pack(pady=10)

tk.Label(root, text="Rate (₹ per unit)", bg="#f5f5f5").pack()
entry_rate = tk.Entry(root)
entry_rate.pack()

tk.Button(root, text="Calculate Bill", bg="#2196F3", fg="white", width=20, command=calculate).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 11), bg="#f5f5f5", justify="left")
result_label.pack(pady=15)
graph_frame = tk.Frame(root, bg="#f5f5f5")
graph_frame.pack(pady=10)

root.mainloop()
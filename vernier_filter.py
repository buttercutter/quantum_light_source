import numpy as np
import matplotlib.pyplot as plt
import lumapi

# Connect to FDTD
fdtd = lumapi.FDTD()

# Create first ring structure
fdtd.addring()
fdtd.set("name", "ring1")
fdtd.set("x", 0)
fdtd.set("y", 0)
fdtd.set("inner radius", 0.5e-6)
fdtd.set("outer radius", 1.0e-6)
fdtd.set("z span", 0.22e-6)
fdtd.set("material", "Si (Silicon) - Palik")

# Create second ring structure
fdtd.addring()
fdtd.set("name", "ring2")
fdtd.set("x", 1.5e-6)  # Offset in x direction
fdtd.set("y", 0)
fdtd.set("inner radius", 0.6e-6)  # Different size
fdtd.set("outer radius", 1.1e-6)  # Different size
fdtd.set("z span", 0.22e-6)
fdtd.set("material", "Si (Silicon) - Palik")

# Set up FDTD region
fdtd.addfdtd()
fdtd.set("dimension", "2D")
fdtd.set("x", 0)
fdtd.set("y", 0)
fdtd.set("x span", 2.0e-6)
fdtd.set("y span", 2.0e-6)
fdtd.set("mesh type", "auto")

# Add a source
fdtd.addmode()
fdtd.set("name", "source")
fdtd.set("x", -0.5e-6)
fdtd.set("y", 0)
fdtd.set("y span", 0.3e-6)

freq_center = 250e12   # 250 THz
freq_span = 100e12     # 100 THz
fdtd.set("center frequency", freq_center)
fdtd.set("frequency span", freq_span)

# Add a monitor
fdtd.addpower()
fdtd.set("name", "monitor")
fdtd.set("x", 0.5e-6)
fdtd.set("y", 0)
fdtd.set("x span", 0.5e-6)  # Change 'y span' to 'x span'
fdtd.set("override global monitor settings", 1)
fdtd.set("use wavelength spacing", 1)
#fdtd.set("number of points", 1000)

# Run the simulation
fdtd.run()

# Get the field profile
x = fdtd.getdata("monitor", "x")
y = fdtd.getdata("monitor", "y")
z = fdtd.getdata("monitor", "z")
E = fdtd.getdata("monitor", "E")

# Plot the field profile
plt.pcolormesh(x, y, np.abs(E))
plt.show()

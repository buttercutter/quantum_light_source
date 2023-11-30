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

# Add a field profile monitor
fdtd.addprofile()
fdtd.set("name", "E_monitor")
fdtd.set("x", 0.5e-6)
fdtd.set("y", 0)
fdtd.set("x span", 0.5e-6)  # Change 'y span' to 'x span'
fdtd.set("override global monitor settings", 1)
fdtd.set("use wavelength spacing", 1)

# Run the simulation
fdtd.run()

# Get the field profile
#print(fdtd.getdata("E_monitor"))
x = fdtd.getdata("E_monitor", "x")
y = fdtd.getdata("E_monitor", "y")
z = fdtd.getdata("E_monitor", "z")
Ex = fdtd.getdata("E_monitor", "Ex")
Ey = fdtd.getdata("E_monitor", "Ey")
Ez = fdtd.getdata("E_monitor", "Ez")

print(f"x.shape = {x.shape}")
print(f"y.shape = {y.shape}")

# Get the frequency data
f = fdtd.getdata("E_monitor", "f")

# Find the index of the center frequency
idx = np.abs(f - freq_center).argmin()

# Select the electric field components at the center frequency and the specific z-index
Ex0 = Ex[:, :, 0, idx]
Ey0 = Ey[:, :, 0, idx]

print(f"Ex.shape = {Ex.shape}")
print(f"Ex0.shape = {Ex0.shape}")

# Compute the magnitude of the electric field
E = np.sqrt(np.abs(Ex0)**2 + np.abs(Ey0)**2)

# The x, y, and E arrays should be 2D arrays with shapes (19, 73) for plotting
x, y = np.meshgrid(x.ravel(), y.ravel())
E = E.reshape(x.shape)

# Check the shapes
print(f"x.shape = {x.shape}")  # Should print (19, 73)
print(f"y.shape = {y.shape}")  # Should print (19, 73)
print(f"E.shape = {E.shape}")  # Should print (19, 73)

# Plot the field profile
plt.pcolormesh(x, y, E, shading='auto')
plt.colorbar(label="Electric field (a.u.)")
plt.xlabel("x position (m)")
plt.ylabel("y position (m)")
plt.show()

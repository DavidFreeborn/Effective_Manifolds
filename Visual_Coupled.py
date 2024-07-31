import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from matplotlib import rcParams

rcParams['toolbar'] = 'None'

def coupled_pendulum_x1(t, d, omega1, omega2):
    return d * np.cos((omega2 - omega1) / 2 * t) * np.cos((omega1 + omega2) / 2 * t)

def coupled_pendulum_x2(t, d, omega1, omega2):
    return d * np.sin((omega2 - omega1) / 2 * t) * np.sin((omega1 + omega2) / 2 * t)

def simplified_pendulum(t, d, omega_h):
    return d * np.cos(omega_h * t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
plt.subplots_adjust(left=0.05, bottom=0.3, right=0.95, top=0.9, wspace=0.3)

ax1.set_xlim(-2, 2)
ax1.set_ylim(-4, 1)
ax1.set_aspect('equal')
ax1.axis('off')

ax2.set_xlim(0, 10)
ax2.set_ylim(-1, 1)
ax2.axis('off')

line1, = ax1.plot([], [], 'o-', color='blue', lw=4, markersize=10)
line2, = ax1.plot([], [], 'o-', color='orange', lw=4, markersize=10)
line3, = ax1.plot([], [], 'o-', color='orange', lw=4, markersize=10)
connector, = ax1.plot([], [], 'orange', lw=2)
line4, = ax2.plot([], [], lw=2, label='Coupled Pendulum')
line5, = ax2.plot([], [], lw=2, label='Simplified Pendulum')
fig.legend(['Simplified Pendulum', 'Coupled Pendulum'], loc='upper right', fontsize=16, frameon=False)

omega_values_ax = plt.axes([0.05, 0.05, 0.9, 0.05], facecolor='w')
omega_values_ax.axis('off')
omega_h_text = omega_values_ax.text(0.25, 0.5, '', transform=omega_values_ax.transAxes, fontsize=12, ha='center')
omega_l_text = omega_values_ax.text(0.75, 0.5, '', transform=omega_values_ax.transAxes, fontsize=12, ha='center')

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    connector.set_data([], [])
    line4.set_data([], [])
    line5.set_data([], [])
    return line1, line2, line3, connector, line4, line5

def update(frame, t, omega1, omega2, omega_h):
    y1 = simplified_pendulum(t[:frame+1], 0.5, omega_h)
    x1 = coupled_pendulum_x1(t[:frame+1], 1, omega1, omega2)
    x2 = coupled_pendulum_x2(t[:frame+1], 1, omega1, omega2)
    
    if y1.size > 0:
        line1.set_data([0, 2 * np.sin(y1[-1])], [0, -2 * np.cos(y1[-1])])
    if x1.size > 0 and x2.size > 0:
        sin_x2, cos_x2 = np.sin(x2[-1]), np.cos(x2[-1])
        sin_x1 = np.sin(x1[-1])
        line2.set_data([0, sin_x2], [0, -cos_x2])
        line3.set_data([sin_x2, sin_x1], [-cos_x2, -2 * cos_x2])
        connector.set_data([sin_x2, sin_x1], [-cos_x2, -2 * cos_x2])
    
    line4.set_data(t[:frame+1], x1 / 2)
    line5.set_data(t[:frame+1], y1)
    return line1, line2, line3, connector, line4, line5

def update_plot(val=None):
    global ani
    omega1 = omega1_slider.val
    omega2 = omega2_slider.val
    omega_h = (omega1 + omega2) / 2
    t = np.linspace(0, 10, 1000)

    omega_h_text.set_text(f'ωₕ = {omega_h:.2f}')
    omega_l_text.set_text(f'ωₗ = {(omega2 - omega1) / 2:.2f}')

    if 'ani' in globals():
        ani.event_source.stop()

    ani = FuncAnimation(fig, update, frames=len(t), fargs=(t, omega1, omega2, omega_h), init_func=init, blit=True, interval=20/speed_slider.val)
    plt.draw()

def restart(event):
    update_plot()

axcolor = 'lightgoldenrodyellow'
ax_omega1 = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_omega2 = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_speed = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_button = plt.axes([0.8, 0.1, 0.1, 0.04])

omega1_slider = Slider(ax_omega1, 'ω₁', 0.1, 10, valinit=2 * np.pi * 1, valstep=0.1)
omega2_slider = Slider(ax_omega2, 'ω₂', 0.1, 10, valinit=2 * np.pi * 1.5, valstep=0.1)
speed_slider = Slider(ax_speed, 'Speed', 0.1, 5, valinit=1, valstep=0.1)
button = Button(ax_button, 'Restart', color=axcolor, hovercolor='0.975')

omega1_slider.on_changed(update_plot)
omega2_slider.on_changed(update_plot)
speed_slider.on_changed(update_plot)
button.on_clicked(restart)

t = np.linspace(0, 10, 1000)
omega_h = (omega1_slider.val + omega2_slider.val) / 2
omega_l = (omega2_slider.val - omega1_slider.val) / 2
update_plot()
ani = FuncAnimation(fig, update, frames=len(t), fargs=(t, omega1_slider.val, omega2_slider.val, omega_h), init_func=init, blit=True, interval=20/speed_slider.val)

plt.show()

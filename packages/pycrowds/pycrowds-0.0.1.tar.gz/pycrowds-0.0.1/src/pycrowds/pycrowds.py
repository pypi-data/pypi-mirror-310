# DEPENDENCIES and DEFAULTS
import math
import numpy as np
import numpy.random
import scipy.signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def duhamel_integral(T: np.ndarray, F: np.ndarray, xi: float, wn: float, m: float) -> np.ndarray:
    """
    Compute the displacement response U using the Duhamel integral.

    Parameters:
    ----------
    T : np.ndarray
        1D array of time points.
    F : np.ndarray
        1D array of force values corresponding to each time point.
    xi : float
        Damping ratio.
    wn : float
        Natural frequency (rad/s).
    m : float
        Mass.

    Returns:
    -------
    U : np.ndarray
        1D array of displacement responses at each time point.
    """

    wd = wn * math.sqrt(1 - xi ** 2)  # (rads/s) Damped angular modal frequency
    if len(T) < 2:
        raise ValueError("Time vector T must contain at least two elements to compute delT.")

    # Initialize displacement array
    U = np.zeros_like(T)

    # Calculate time step assuming uniform spacing
    delta_t = T[1] - T[0]

    # Precompute constant coefficient
    coef = 1 / (m * wd)

    # Initialize cumulative sums for A and B
    A_cumulative = 0.0
    B_cumulative = 0.0

    # Loop through each time step starting from the second point
    for i in range(1, len(T)):
        exp_term_current = np.exp(xi * wn * T[i])
        exp_term_prev = np.exp(xi * wn * T[i - 1])

        y_current = exp_term_current * F[i]
        y_prev = exp_term_prev * F[i - 1]

        # Trapezoidal integration for A and B
        A_cumulative += 0.5 * delta_t * (y_current * np.cos(wd * T[i]) + y_prev * np.cos(wd * T[i - 1]))
        B_cumulative += 0.5 * delta_t * (y_current * np.sin(wd * T[i]) + y_prev * np.sin(wd * T[i - 1]))

        # Compute A_i and B_i
        A_i = coef * A_cumulative
        B_i = coef * B_cumulative

        # Compute the exponential decay term
        ep = np.exp(-xi * wn * T[i])

        # Calculate displacement response at current time step
        U[i] = A_i * ep * np.sin(wd * T[i]) - B_i * ep * np.cos(wd * T[i])

    # Calculate accelerations from displacement
    A = np.gradient(np.gradient(U, delta_t), delta_t)

    return U, A


def find_peaks(array: np.ndarray, time: np.ndarray):
    """
    Identify peak values in a data array and their corresponding times using SciPy's find_peaks.

    A peak is defined as a point where the slope changes from positive to negative.

    Parameters:
    ----------
    array : np.ndarray
        1D array of data points where peaks are to be identified.
    time : np.ndarray
        1D array of time points corresponding to each data point in `array`.

    Returns:
    -------
    peaks : np.ndarray
        1D array containing the peak values.
    peak_times : np.ndarray
        1D array containing the times at which each peak occurs.

    Raises:
    ------
    ValueError
        If `array` and `time` do not have the same length.
    """

    if array.shape != time.shape:
        raise ValueError("The 'array' and 'time' inputs must have the same shape.")

    # Use SciPy's find_peaks to identify peak indices
    peak_indices, _ = scipy.signal.find_peaks(array)

    # Extract peak values and their corresponding times
    peaks = array[peak_indices]
    peak_times = time[peak_indices]

    return peaks, peak_times


def simulate(L, M, N, mp, fn, xi, window, V_avg=1.3, delta_t=0.005, buffer=10):
    # buffer (s) Additional seconds to allow simulation of response beyond window length (late finishers)
    wn = 2 * math.pi * fn  # (rads/s) Angular modal frequency
    m = 0.5 * M * L  # (kg) Modal mass of mode 1
    # Random variables
    t_start = np.random.uniform(low=2.0, high=window, size=N)  # Uniformly distributed start times
    Vp = np.random.normal(loc=V_avg, scale=0.125, size=N)  # Normally distributed walking velocities
    G = 9.81 * mp  # (N) Static weight of pedestrian

    # Set up the simulation time vector
    t_max = window + buffer  # (s) Max time
    time = np.arange(0, t_max + delta_t, delta_t)

    # Initialise containers to hold the individual forces and responses calculated for each pedestrian
    crowd_force = np.zeros([N, len(time)])
    crowd_displacements = np.zeros([N, len(time)])
    crowd_accelerations = np.zeros([N, len(time)])

    # For each pedestrian...
    for i, n in enumerate(np.arange(N)):
        vp = Vp[i]  # (m/s) Walking velocity
        start_time = t_start[i]  # (s) Start time
        tCross = L / vp  # (s) Crossing time

        fv = 0.35 * vp ** 3 - 1.59 * vp ** 2 + 2.93 * vp  # (Hz) Pacing frequency
        DLF = 0.41 * (fv - 0.95)  # Dynamic load factor

        time_vector = np.arange(0, tCross + delta_t, delta_t)  # Time vector for this pedestrian
        Fv = G + abs(
            G * DLF * np.sin(2 * math.pi * (fv / 2) * time_vector))  # Static + Dynamic GRF (ignore static component)

        xp = vp * time_vector  # Position as a function of time
        phi = np.sin(math.pi * xp / L)  # Mode shape at pedestrian's location
        Fn = Fv * phi  # Modal force experienced by SDoF system

        displacements, accelerations = duhamel_integral(time_vector, Fn, xi=xi, wn=wn,
                                                        m=m )  # Response calculated using the Duhamel integral function

        # Save the GRF and response for this pedestrian at the correct position in the overal simulation records
        iStart = round(start_time / delta_t)  # Index for start time
        crowd_force[i, iStart:iStart + len(Fn)] = Fn
        crowd_displacements[i, iStart:iStart + len(Fn)] = displacements
        crowd_accelerations[i, iStart:iStart + len(Fn)] = accelerations

    return time, crowd_force, crowd_displacements, crowd_accelerations


def plot_crowd_results(time: np.ndarray, total_force: np.ndarray,
                       total_displacement: np.ndarray, total_acceleration: np.ndarray) -> go.Figure:
    """
    Generate an interactive Plotly figure with three subplots:
    1. Force vs Time
    2. Displacement vs Time with Peak Markers
    3. Acceleration vs Time

    Parameters:
    ----------
    time : np.ndarray
        1D array of time points.
    total_force : np.ndarray
        1D array of total force values corresponding to each time point.
    total_displacement : np.ndarray
        1D array of total displacement values corresponding to each time point.
    total_acceleration : np.ndarray
        1D array of total acceleration values corresponding to each time point.
    find_peaks_func : callable
        Function to identify peaks in the displacement data. Should return peaks and their corresponding times.

    Returns:
    -------
    fig : plotly.graph_objects.Figure
        Interactive Plotly figure containing the three subplots.
    """
    # Create a subplot figure with 3 rows and 1 column
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(
            "Force vs Time",
            "Displacement vs Time with Peaks",
            "Acceleration vs Time"
        )
    )

    # First Subplot: Force vs Time
    fig.add_trace(
        go.Scatter(
            x=time,
            y=total_force,
            mode='lines',
            name='Total Force',
            line=dict(color='blue')
        ),
        row=1, col=1
    )

    # Identify peaks in displacement
    peaks, peak_times = find_peaks(total_displacement, time)

    # Second Subplot: Displacement vs Time
    fig.add_trace(
        go.Scatter(
            x=time,
            y=-1000 * total_displacement,  # Convert to mm and invert
            mode='lines',
            name='Total Displacement',
            line=dict(color='green')
        ),
        row=2, col=1
    )

    # Add peak markers to the Displacement subplot
    fig.add_trace(
        go.Scatter(
            x=peak_times,
            y=-1000 * peaks,  # Convert to mm and invert
            mode='markers',
            name='Peaks',
            marker=dict(color='red', size=8, symbol='circle'),
            hovertemplate='Time: %{x:.2f}s<br>Displacement: %{y:.2f} mm'
        ),
        row=2, col=1
    )

    # Third Subplot: Acceleration vs Time
    fig.add_trace(
        go.Scatter(
            x=time,
            y=total_acceleration,
            mode='lines',
            name='Total Acceleration',
            line=dict(color='orange')
        ),
        row=3, col=1
    )

    # Update Y-Axis Titles
    fig.update_yaxes(title_text="Force (N)", row=1, col=1)
    fig.update_yaxes(title_text="Displacement (mm)", row=2, col=1)
    fig.update_yaxes(title_text="Acceleration (m/s²)", row=3, col=1)

    # Update X-Axis Title for the Bottom Plot
    fig.update_xaxes(title_text="Time (s)", row=3, col=1)

    # Update Layout for better aesthetics
    fig.update_layout(
        height=900,  # Adjust the height as needed
        width=1000,  # Adjust the width as needed
        title_text="Crowd Simulation Results",
        showlegend=False,
        template="plotly_white"
    )

    # Add Gridlines and Customize Hover Behavior
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig


if __name__=="__main__":
    numpy.random.seed(1)  # repeatable
    L = 20  # (m) Bridge span
    M = 150  # (kg/m) Mass per unit length]
    N = 50  # Number of pedestrians that cross the bridge in the time window
    mp = 80  # (kg) Pedestrian mass
    xi = 0.025  # Damping ratio
    fn = 2.5  # (Hz) Bridge modal frequency

    V_avg = 1.3  # (m/s) average walking speed
    window = 30
    buffer = int(1.5*L/V_avg)

    time, crowd_forces, crowd_displacements, crowd_accelerations = simulate(L, M, N, mp, fn, xi, window=window, V_avg=V_avg, buffer=buffer)

    # Sum across rows of crowdForce and crowdResponse
    total_force = sum(crowd_forces)
    total_displacement = sum(crowd_displacements)
    total_acceleration = sum(crowd_accelerations)

    fig = plot_crowd_results(time, total_force, total_displacement, total_acceleration)
    fig.show()


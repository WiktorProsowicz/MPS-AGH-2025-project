import numpy as np
import logging
import matplotlib.pyplot as plt
from PyMPDATA import Options, ScalarField, VectorField, Stepper, Solver
from PyMPDATA.boundary_conditions import Constant

# ─── Main driver ───────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# domain
xmin, xmax, nx = -5.0, 5.0, 64
dx = (xmax - xmin) / nx
x = np.linspace(xmin + dx / 2, xmax - dx / 2, nx)

# time
dt = 1e-3
t_final = 100.0
n_steps = int(t_final / dt)

# heterogeneous diffusivity D(x)
D_field = 1.01 + np.tanh(x)

# initial condition - uniform field (to match py-pde reference exactly)
c0 = np.ones(nx)  # Uniform concentration everywhere

# ── build a Solver with native heterogeneous diffusion ───────────────────────────
opts = Options(
    n_iters=10,  # more MPDATA iterations → sharper features
    non_zero_mu_coeff=True,
    heterogeneous_diffusion=True,  # Enable native heterogeneous diffusion
)

# Set up fields with proper boundary conditions
advectee = ScalarField(data=c0, halo=opts.n_halo, boundary_conditions=(Constant(0.0),))
advector = VectorField(
    data=(np.zeros(nx + 1),), halo=opts.n_halo, boundary_conditions=(Constant(0.0),)
)
diffusivity_field = ScalarField(
    data=D_field, halo=opts.n_halo, boundary_conditions=(Constant(0.0),)
)

stepper = Stepper(options=opts, grid=(nx,))
solver = Solver(
    stepper=stepper,
    advectee=advectee,
    advector=advector,
    diffusivity_field=diffusivity_field,
)

# ── march & record for kymograph ──────────────────────────────────────────────
logging.info("Starting heterogeneous diffusion simulation...")
logging.info(
    f"Using native PyMPDATA implementation (should be ~3x faster than Strang splitting)"
)

kymo = np.empty((n_steps + 1, nx))
kymo[0] = solver.advectee.get()

# Use stronger mu_coeff for more realistic long-time evolution
mu_coeff = 0.05  # Increased to get more decay over time

logging.info(f"Diffusivity range: {D_field.min():.3f} to {D_field.max():.3f}")
logging.info(f"Using balanced mu coefficient: {mu_coeff:.6f}")

for i in range(1, n_steps + 1):
    if i % 10000 == 0:
        logging.info(f"At step {i}/{n_steps}")

    # Single call per timestep (vs 3 calls in Strang splitting!)
    solver.advance(n_steps=1, mu_coeff=(mu_coeff,))
    kymo[i] = solver.advectee.get()

logging.info("Simulation completed!")

# ── plot ───────────────────────────────────────────────────────────────────────
T = np.linspace(0, t_final, n_steps + 1)
X, Tgrid = np.meshgrid(x, T)

plt.figure(figsize=(10, 6))

# Main kymograph
plt.subplot(2, 2, (1, 3))
plt.pcolormesh(X, Tgrid, kymo, shading="auto")
plt.colorbar(label="c(x,t)")
plt.xlabel("x")
plt.ylabel("Time")
plt.title("Native PyMPDATA Heterogeneous Diffusion")

# Diffusivity profile
plt.subplot(2, 2, 2)
plt.plot(x, D_field, "b-", linewidth=2)
plt.xlabel("x")
plt.ylabel("D(x)")
plt.title("Heterogeneous Diffusivity")
plt.grid(True, alpha=0.3)

# Final solution
plt.subplot(2, 2, 4)
plt.plot(x, kymo[0], "k--", alpha=0.7, label="t=0")
plt.plot(x, kymo[-1], "r-", label=f"t={t_final}")
plt.xlabel("x")
plt.ylabel("c(x)")
plt.title("Initial vs Final")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ── Summary statistics ─────────────────────────────────────────────────────────
logging.info(
    f"Mass conservation: initial={kymo[0].sum():.6f}, final={kymo[-1].sum():.6f}"
)
logging.info(
    f"Relative mass change: {abs(kymo[-1].sum() - kymo[0].sum()) / kymo[0].sum() * 100:.2e}%"
)

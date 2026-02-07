import requests
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000"
SOLVE_URL = f"{BASE_URL}/solve/"
# Replace with your actual list of 50 problems
PROBLEMS = [
    # Domain 1: Calculus & Differential Equations
    "Evaluate the indefinite integral: \int 1/(x^2 + 4x + 13) dx.",
    "Solve the second-order linear ODE: y'' + 6y' + 9y = 0 with y(0)=2, y'(0)=1.",
    "Compute the derivative of f(x) = ln(sin(x^2)).",
    "Find the Taylor series expansion of e^x * cos(x) up to the x^4 term centered at x=0.",
    "Evaluate the double integral: \int_0^1 \int_0^x (x+y) dy dx.",
    "Solve the Bernoulli differential equation: y' + y/x = y^2 * ln(x).",
    "Find the area of the region bounded by y = x^2 and y = sqrt(x).",
    "Compute the arc length of the curve y = (2/3)x^(3/2) from x=0 to x=3.",
    "Solve the initial value problem: dy/dt = ky(M-y) with y(0)=y0.",
    "Determine the convergence of the series: \sum_{n=1}^{\infty} n^2 / 2^n.",

    # Domain 2: Engineering Mechanics (Statics & Dynamics)
    "A cantilever beam of length L has a point load P at the free end. Derive the deflection y(x).",
    "Calculate the moment of inertia of a solid cylinder of mass M and radius R about its central axis.",
    "Determine the tension in a cable supporting a mass M in a pulley system with friction coefficient mu.",
    "A particle moves with acceleration a(t) = 3t^2 - 2t. Find the velocity v(t) if v(0)=5.",
    "Derive the formula for the maximum shear stress in a circular shaft under torque T.",
    "Find the center of mass of a semi-circular thin plate of radius R.",
    "A block of mass m slides down a plane inclined at theta with friction f = mu * N. Derive the acceleration.",
    "Compute the work done by a force F(x) = ax^2 + b moving a particle from x1 to x2.",
    "Calculate the escape velocity of a planet with mass M and radius R.",
    "Derive the period of a simple pendulum of length L for small angular displacements.",

    # Domain 3: Thermodynamics & Heat Transfer
    "Derive the expression for the work done during an adiabatic expansion: PV^gamma = constant.",
    "Calculate the entropy change delta S for 1 mole of an ideal gas expanding from V1 to V2 isothermally.",
    "Derive the efficiency of a Carnot cycle operating between temperatures TH and TC.",
    "Find the steady-state temperature distribution in a plane wall with thickness L and thermal conductivity k.",
    "Calculate the heat loss per unit length from a pipe of radius r1 with insulation up to r2.",
    "Determine the final temperature when m1 mass of water at T1 is mixed with m2 at T2 in an isolated system.",
    "Derive the ideal gas law PV=nRT from the kinetic theory of gases.",
    "Find the heat required to change 10g of ice at -10C to steam at 110C.",
    "Derive the first law of thermodynamics for an open system (Steady Flow Energy Equation).",
    "Calculate the change in internal energy delta U for a constant volume heating process.",

    # Domain 4: Fluid Mechanics
    "Apply the Bernoulli equation to find the exit velocity of water from a large tank at depth h.",
    "Derive the continuity equation for a 1D steady incompressible flow in a pipe with changing area.",
    "Calculate the Reynolds number for a fluid of density rho and viscosity mu flowing in a pipe of diameter D.",
    "Find the hydrostatic pressure at a depth z in a fluid with varying density rho(z) = rho0 * e^(-az).",
    "Derive the velocity profile for laminar flow in a pipe (Hagen-Poiseuille flow).",
    "Determine the drag force on a sphere of radius r moving at velocity v in a fluid with viscosity eta (Stokes' Law).",
    "Calculate the lift force on an airfoil using the Kutta-Joukowski theorem.",
    "Derive the expression for the capillary rise h in a tube of radius r with surface tension sigma.",
    "Find the torque required to rotate a disk of radius R in a fluid of viscosity mu at height h above a plate.",
    "Apply the momentum equation to find the force exerted by a jet on a stationary flat plate.",

    # Domain 5: Circuits, Controls & Advanced Engineering
    "Find the Laplace transform of f(t) = t^2 * e^(-3t) * sin(4t).",
    "Determine the transfer function H(s) = Vout/Vin for a series RC circuit.",
    "Solve for the current i(t) in a series RL circuit with a step voltage V applied at t=0.",
    "Compute the inverse Laplace transform of F(s) = (s+1)/(s^2 + 4s + 13).",
    "Find the resonant frequency omega0 of a series RLC circuit with R, L, C.",
    "Derive the state-space representation for a mass-spring-damper system.",
    "Calculate the Fourier coefficients for a periodic triangular wave.",
    "Determine the stability of a system with characteristic equation s^3 + 2s^2 + 4s + 8 = 0 using Routh-Hurwitz.",
    "Find the Z-transform of the sequence x[n] = (0.5)^n * u[n].",
    "Solve the wave equation d^2u/dt^2 = c^2 * d^2u/dx^2 for a string fixed at both ends."
]

def run_batch():
    session = requests.Session()
    
    # 1. Get the CSRF token from the index page
    try:
        get_response = session.get(BASE_URL)
        csrf_token = session.cookies.get('csrftoken')
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    print(f"🚀 Starting Batch: 50 Problems | Token: {csrf_token[:10]}...")

    for i, problem in enumerate(PROBLEMS):
        print(f"[{i+1}/50] Solving: {problem[:40]}...")
        
        # 2. Send the POST request exactly like the UI form
        payload = {
            "query": problem,
            "csrfmiddlewaretoken": csrf_token
        }
        
        headers = {
            "Referer": BASE_URL,
            "X-CSRFToken": csrf_token
        }

        try:
            start_time = time.time()
            response = session.post(SOLVE_URL, data=payload, headers=headers)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✅ Success ({duration:.2f}s)")
            else:
                print(f"❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Request Error: {e}")

        # 3. Cooldown to stay within Groq/Gemini RPM limits
        # Recommended: 4 seconds for 15 RPM limits
        time.sleep(4) 

if __name__ == "__main__":
    run_batch()
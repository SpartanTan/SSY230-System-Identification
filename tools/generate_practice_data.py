"""Self-designed SI exercises, not official Freiburg data or solved estimators."""
from pathlib import Path
import argparse
import json
import hashlib
import numpy as np
from scipy.io import savemat


def rk4(f, x, u, dt):
    k1 = f(x, u)
    k2 = f(x + dt*k1/2, u)
    k3 = f(x + dt*k2/2, u)
    k4 = f(x + dt*k3, u)
    return x + dt*(k1 + 2*k2 + 2*k3 + k4)/6


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    records = []

    def save(name, arrays, description):
        values = {k: np.asarray(v) for k, v in arrays.items()}
        for k, a in values.items():
            if a.dtype.kind in "fiuc":
                assert np.isfinite(a).all(), (name, k)
        np.savez_compressed(output/(name+".npz"), **values)
        savemat(output/(name+".mat"), values, oned_as="column", do_compression=True)
        # Hash the mathematical arrays; MAT headers contain a creation timestamp.
        digest = hashlib.sha256()
        for k in sorted(values):
            a = np.ascontiguousarray(values[k])
            digest.update(k.encode())
            digest.update(str(a.shape).encode())
            digest.update(a.dtype.str.encode())
            digest.update(a.tobytes())
        records.append({"name": name, "description": description,
                        "array_sha256": digest.hexdigest(),
                        "shapes": {k: list(v.shape) for k, v in values.items()}})

    for split, seed in [("train", 230), ("validation", 231), ("test", 232)]:
        rng = np.random.default_rng(seed)
        n = 180
        current = rng.uniform(-2, 2, n)
        sigma = .04 + .06*np.abs(current)
        voltage = 2.4*current + .7 + rng.normal(size=n)*sigma
        save("resistance_"+split, {"u": current[:, None], "y": voltage[:, None],
             "noise_std": sigma, "truth_theta": [2.4, .7], "seed": seed},
             {"columns": {"u": ["current_A"], "y": ["voltage_V"],
                          "truth_theta": ["resistance_ohm", "offset_V"]},
              "kind": "synthetic heteroscedastic static regression"})

        n = 800
        u = rng.choice([-1., 1.], n)
        a = np.r_[np.full(n//2, .65), np.full(n-n//2, .35)]
        b = np.r_[np.full(n//2, .4), np.full(n-n//2, .7)]
        y = np.zeros(n)
        for k in range(1, n):
            y[k] = a[k]*y[k-1] + b[k]*u[k-1] + .15*rng.normal()
        save("rls_"+split, {"u": u[:, None], "y": y[:, None],
             "truth_theta": np.column_stack([a, b]), "Ts": 1., "seed": seed},
             {"time_unit": "normalized samples, not physical seconds",
              "equation": "y[k]=a[k]*y[k-1]+b[k]*u[k-1]+e[k], std(e)=0.15"})

        for degenerate in ([False, True] if split == "train" else [False]):
            dt, n = .02, 1200
            t = np.arange(n)*dt
            phase = .7*(seed-230)
            u = np.column_stack([8+2*np.sin(.7*t+phase)+np.sin(1.6*t),
                                 8+2*np.cos(.5*t+phase)+np.sin(1.3*t)])
            if degenerate:
                u[:] = 6.
            theta = np.array([.158, .162, .54])  # RL, RR, full track
            def f(x, w):
                v = (theta[1]*w[1]+theta[0]*w[0])/2
                yaw = (theta[1]*w[1]-theta[0]*w[0])/theta[2]
                return np.array([v*np.cos(x[2]), v*np.sin(x[2]), yaw])
            x = np.zeros((n, 3))
            for k in range(n-1):
                x[k+1] = rk4(f, x[k], u[k], dt)
            noise_std = np.sqrt([1.6e-3, 4e-4])
            y = x[:, :2]+rng.normal(size=(n, 2))*noise_std
            name = "differential_drive_"+("degenerate" if degenerate else split)
            save(name, {"t": t, "u": u, "y": y, "truth_x": x,
                 "truth_theta": theta, "noise_std": noise_std,
                 "x0": x[0], "Ts": dt, "seed": seed},
                 {"u": ["omega_left_rad_s", "omega_right_rad_s"],
                  "y": ["px_m", "py_m"], "x": ["px_m", "py_m", "yaw_rad"],
                  "theta": ["R_left_m", "R_right_m", "full_track_m"],
                  "integration": "RK4, piecewise constant wheel speeds",
                  "kind": "synthetic Sheet-8-inspired replacement"})

        dt, n = .1, 600
        t = np.arange(n)*dt
        A = np.array([[1, dt], [0, 1.]])
        g = np.array([dt*dt/2, dt])
        C = np.array([[1., 0]])
        q, R = .08, .04
        u = (.3*np.sin(.4*t)+.2*np.cos(.9*t))[:, None]
        x = np.zeros((n, 2))
        for k in range(n-1):
            x[k+1] = A@x[k]+g*(u[k, 0]+np.sqrt(q)*rng.normal())
        y = x[:, [0]]+np.sqrt(R)*rng.normal(size=(n, 1))
        save("two_state_kf_"+split, {"t": t, "u": u, "y": y,
             "truth_x": x, "A": A, "B": g[:, None], "g": g,
             "C": C, "R": R, "truth_q": q, "x0": x[0],
             "Ts": dt, "seed": seed},
             {"x": ["position_m", "velocity_m_s"], "u": ["acceleration_m_s2"],
              "y": ["position_m"], "noise": "per-step acceleration variance q, Q=q*g*g.T",
              "kind": "self-designed 2-state KF, not official Sheet 9"})

        dt, n = .05, 1200
        t = np.arange(n)*dt
        m, radius, half_track, inertia, wheel_inertia = 220., .16, .32, 9.6, .1
        c1 = 1/(m+2*wheel_inertia/radius**2)
        c2 = half_track/(inertia+2*half_track**2*wheel_inertia/radius**2)
        phase = .5*(seed-230)
        common = .3*np.sin(.2*t+phase)+.15*np.sin(.8*t)
        difference = .08*np.cos(.3*t+phase)
        u = np.column_stack([(common-difference)/2, (common+difference)/2])
        x = np.zeros((n, 5))
        x[0, 3] = 1.
        process_std = np.array([0., 0., 0., .015, .008])
        for k in range(n-1):
            px, py, psi, v, w = x[k]
            tl, tr = u[k]
            dx = np.array([v*np.cos(psi), v*np.sin(psi), w,
                           c1*(tl+tr)/radius, c2*(tr-tl)/radius])
            x[k+1] = x[k]+dt*dx+rng.normal(size=5)*process_std
        clean = np.column_stack([x[:, :2],
             (x[:, 3]-half_track*x[:, 4])/radius,
             (x[:, 3]+half_track*x[:, 4])/radius])
        obs_std = np.sqrt([10., 10., 1e-6, 1e-6])
        y = clean+rng.normal(size=(n, 4))*obs_std
        save("torque_robot_"+split, {"t": t, "u": u, "y": y,
             "truth_x": x, "x0": x[0], "Ts": dt,
             "physical_parameters": [m, radius, half_track, inertia, wheel_inertia],
             "process_std_per_step": process_std, "noise_std": obs_std, "seed": seed},
             {"u": ["torque_left_Nm", "torque_right_Nm"],
              "y": ["px_m", "py_m", "omega_left_rad_s", "omega_right_rad_s"],
              "x": ["px_m", "py_m", "yaw_rad", "speed_m_s", "yaw_rate_rad_s"],
              "parameters": ["m_kg", "R_m", "half_track_m", "I_kg_m2", "Iw_kg_m2"],
              "integration": "Euler, discrete additive state noise after each step",
              "kind": "synthetic Sheet-10-inspired replacement"})

    manifest = {"origin": "self-designed synthetic learning data, 2026-11-10",
                "truth_policy": "truth fields for evaluation, not parameter fitting",
                "datasets": records}
    (output/"dataset_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"datasets": len(records), "output": str(output)}, ensure_ascii=False))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1]/"practice_data")
    build(parser.parse_args().output)

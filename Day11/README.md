# Day 11 — Marine Dynamics Theory

**Phase 3 · Marine Dynamics + MuJoCo Fluid · ~2.5 hours**

## 🎯 Goal
Understand the forces that make underwater motion different from motion in air: **added mass**, **hydrodynamic damping**, and **buoyancy/restoring forces** — the Fossen 6-DOF picture.

---

## Why Underwater Is Different

On land, a robot stops when you cut the motor. Underwater, the water itself is a major player. Four effects dominate:

### 1. Buoyancy & restoring forces
Water pushes up with a force equal to the weight of water displaced (Archimedes). If buoyancy = weight, the vehicle is **neutrally buoyant** (hovers). Where the buoyancy acts vs. where gravity acts creates **restoring torques** that self-right the vehicle (like a weeble). You'll model this on Day 13.

### 2. Added mass
To move, the vehicle must shove surrounding water out of the way — so it behaves as if it's **heavier than it is**. This "added mass" is large underwater and is why a vehicle feels sluggish to accelerate.

### 3. Hydrodynamic damping (drag)
Water resists motion strongly — roughly proportional to velocity and velocity² . This is why an underwater vehicle **glides to a stop** smoothly rather than coasting forever.

### 4. The combined picture (Fossen)
Marine engineering bundles all of this into the **Fossen 6-DOF model** — equations of motion that include added mass, damping, restoring forces, and thruster inputs across surge/sway/heave/roll/pitch/yaw (your Day-2 vocabulary).

---

## The Intuition to Lock In

> **Why does a vehicle keep gliding after you cut thrust?**
> Added mass (it stored momentum in the moving water) + relatively low damping at low speed. It can't stop instantly — the water carries it.

This single intuition explains the *feel* you'll tune for in Phase 4. A good ROV sim has *some* glide (added mass) but settles (damping) — not a brick, not a balloon.

---

## 📝 Today's Task
- Read the relevant chapters of Fossen's *Handbook* (added mass, damping, restoring forces).
- Clone and run a demo from the Python Vehicle Simulator to *see* marine dynamics in action.
- In `notes/`, write the glide explanation in your own words.

---

## ✅ Checkpoint
**You can explain why a vehicle glides after thrust stops** (added mass + low damping).

---

## 📚 Resources
- Fossen — *Handbook of Marine Craft Hydrodynamics and Motion Control*
- [Python Vehicle Simulator](https://github.com/cybergalactic/PythonVehicleSimulator)
- Reference that MuJoCo can model AUVs: *"Learning to Swim"* ([arXiv:2410.00120](https://arxiv.org/abs/2410.00120))

---

## 🔭 Next
**Day 12 — Put fluid forces into MuJoCo: density, viscosity, and the ellipsoid fluid model.**

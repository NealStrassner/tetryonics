/*
 * tetryonics.js — the Tetryonics engine for JavaScript.
 *
 * A faithful mirror of the Python `tetryonics` package: physics from equilateral
 * triangles. Drop this into any web app or Node program and call the engine.
 *
 *   Browser:  <script src="tetryonics.js"></script>   ->   window.Tetryonics
 *   Node:     const T = require('./tetryonics.js')
 *   ES:       import T from './tetryonics.js'           (default export)
 *
 * Software © 2026 Neal Strassner — PolyForm Noncommercial License 1.0.0 (free for
 * noncommercial use; commercial use needs permission). See LICENSE.
 * Geometry & theory © Kelvin Abraham (used with permission). See ATTRIBUTION.md.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Tetryonics = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  const PI = Math.PI, SQRT3 = Math.sqrt(3), PHI = (1 + Math.sqrt(5)) / 2;

  /* ---- constants ---- */
  const H = 6.629432672e-34;
  const H_EV = 4.137664546e-15;              // eV*s (= H/e; Kelvin's "exact value of Planck's constant" paper, title page)
  const C = 299792458;                       // exact SI value (matches Kelvin's m_q digits)
  const C2 = C * C;
  const M_Q = H / C2;                       // 7.376e-51 kg
  const OMEGA = 0.0012;                      // QAM
  const CHARGE_QUANTUM = OMEGA / C2;         // 1.335e-20 C
  const ELEMENTARY_CHARGE = 12 * CHARGE_QUANTUM;
  const EPSILON_0 = 8.85418785e-12, MU_0 = 1.25663706e-6;
  const G = 6.67384e-11, K_B = 1.380649e-23;   // G = Kelvin's Book-4 value
  const FINE_STRUCTURE = 2 * PI * OMEGA;     // Tetryonic alpha ~0.00754
  const N_ELECTRON = 1.2e20, N_PROTON = 2.25e23, N_NEUTRON = 2.25e23;
  const N_HYDROGEN = N_PROTON + N_ELECTRON;
  const PROTON_ELECTRON_RATIO = N_PROTON / N_ELECTRON;
  const H_BAR = H / (2 * PI);
  const BOHR_MAGNETON = ELEMENTARY_CHARGE * H_BAR / (2 * N_ELECTRON * M_Q);
  const NUCLEAR_MAGNETON = BOHR_MAGNETON / PROTON_ELECTRON_RATIO;
  const CHARGE_MASS_RATIO_E = ELEMENTARY_CHARGE / (N_ELECTRON * M_Q);
  const CHARGE_MASS_RATIO_P = ELEMENTARY_CHARGE / (N_PROTON * M_Q);
  const EINSTEIN_KAPPA = 8 * PI * G / (C2 * C2);
  const MAX_Z = 120, PERIODIC_SHELL_CAPS = [2, 8, 18, 32, 32, 18, 8, 2];
  const COSMIC = {dark_energy: 0.68, dark_matter: 0.27, baryonic: 0.05};
  const BARYON_MEV = 930.947, ELECTRON_KEV = 496.519;
  const MEV_J = 1.0e6 * ELEMENTARY_CHARGE;        // 1 MeV in Joules
  const AMU_KG = N_HYDROGEN * M_Q;                // 1 amu (Tetryonic: hydrogen)
  const MEV_PER_AMU = BARYON_MEV + ELECTRON_KEV / 1000.0;   // 931.443519 = Kelvin's printed H rest-energy (proton+electron); element masses then match his Book-3 pages exactly
  // --- constants completed to full parity with the Python `constants` module (exact same derivations) ---
  const EPS_MU = EPSILON_0 * MU_0;                          // = 1/c^2
  const COULOMB_K = 1.0 / (4 * PI * EPSILON_0);             // ~8.9876e9
  const FINE_STRUCTURE_INV = 1.0 / FINE_STRUCTURE;          // ~132.629
  const FINE_STRUCTURE_CODATA = 7.2973525693e-3;            // empirical alpha (comparison)
  const AVOGADRO = 6.022141579e23;                          // 1/mol (Tetryonic)
  const TAU = 2 * PI;
  const AMPERE_CONSTANT = MU_0 / (2 * PI);                  // ~2e-7 N/A^2
  const IMPEDANCE_FREE_SPACE = Math.sqrt(MU_0 / EPSILON_0); // Z0 ~376.73 ohm
  const ELECTRONS_PER_COULOMB = 1.0 / ELEMENTARY_CHARGE;    // ~6.24e18
  const EV_KJ_PER_MOLE = ELEMENTARY_CHARGE * AVOGADRO / 1000.0;
  const LONGITUDINAL_VELOCITY = (PI / 2) * C;               // (pi/2)c longitudinal EM velocity (Book 2 p.96)
  const BOLTZMANN = K_B;                                    // J/K (Python name; same value as K_B)
  const GAS_CONSTANT = 8.314462618;                         // J/(mol K)
  const MERCURY_PRECESSION_ARCSEC_CENTURY = 43.0;
  const PIONEER_ANOMALY = 8.74e-10;                         // m/s^2
  const RYDBERG_DIVISOR = 27.49545417;                      // Book 2 p.128
  const RYDBERG_TETRYONIC = C / 27.49545417;                // his geometric Rydberg ~1.0903e7
  const RYDBERG_OBSERVED = 1.0967758e7;                     // empirical (comparison)
  const E_EULER = Math.E;
  const ZETA2 = PI * PI / 6;                                // Basel sum
  const KEPLER_BOUWKAMP = 0.1149420448;
  const APOLLO_CONSTANT = 873825;                           // light:sound speed ratio (Book 5 p.130)
  const KEM_EV = 13.525;                                    // hydrogen KEM ground (eV)
  const COSMIC_DARK_ENERGY = 0.68, COSMIC_DARK_MATTER = 0.27, COSMIC_BARYONIC = 0.05;
  const constants = {
    H, H_EV, C, C2, M_Q, OMEGA, CHARGE_QUANTUM, ELEMENTARY_CHARGE,
    EPSILON_0, MU_0, EPS_MU, COULOMB_K, G, K_B, BOLTZMANN, GAS_CONSTANT,
    FINE_STRUCTURE, FINE_STRUCTURE_INV, FINE_STRUCTURE_CODATA,
    AVOGADRO, AMPERE_CONSTANT, IMPEDANCE_FREE_SPACE, ELECTRONS_PER_COULOMB, EV_KJ_PER_MOLE, LONGITUDINAL_VELOCITY,
    N_ELECTRON, N_PROTON, N_NEUTRON, N_HYDROGEN, PROTON_ELECTRON_RATIO,
    H_BAR, BOHR_MAGNETON, NUCLEAR_MAGNETON, CHARGE_MASS_RATIO_E, CHARGE_MASS_RATIO_P,
    EINSTEIN_KAPPA, MAX_Z, PERIODIC_SHELL_CAPS,
    BARYON_MEV, ELECTRON_KEV, KEM_EV, MEV_J, AMU_KG, MEV_PER_AMU,
    TAU, PHI, E_EULER, ZETA2, KEPLER_BOUWKAMP, APOLLO_CONSTANT,
    MERCURY_PRECESSION_ARCSEC_CENTURY, PIONEER_ANOMALY,
    RYDBERG_DIVISOR, RYDBERG_TETRYONIC, RYDBERG_OBSERVED,
    COSMIC_DARK_ENERGY, COSMIC_DARK_MATTER, COSMIC_BARYONIC,
    massFromMev: mev => mev * MEV_J / C2, amuFromMev: mev => mev / MEV_PER_AMU, massFromQuanta: n => n * M_Q};

  /* ---- energy / mechanics ---- */
  const energy = {
    energyFromQuanta: N => N * H,
    quantaFromEnergy: E => E / H,
    massFromQuanta: N => N * M_Q,
    emMass: E => E / C2,
    energyFromEmMass: m => m * C2,
    matter: E => E / (C2 * C2),                // M = E/c⁴  (3D Matter)
    matterEnergy: M => M * C2 * C2,            // E = Mc⁴  (forward, his primary identity)
    momentum: (m, v) => m * v,
    scalarEnergy: (m, v) => m * v * v,         // Kelvin's primary form E = m·v²
    kineticEnergy: (m, v) => 0.5 * m * v * v,  // ⚠ classical ½mv², comparison only (his = scalarEnergy)
    bosonEnergy: v => H * v,
    photonEnergy: f => H * f,
    frequencyFromQuanta: v => 2 * v,
    beta: v => v / C,
    gamma: v => 1 / Math.sqrt(1 - (v / C) ** 2),
    timeDilation: (t, v) => t * energy.gamma(v),
    lengthContraction: (L, v) => L / energy.gamma(v),
    deBroglie: p => H / p,
    compton: m => H / (m * C),
    transverseEnergy: (n, v) => n * PI * H * v,
    scalarEnergyQuantised: (n, v) => n * PI * H * v * v,
    tetryonUnits: n => 4 * n * n,
    relativisticEnergy: (p, m) => Math.sqrt((p * C) ** 2 + (m * C2) ** 2),
    qam: () => OMEGA,
    quantaFromMass: m => m / M_Q,
    energyFromMatter: M => M * C2 * C2,
    matterFromEmMass: m => m / C2,
    emMassFromMatter: M => M * C2,
    massFromEnergyVelocity: (E, v) => E / (v * v),
    frequencyFromEnergy: E => E / H,
    bosonQuantaFromEnergy: E => E / H,
    quantaFromFrequency: f => f / 2,
    deBroglieWavelength: p => H / p,
    momentumFromDeBroglie: lam => H / lam,
    comptonWavelength: m => H / (m * C),
    massFromCompton: lam => H / (lam * C),
    velocityFromBeta: b => b * C,
  };

  /* ---- charge ---- */
  const charge = {
    netQuanta: (cw, ccw) => cw - ccw,
    chargeInE: (cw, ccw) => (cw - ccw) / 12,
    chargeCoulombs: (cw, ccw) => (cw - ccw) * CHARGE_QUANTUM,
    chargeFromQam: (qam = OMEGA) => qam / C2,
    timeAsCharge: seconds => seconds * C2 / OMEGA,
    isFermionCharge: (cw, ccw) => (cw - ccw) % 4 === 0,
  };

  /* ---- fields ---- */
  const fields = {
    coulombForce: (q1, q2, r) => (1 / (4 * PI * EPSILON_0)) * q1 * q2 / (r * r),
    electricField: (q, r) => q / (4 * PI * EPSILON_0 * r * r),
    speedOfLight: () => 1 / Math.sqrt(EPSILON_0 * MU_0),
    gaussFlux: q => q / EPSILON_0,
    poynting: (e, h) => e * h,
    fineStructure: (tet = true) => tet ? FINE_STRUCTURE : 7.2973525693e-3,
    electricFalloff: r => 1 / (r * r),
    magneticDipoleFalloff: r => 1 / (r * r * r),
    ampereForcePerLength: (i1, i2, d) => MU_0 * i1 * i2 / (2 * PI * d),
    lorentzForce: (q, E, v, B) => q * (E + v * B),
    coulombConstant: () => 1 / (4 * PI * EPSILON_0),
    bohrMagneton: () => BOHR_MAGNETON,
    nuclearMagneton: () => NUCLEAR_MAGNETON,
    chargeMassRatio: (p = "electron") => p === "electron" ? CHARGE_MASS_RATIO_E : CHARGE_MASS_RATIO_P,
    speedOfLightFromConstants: () => 1 / Math.sqrt(EPSILON_0 * MU_0),
    epsilon0From: (mu0 = MU_0, c = C) => 1 / (mu0 * c * c),
    mu0From: (eps0 = EPSILON_0, c = C) => 1 / (eps0 * c * c),
    biotSavartPoint: (i, len, r) => MU_0 * i * len / (4 * PI * r * r),
    magneticFieldFromH: h => MU_0 * h,
    fineStructureConstant: (tet = true) => tet ? FINE_STRUCTURE : 7.2973525693e-3,
    ampereConstant: () => MU_0 / (2 * PI),
    impedanceOfFreeSpace: () => Math.sqrt(MU_0 / EPSILON_0),
    magneticForcePerLength: (i, r) => MU_0 * i * i / (2 * PI * r),
    longitudinalVelocity: () => (PI / 2) * C,
  };

  /* ---- optics ---- */
  const ELECTRON_REST_ENERGY = N_ELECTRON * M_Q * C2;
  const optics = {
    refractiveIndex: v => C / v, phaseVelocity: n => C / n,
    snell: (n1, t1, n2) => Math.asin(n1 * Math.sin(t1) / n2),
    photoelectricKE: (f, phi) => Math.max(0, H * f - phi),
    thresholdFrequency: phi => phi / H,
    pairProductionThreshold: () => 2 * ELECTRON_REST_ENERGY,
    reflectionAngle: i => i,
    wavelengthInMedium: (lamVac, n) => lamVac / n,
    amplitudeFromIntensity: I => Math.sqrt(I),
    superpose: (...a) => a.reduce((s, x) => s + x, 0),
    photoelectricThresholdFrequency: phi => phi / H,
    recoilMomentum: (E, m) => Math.sqrt(E * E - (m * C2) ** 2) / C,
  };

  /* ---- levels & spectra ---- */
  const RYDBERG = C / 27.49545417;   // his Tetryonic R_H = 10,903,346 (Book 2 p.118) -> 660nm
  // RYDBERG_OBSERVED declared at the top (constants block) — parity with constants.py
  const KEM_GROUND_EV = 13.525;      // his hydrogen ground (Book 3 p.75); 13.6 = std boundary
  const LEVEL_COLOURS = ["Brown", "Red", "Orange", "Yellow", "Green", "Aqua",
    "Blue", "Indigo", "Violet", "Black"];
  const SERIES = {lyman: 1, balmer: 2, paschen: 3, brackett: 4, pfund: 5,
    humphreys: 6, abraham: 7};
  const levels = {
    levelQuanta: n => n * n,
    levelStep: n => 2 * n - 1,
    shellQuanta: n => 12 * n * n,
    // His KEM ground 13.525 eV (Book 3 p.75 eigenstates −13.525/n²). 13.6 = std boundary only.
    hydrogenEnergy: n => -KEM_GROUND_EV / (n * n),
    ionizationEnergy: n => KEM_GROUND_EV / (n * n),
    // His Tetryonic Rydberg by default (660nm); pass observed=true for empirical 656.5nm.
    rydbergWavelength: (nl, nh, observed) => 1 / ((observed ? RYDBERG_OBSERVED : RYDBERG) * (1 / (nl * nl) - 1 / (nh * nh))),
    colour: n => LEVEL_COLOURS[n % 10],
    spinAngle: s => ({0.5: 720, 1: 360, 2: 180, 3: 120}[s]),
    shellName: n => (n >= 1 && n <= 8) ? "KLMNOPQR"[n - 1] : "n" + n,
    spinRotationAngle: spin => ({0.5: 720, 1: 360, 2: 180, 3: 120}[spin]),
  };
  const spectra = {
    SERIES,
    lowerLevel: s => SERIES[s.toLowerCase()],
    lineWavelength: (s, nh) => levels.rydbergWavelength(SERIES[s.toLowerCase()], nh),
    lineEnergyEv: (s, nh) => Math.abs(levels.hydrogenEnergy(nh) - levels.hydrogenEnergy(SERIES[s.toLowerCase()])),
    quantaDifferential: n => 12 * (2 * n - 1),
    allSeries: () => Object.keys(SERIES),
    seriesLowerLevel: s => SERIES[s.toLowerCase()],
    rydbergFactor: (nl, nh) => 1 / (nl * nl) - 1 / (nh * nh),
    seriesRydbergDivisor: s => 27.49545417 * SERIES[s.toLowerCase()] ** 2,
    seriesShellQuanta: s => 12 * SERIES[s.toLowerCase()] ** 2,
    seriesLines: (s, count = 4) => {
      const nl = SERIES[s.toLowerCase()], out = [];
      for (let nh = nl + 1; nh < nl + 1 + count; nh++) {
        out.push({transition: "n" + nh + "->n" + nl,
          wavelengthNm: levels.rydbergWavelength(nl, nh) * 1e9,
          energyEv: Math.abs(levels.hydrogenEnergy(nh) - levels.hydrogenEnergy(nl))});
      }
      return out;
    },
  };

  /* ---- electrical ---- */
  const electrical = {
    voltage: (i, r) => i * r, current: (v, r) => v / r, resistance: (v, i) => v / i,
    powerVI: (v, i) => v * i, powerI2R: (i, r) => i * i * r, powerV2R: (v, r) => v * v / r,
    work: (q, v) => q * v, eVtoJ: ev => ev * ELEMENTARY_CHARGE,
    capacitorEnergy: (c, v) => 0.5 * c * v * v,
    inductorEnergy: (l, i) => 0.5 * l * i * i,
    lcResonance: (l, c) => 1 / (2 * PI * Math.sqrt(l * c)),
    faradayEmf: (dFlux, dt, turns = 1) => -turns * dFlux / dt,
    inductorEmf: (l, di, dt) => -l * di / dt,
    capacitanceFromCharge: (q, v) => q / v,
    parallelPlateCapacitance: (A, d, er = 1) => er * EPSILON_0 * A / d,
    capacitorCharge: (c, v) => c * v,
    electricalWork: (q, v) => q * v,
    electronVoltToJoules: ev => ev * ELEMENTARY_CHARGE,
    joulesToElectronVolt: j => j / ELEMENTARY_CHARGE,
    displacementCurrent: (dEFlux, dt) => EPSILON_0 * dEFlux / dt,
    reactanceCapacitive: (f, c) => 1 / (2 * PI * f * c),
    reactanceInductive: (f, l) => 2 * PI * f * l,
    impedance: (r, xl = 0, xc = 0) => Math.sqrt(r * r + (xl - xc) ** 2),
    rcTimeConstant: (r, c) => r * c,
    lrTimeConstant: (l, r) => l / r,
    resistivityField: (rho, j) => rho * j,
    driftVelocity: (i, n, A, q = ELEMENTARY_CHARGE) => i / (n * q * A),
    evToKjPerMole: ev => ev * (ELEMENTARY_CHARGE * 6.022141579e23 / 1000),
    kjPerMoleToEv: kjMol => kjMol / (ELEMENTARY_CHARGE * 6.022141579e23 / 1000),
  };

  /* ---- waves ---- */
  const waves = {
    wavelength: f => C / f, frequency: lam => C / lam, wavenumber: lam => 1 / lam,
    photonEnergyFromFreq: f => H * f, photonEnergyFromWavelength: lam => H * C / lam,
    photonMomentum: lam => H / lam, inverseSquare: (i0, r) => i0 / (r * r),
    comptonShift: (theta, m = N_ELECTRON * M_Q) => (H / (m * C)) * (1 - Math.cos(theta)),
    angularFrequency: f => 2 * PI * f,
    wavelengthFromWavenumber: k => 1 / k,
    frequencyFromWavenumber: k => C * k,
    energyFromWavenumber: k => H * C * k,
    wavenumberFromEnergy: E => E / (H * C),
    wavelengthFromEnergy: E => H * C / E,
    frequencyFromEnergy: E => E / H,
    photonEnergyFromFrequency: f => H * f,
    bosonPhotonEnergy: (n, v) => n * H * v,
    eulerPhase: theta => ({re: Math.cos(theta), im: Math.sin(theta)}),
    photonPhaseOffset: index => index * PI / 2,
    comptonFrequency: m => m * C2 / H,
    vacuumEnergyWavelength: (lam, n) => lam / (2 * n * n),
  };

  /* ---- radiation ---- */
  const radiation = {
    wienPeak: T => 2.897771955e-3 / T,
    stefanBoltzmann: (T, A = 1, e = 1) => e * 5.670374419e-8 * A * Math.pow(T, 4),
    planckRadiance: (lam, T) => {
      const a = 2 * H * C * C / Math.pow(lam, 5);
      return a / (Math.expm1(H * C / (lam * K_B * T)));
    },
    stellarLuminosity: (R, T, e = 1) => e * 5.670374419e-8 * 4 * PI * R * R * Math.pow(T, 4),
    planckSpectralRadiance: (lam, T) => {
      const a = 2 * H * C * C / Math.pow(lam, 5);
      return a / (Math.expm1(H * C / (lam * K_B * T)));
    },
    wienPeakWavelength: T => 2.897771955e-3 / T,
    wienPeakFrequency: T => 2.821439372 * K_B * T / H,
    stefanBoltzmannPower: (T, A = 1, e = 1) => e * 5.670374419e-8 * A * Math.pow(T, 4),
    photonQuantaAtLevel: n => n * n,
    photonFlux: (P, f) => P / (H * f),
    photonIntensity: (P, A) => P / A,
    rayleighJeans: (lam, T) => 2 * C * K_B * T / Math.pow(lam, 4),
  };

  /* ---- particles ---- */
  const QUARKS = {up: [10, 2], down: [4, 8], "anti-up": [2, 10], "anti-down": [8, 4]};
  function compose(name, fl, nPlanck) {
    let cw = 0, ccw = 0; fl.forEach(f => {cw += QUARKS[f][0]; ccw += QUARKS[f][1];});
    return {name, cw, ccw, fascia: 12 * fl.length,
      topology: fl.length === 3 ? 20 : 8 * fl.length, nPlanck,
      chargeE: (cw - ccw) / 12, massKg: nPlanck == null ? null : nPlanck * M_Q};
  }
  const particles = {
    QUARKS,
    quark: f => ({name: f, cw: QUARKS[f][0], ccw: QUARKS[f][1], fascia: 12, topology: 8,
      chargeE: (QUARKS[f][0] - QUARKS[f][1]) / 12, massKg: null}),
    electron: () => ({name: "electron", cw: 0, ccw: 12, fascia: 12, topology: 12,
      chargeE: -1, massKg: N_ELECTRON * M_Q}),
    positron: () => ({name: "positron", cw: 12, ccw: 0, fascia: 12, topology: 12,
      chargeE: 1, massKg: N_ELECTRON * M_Q}),
    neutrino: () => ({name: "neutrino", cw: 6, ccw: 6, fascia: 12, topology: 12,
      chargeE: 0, massKg: null}),
    proton: () => compose("proton", ["up", "up", "down"], N_PROTON),
    neutron: () => compose("neutron", ["up", "down", "down"], N_NEUTRON),
    antiProton: () => compose("anti-proton", ["anti-up", "anti-up", "anti-down"], N_PROTON),
    baryon: (fl, n) => compose(fl.join(""), fl, n || null),
    standard: () => [particles.quark("up"), particles.quark("down"),
      particles.quark("anti-up"), particles.quark("anti-down"), particles.electron(),
      particles.positron(), particles.neutrino(), particles.proton(),
      particles.neutron(), particles.antiProton()],
    fromQuanta: (cw, ccw, nPlanck = null, fascia = null, name = "custom", kind = "particle") => {
      if (fascia == null) fascia = cw + ccw;
      return {name, cw, ccw, fascia, topology: fascia, nPlanck,
        chargeE: (cw - ccw) / 12, massKg: nPlanck == null ? null : nPlanck * M_Q};
    },
    meson: (flavour1, flavour2, name) => {
      const cw = QUARKS[flavour1][0] + QUARKS[flavour2][0];
      const ccw = QUARKS[flavour1][1] + QUARKS[flavour2][1];
      return {name: name || (flavour1 + "-" + flavour2), cw, ccw, fascia: 24, topology: 14,
        nPlanck: null, chargeE: (cw - ccw) / 12, massKg: null};
    },
    particle: name => {
      const reg = {up: () => particles.quark("up"), down: () => particles.quark("down"),
        "anti-up": () => particles.quark("anti-up"), "anti-down": () => particles.quark("anti-down"),
        electron: particles.electron, positron: particles.positron, neutrino: particles.neutrino,
        proton: particles.proton, neutron: particles.neutron, "anti-proton": particles.antiProton};
      return reg[name.toLowerCase()]();
    },
    standardParticles: () => particles.standard(),
  };

  /* ---- matter: build everything from the TETRYON (the base unit) ---- */
  // tetryon = 4 charged fascia. [cw,ccw]: positive[4,0], negative[0,4], gluon[2,2].
  const TET = {positive: [4, 0], negative: [0, 4], gluon: [2, 2]};
  const QUARK_RECIPES = {
    up: ["positive", "positive", "gluon"],      // [10,2]  +2/3
    down: ["negative", "gluon", "gluon"],       // [4,8]   -1/3
    "anti-up": ["negative", "negative", "gluon"],
    "anti-down": ["positive", "gluon", "gluon"],
  };
  const LEPTON_RECIPES = {electron: ["negative", "negative", "negative"],
    positron: ["positive", "positive", "positive"], neutrino: ["gluon", "gluon", "gluon"]};
  const BARYON_RECIPES = {proton: ["up", "up", "down"], neutron: ["up", "down", "down"]};
  const MESON_RECIPES = {"pi+": ["up", "anti-down"], "pi-": ["anti-up", "down"], "pi0": ["up", "anti-up"]};
  function assemble(tets) {
    let cw = 0, ccw = 0; tets.forEach(s => {cw += TET[s][0]; ccw += TET[s][1];});
    return {tetryons: tets, count: tets.length, cw, ccw, fascia: 4 * tets.length,
      chargeE: (cw - ccw) / 12};
  }
  const matter = {
    TET, QUARK_RECIPES, LEPTON_RECIPES, BARYON_RECIPES,
    tetryon: state => assemble([state]),
    buildQuark: f => ({...assemble(QUARK_RECIPES[f]), name: f, topology: 8}),
    buildLepton: n => ({...assemble(LEPTON_RECIPES[n]), name: n, topology: 12}),
    buildBaryon: n => {const tets = []; BARYON_RECIPES[n].forEach(q => tets.push(...QUARK_RECIPES[q]));
      return {...assemble(tets), name: n, topology: 20};},
    buildMeson: n => {const tets = []; MESON_RECIPES[n].forEach(q => tets.push(...QUARK_RECIPES[q]));
      return {...assemble(tets), name: n, topology: 14};},
    // recursively flatten any particle/atom to its tetryon-state list
    tetryonsOf: function f(n) {
      if (TET[n]) return [n];
      if (QUARK_RECIPES[n]) return QUARK_RECIPES[n].flatMap(f);
      if (LEPTON_RECIPES[n]) return LEPTON_RECIPES[n].flatMap(f);
      if (BARYON_RECIPES[n]) return BARYON_RECIPES[n].flatMap(f);
      if (n === "deuterium") return ["proton", "neutron", "electron"].flatMap(matter.tetryonsOf);
      if (n === "hydrogen") return ["proton", "electron"].flatMap(matter.tetryonsOf);
      return [];
    },
    buildDeuterium: () => ({...assemble(matter.tetryonsOf("deuterium")), name: "deuterium",
      subparticles: ["proton", "neutron", "electron"]}),
    buildHydrogen: () => ({...assemble(matter.tetryonsOf("hydrogen")), name: "hydrogen",
      subparticles: ["proton", "electron"]}),
    buildAtom: z => {const tets = z === 1 ? matter.tetryonsOf("hydrogen")
      : Array.from({length: z}, () => matter.tetryonsOf("deuterium")).flat();
      return {...assemble(tets), z, deuteriumUnits: z === 1 ? 0 : z};},
    build: n => QUARK_RECIPES[n] ? matter.buildQuark(n) : LEPTON_RECIPES[n] ? matter.buildLepton(n)
      : BARYON_RECIPES[n] ? matter.buildBaryon(n) : MESON_RECIPES[n] ? matter.buildMeson(n)
      : n === "deuterium" ? matter.buildDeuterium() : n === "hydrogen" ? matter.buildHydrogen() : null,
    tetryonCount: n => matter.tetryonsOf(n).length,
    buildTetryon: (state = "positive") => {
      const s = state === "neutral" ? "gluon" : state;
      return {...matter.tetryon(s), name: "tetryon(" + state + ")", kind: "tetryon", topology: 4};
    },
    matterPi: nTetryons => 4 * nTetryons,
  };

  /* ---- elements & chemistry ---- */
  const SYMBOLS = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe " +
    "Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe " +
    "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb " +
    "Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds " +
    "Rg Cn Nh Fl Mc Lv Ts Og").split(" ");
  const SYM2Z = {}; SYMBOLS.forEach((s, i) => SYM2Z[s] = i + 1);
  function atom(z, p, n, e) {
    const topo = 36 * (p + n) + 12 * e;
    const quanta = p * N_PROTON + n * N_NEUTRON + e * N_ELECTRON;
    return {z, symbol: SYMBOLS[z - 1] || ("Z" + z), protons: p, neutrons: n, electrons: e,
      topologyPi: topo, deuteriumUnits: topo / 84, planckQuanta: quanta,
      massKg: quanta * M_Q, massAmu: quanta * M_Q / (N_HYDROGEN * M_Q)};
  }
  // Nuclear energy-level mass model (Book 3 p.83/p.92): elements are n-level Deuterium
  // nuclei. Per-Deuteron mass-energy MeV(n) = 2*BARYON*((24+n)/25)^2 (levels 25..32 for
  // K..R). Deuterons occupy the SAME Aufbau shells as the electrons (each unit = p+n+e),
  // so mass grows with level n — NOT excess neutrons. Reproduces Kelvin's element pages.
  const SHELL_LETTERS = "KLMNOPQR";
  const ELECTRON_REST_MEV = ELECTRON_KEV / 1000.0;
  const DEUTERON_SHELL_MEV = Array.from({length: 8}, (_, i) =>
    2 * BARYON_MEV * Math.pow((24 + (i + 1)) / 25.0, 2));
  function nuclearShellFill(z) {
    const perN = {};
    for (const tok of electronConfig(z).split(" ")) {
      const n = +tok[0]; perN[n] = (perN[n] || 0) + (+tok.slice(2));
    }
    return Object.keys(perN).map(Number).sort((a, b) => a - b).map(n => ({
      n, letter: SHELL_LETTERS[n - 1], deuterons: perN[n],
      capacity: PERIODIC_SHELL_CAPS[n - 1] || 0,
      mevEach: DEUTERON_SHELL_MEV[n - 1], mevTotal: perN[n] * DEUTERON_SHELL_MEV[n - 1]}));
  }
  function nuclearMassMev(z) {
    if (z === 1) return BARYON_MEV + ELECTRON_REST_MEV;   // proton + electron, no neutron
    return nuclearShellFill(z).reduce((s, sh) => s + sh.mevTotal, 0) + z * ELECTRON_REST_MEV;
  }
  function parseFormula(f) {
    // expands parenthesised groups: Ca(OH)2 -> {Ca:1,O:2,H:2}; Ca3(PO4)2 -> {Ca:3,P:2,O:8}
    function parse(s, i) {
      const local = {};
      while (i < s.length) {
        const ch = s[i];
        if (ch === "(" || ch === "[" || ch === "{") {
          const [sub, j] = parse(s, i + 1); i = j;
          const m = /^\d+/.exec(s.slice(i)); const mult = m ? +m[0] : 1; if (m) i += m[0].length;
          for (const k in sub) local[k] = (local[k] || 0) + sub[k] * mult;
        } else if (ch === ")" || ch === "]" || ch === "}") {
          return [local, i + 1];
        } else {
          const m = /^([A-Z][a-z]?)(\d*)/.exec(s.slice(i));
          if (m && m[1]) {local[m[1]] = (local[m[1]] || 0) + (m[2] ? +m[2] : 1); i += m[0].length;}
          else i += 1;
        }
      }
      return [local, i];
    }
    return parse(f, 0)[0];
  }
  const MADELUNG = [[1,"s"],[2,"s"],[2,"p"],[3,"s"],[3,"p"],[4,"s"],[3,"d"],[4,"p"],
    [5,"s"],[4,"d"],[5,"p"],[6,"s"],[4,"f"],[5,"d"],[6,"p"],[7,"s"],[5,"f"],[6,"d"],[7,"p"]];
  const SUBCAP = {s: 2, p: 6, d: 10, f: 14};
  function electronConfig(z) {
    let rem = z; const parts = [];
    for (const [n, sub] of MADELUNG) {
      if (rem <= 0) break;
      const fill = Math.min(SUBCAP[sub], rem);
      parts.push(`${n}${sub}${fill}`); rem -= fill;
    }
    return parts.join(" ");
  }
  const elements = {
    SYMBOLS,
    element: z => atom(z, z, z === 1 ? 0 : z, z),
    isotope: (z, A) => atom(z, z, A - z, z),
    nuclearShellFill,
    nuclearMassMev,
    nuclearMassKg: z => constants.massFromMev(nuclearMassMev(z)),
    nuclearMassAmu: z => constants.amuFromMev(nuclearMassMev(z)),
    shellCapacity: n => 2 * n * n,
    periodicShellCap: lvl => PERIODIC_SHELL_CAPS[lvl - 1] || 0,
    ionisationEnergy: (z, n = 1) => 13.525 * z * z / (n * n),   // his KEM ground (Book 3 p.75)
    electronConfiguration: electronConfig,
    valenceElectrons: z => {const cfg = electronConfig(z).split(" ");
      const maxN = Math.max(...cfg.map(t => +t[0]));
      return cfg.filter(t => +t[0] === maxN).reduce((s, t) => s + +t.slice(2), 0);},
    atomsPerKg: z => 1 / elements.element(z).massKg,
    moleculeTopologyPi: f => Object.entries(parseFormula(f))
      .reduce((s, [sym, c]) => s + atom(SYM2Z[sym], SYM2Z[sym], SYM2Z[sym] === 1 ? 0 : SYM2Z[sym], SYM2Z[sym]).topologyPi * c, 0),
    moleculeMass: f => Object.entries(parseFormula(f))
      .reduce((s, [sym, c]) => s + elements.element(SYM2Z[sym]).massKg * c, 0),
    moleculeMassAmu: f => elements.moleculeMass(f) / (N_HYDROGEN * M_Q),
    moleculeNuclearMassAmu: f => Object.entries(parseFormula(f))
      .reduce((s, [sym, c]) => s + elements.nuclearMassAmu(SYM2Z[sym]) * c, 0),
    moleculeComposition: f => Object.entries(parseFormula(f)).map(([sym, c]) => {
      const z = SYM2Z[sym], a = elements.element(z);
      return {symbol: sym, z, count: c, topologyPi: a.topologyPi,
        massAmu: a.massAmu, shellMassAmu: elements.nuclearMassAmu(z)};}),
    dividesIntoDeuteriumUnits: f => elements.moleculeTopologyPi(f) % 84 === 0,
    balanceReaction: (reactants, products) => {
      const gcd = (a, b) => {a = Math.abs(a); b = Math.abs(b); while (b) {[a, b] = [b, a % b];} return a;};
      const fr = (n, d = 1) => {if (d < 0) {n = -n; d = -d;} const g = gcd(n, d) || 1; return [n / g, d / g];};
      const sub = (a, b) => fr(a[0] * b[1] - b[0] * a[1], a[1] * b[1]);
      const mul = (a, b) => fr(a[0] * b[0], a[1] * b[1]), div = (a, b) => fr(a[0] * b[1], a[1] * b[0]);
      const species = [...reactants, ...products], n = species.length;
      const counts = species.map(parseFormula);
      const sign = j => j < reactants.length ? 1 : -1;
      const els = [...new Set(species.flatMap(f => Object.keys(parseFormula(f))))].sort();
      const M = els.map(e => species.map((_, j) => fr(sign(j) * (counts[j][e] || 0))));
      const rows = M.length, cols = n, pivots = []; let r = 0;
      for (let c = 0; c < cols && r < rows; c++) {
        let piv = -1; for (let i = r; i < rows; i++) if (M[i][c][0] !== 0) {piv = i; break;}
        if (piv < 0) continue;
        [M[r], M[piv]] = [M[piv], M[r]];
        const pv = M[r][c]; M[r] = M[r].map(x => div(x, pv));
        for (let i = 0; i < rows; i++) if (i !== r && M[i][c][0] !== 0) {const f = M[i][c]; M[i] = M[i].map((a, k) => sub(a, mul(f, M[r][k])));}
        pivots.push(c); r++;
      }
      const free = [...Array(cols).keys()].filter(c => !pivots.includes(c));
      if (free.length !== 1) throw new Error("reaction not uniquely balanceable");
      const fcol = free[0]; const x = Array.from({length: cols}, () => [0, 1]); x[fcol] = [1, 1];
      pivots.forEach((pc, i) => {x[pc] = fr(-M[i][fcol][0], M[i][fcol][1]);});
      let denom = 1; x.forEach(v => {denom = denom * v[1] / gcd(denom, v[1]);});
      let ints = x.map(v => Math.round(v[0] * denom / v[1]));
      if (ints.every(v => v <= 0)) ints = ints.map(v => -v);
      let g = 0; ints.forEach(v => g = gcd(g, v)); if (g > 1) ints = ints.map(v => v / g);
      const out = {}; species.forEach((s, i) => out[s] = ints[i]); return out;
    },
    reactionConservesTopology: (reactants, products, coeffs) => {
      coeffs = coeffs || elements.balanceReaction(reactants, products);
      const side = arr => arr.reduce((s, f) => s + coeffs[f] * elements.moleculeTopologyPi(f), 0);
      return side(reactants) === side(products);
    },
    neutralise: (acid, base) => {
      const ACID = {HCl: ["Cl", -1], HNO3: ["NO3", -1], H2SO4: ["SO4", -2], H3PO4: ["PO4", -3],
        H2CO3: ["CO3", -2], HF: ["F", -1], HBr: ["Br", -1], HI: ["I", -1]};
      const BASE = {NaOH: ["Na", 1], KOH: ["K", 1], LiOH: ["Li", 1], CaO2H2: ["Ca", 2], MgO2H2: ["Mg", 2]};
      const gcd = (a, b) => {a = Math.abs(a); b = Math.abs(b); while (b) {[a, b] = [b, a % b];} return a;};
      if (!ACID[acid]) throw new Error("unsupported acid: " + acid);
      if (!BASE[base]) throw new Error("unsupported base: " + base);
      const [anion, qa] = ACID[acid], [cation, qc] = BASE[base];
      const g = gcd(Math.abs(qa), Math.abs(qc)), nCat = Math.abs(qa) / g, nAn = Math.abs(qc) / g;
      const sc = {[cation]: nCat}; for (const [s, c] of Object.entries(parseFormula(anion))) sc[s] = (sc[s] || 0) + c * nAn;
      const saltPlain = Object.keys(sc).map(s => s + (sc[s] > 1 ? sc[s] : "")).join("");
      const salt = (nAn > 1 && Object.keys(parseFormula(anion)).length > 1) ? `${cation}${nCat > 1 ? nCat : ""}(${anion})${nAn}` : saltPlain;
      const coeffs = elements.balanceReaction([acid, base], [saltPlain, "H2O"]);
      const term = f => coeffs[f] > 1 ? coeffs[f] + " " + f : f;
      const saltTerm = coeffs[saltPlain] > 1 ? coeffs[saltPlain] + " " + salt : salt;
      return {reaction: `${term(acid)} + ${term(base)} -> ${saltTerm} + ${term("H2O")}`, salt, coefficients: coeffs,
        conservesTopology: elements.reactionConservesTopology([acid, base], [saltPlain, "H2O"], coeffs)};
    },
    period: z => Math.max(...electronConfig(z).split(" ").map(t => +t[0])),
    allotropeTopologyPi: z => elements.element(z).topologyPi,
    bondOrder: sharedE => Math.floor(sharedE / 2),
    sigmaPiBonds: order => order < 1 ? [0, 0] : [1, order - 1],
    sharedElectronsForBond: order => 2 * order,
    fasciaBond: order => ({1: "single fascia bond", 2: "double fascia bonds", 3: "triple fascia bonds"}[order] || (order + "-fascia bonds")),
    isMetal: z => ![1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18, 34, 35, 36, 53, 54, 86, 118, 5, 14, 32, 33, 51, 52, 85].includes(z),
    isNonmetal: z => [1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18, 34, 35, 36, 53, 54, 86, 118].includes(z),
    bondType: (a, b) => {const za = SYM2Z[a], zb = SYM2Z[b], ma = elements.isMetal(za), mb = elements.isMetal(zb);
      if (ma && mb) return "metallic";
      if (ma !== mb) return (za === 4 || zb === 4) ? "covalent" : "ionic";   // Be forms covalent (p.370)
      return "covalent";},
    ionChargeQuanta: chargeE => 12 * chargeE,
    groupValence: z => elements.valenceElectrons(z),
    ionicBond: (cation, anion, nCat = 1, nAn = 1) => {
      const zc = SYM2Z[cation], za = SYM2Z[anion];
      const qc = elements.groupValence(zc), qa = elements.groupValence(za) - 8;
      const topo = elements.element(zc).topologyPi * nCat + elements.element(za).topologyPi * nAn;
      return {compound: cation + (nCat > 1 ? nCat : "") + anion + (nAn > 1 ? nAn : ""),
        cation, cationChargeE: qc, cationChargeQuanta: 12 * qc,
        anion, anionChargeE: qa, anionChargeQuanta: 12 * qa,
        netChargeE: qc * nCat + qa * nAn, topologyPi: topo, type: "ionic"};},
    molecularGeometry: (bonding, lone = 0) => {
      const G = {"2,0": ["linear", 180], "3,0": ["trigonal planar", 120], "4,0": ["tetrahedral", 109.5],
        "5,0": ["trigonal bipyramidal", 90], "6,0": ["octahedral", 90], "2,1": ["bent", 119],
        "3,1": ["trigonal pyramidal", 107], "2,2": ["bent", 104.5], "4,1": ["seesaw", 90],
        "3,2": ["T-shaped", 90], "2,3": ["linear", 180], "5,1": ["square pyramidal", 90], "4,2": ["square planar", 90]};
      const [shape, angle] = G[bonding + "," + lone] || ["unknown", 0];
      return {stericNumber: bonding + lone, shape, bondAngleDeg: angle, bondingRegions: bonding, lonePairs: lone};},
    centralLonePairs: (central, nBonded, charge = 0) => {
      const v = elements.groupValence(SYM2Z[central]) - charge; return Math.max(0, Math.floor((v - nBonded) / 2));},
    moleculeShape: name => {
      const S = {BeCl2: [2, 0], BH3: [3, 0], BF3: [3, 0], CH4: [4, 0], NH3: [3, 1], H2O: [2, 2], HF: [1, 0],
        CO2: [2, 0], HCHO: [3, 0], CH2O: [3, 0], C2H4: [3, 0], C2H2: [2, 0], PCl5: [5, 0], SF6: [6, 0]};
      const e = S[name]; if (!e) throw new Error("no tabulated shape for " + name);
      const [b, lp] = e; if (b === 1) return {stericNumber: 1, shape: "linear", bondAngleDeg: 180, bondingRegions: 1, lonePairs: lp};
      return elements.molecularGeometry(b, lp);},
    hydrogenRadical: () => ({species: "H", topologyPi: 48, cw: 24, ccw: 24, netChargeE: 0, role: "bonding agent / free radical"}),
    hydrogenBondQuanta: (nH = 1) => 48 * nH,
    polyatomicIon: name => {
      const T = {hydroxide: ["OH", -1], hydronium: ["H3O", 1], ammonium: ["NH4", 1], nitrate: ["NO3", -1],
        nitrite: ["NO2", -1], bicarbonate: ["HCO3", -1], carbonate: ["CO3", -2], sulfate: ["SO4", -2],
        sulfite: ["SO3", -2], phosphate: ["PO4", -3], cyanide: ["CN", -1], acetate: ["C2H3O2", -1],
        permanganate: ["MnO4", -1], chromate: ["CrO4", -2], peroxide: ["O2", -2]};
      const e = T[name.toLowerCase()]; if (!e) throw new Error("unknown polyatomic ion: " + name);
      const [formula, charge] = e;
      return {name: name.toLowerCase(), formula, chargeE: charge, chargeQuanta: 12 * charge,
        topologyPi: elements.moleculeTopologyPi(formula)};},
    lewisStructure: formula => {
      const counts = parseFormula(formula);
      const prio = {C: 0, Si: 1, B: 2, Al: 2, P: 3, N: 4, S: 5, O: 7, H: 9};
      const nonH = Object.keys(counts).filter(s => s !== "H");
      let central = "H";
      if (nonH.length) {const singles = nonH.filter(s => counts[s] === 1), pool = singles.length ? singles : nonH;
        central = pool.reduce((a, b) => ((prio[a] ?? 6) <= (prio[b] ?? 6) ? a : b));}
      const terminals = {}; for (const s in counts) if (s !== central) terminals[s] = counts[s];
      const nCentral = counts[central] || 1;
      let regions = Object.values(terminals).reduce((s, c) => s + c, 0);
      if (nCentral > 1) regions = Math.max(1, Math.floor(regions / nCentral) + 1);
      const totalVal = Object.entries(counts).reduce((s, [sym, c]) => s + elements.groupValence(SYM2Z[sym]) * c, 0);
      const SHAPES = {BeCl2: 1, BH3: 1, BF3: 1, CH4: 1, NH3: 1, H2O: 1, HF: 1, CO2: 1, HCHO: 1, CH2O: 1, C2H4: 1, C2H2: 1, PCl5: 1, SF6: 1};
      if (SHAPES[formula]) {const g = elements.moleculeShape(formula);
        return {...g, central, terminals, valenceElectrons: totalVal, exact: true};}
      const lone = elements.centralLonePairs(central, regions);
      const g = regions >= 1 ? elements.molecularGeometry(regions, lone)
        : {stericNumber: 0, shape: "monatomic", bondAngleDeg: 0, bondingRegions: 0, lonePairs: lone};
      return {...g, central, terminals, valenceElectrons: totalVal, exact: false};},
    orbital: sub => {const O = {s: {l: 0, orbitals: 1, capacity: 2, shape: "spherical", family: "Alkali metals & Alkaline earths"},
        p: {l: 1, orbitals: 3, capacity: 6, shape: "dumbbell (lobed)", family: "Non-metals, Halogens & Noble gases"},
        d: {l: 2, orbitals: 5, capacity: 10, shape: "cloverleaf", family: "Transition & post-Transition metals"},
        f: {l: 3, orbitals: 7, capacity: 14, shape: "complex (8-lobed)", family: "Lanthanoids & Actinoids"}};
      const o = O[sub.toLowerCase()]; if (!o) throw new Error("unknown subshell: " + sub); return {subshell: sub.toLowerCase(), ...o};},
    azimuthalQuantumNumber: sub => elements.orbital(sub).l,
    subshellCapacity: sub => elements.orbital(sub).capacity,
    elementOrbital: z => elements.orbital(elements.elementBlock(z)),
    bondGeometry: name => {const D = {CO2: {bond: "C=O", bondLengthPm: 116.3, shape: "linear", bondAngleDeg: 180},
        O3: {bond: "O-O", bondLengthPm: 127.8, shape: "bent", bondAngleDeg: 116.8}};
      if (D[name]) return {molecule: name, ...D[name]};
      const g = elements.moleculeShape(name); return {molecule: name, shape: g.shape, bondAngleDeg: g.bondAngleDeg};},
    commonIsotopes: z => ({1: [1, 2, 3], 2: [3, 4], 6: [12, 13, 14], 7: [14, 15], 8: [16, 17, 18], 17: [35, 37], 92: [234, 235, 238]}[z] || []),
    isotopeNotation: (z, A) => SYMBOLS[z - 1] + "-" + A,
    neutronNumber: (z, A) => A - z,
    molecularFormula: formula => {const c = parseFormula(formula), parts = [];
      if (c.C) {parts.push(["C", c.C]); delete c.C; if (c.H) {parts.push(["H", c.H]); delete c.H;}}
      Object.keys(c).sort().forEach(s => parts.push([s, c[s]]));
      return parts.map(([s, n]) => s + (n > 1 ? n : "")).join("");},
    areIsomers: (a, b) => a !== b && elements.molecularFormula(a) === elements.molecularFormula(b),
    acid: name => ELEMENT_ACIDS[name.toLowerCase()],
    hydrogen: () => ({...atom(1, 1, 0, 1), name: "protium"}),
    deuterium: () => ({...atom(1, 1, 1, 1), name: "deuterium"}),
    tritium: () => ({...atom(1, 1, 2, 1), name: "tritium"}),
    ion: (z, charge, name) => ({...atom(z, z, z === 1 ? 0 : z, z - charge),
      name: name || (SYMBOLS[z - 1] + (charge >= 0 ? "+" : "-") + Math.abs(charge))}),
    periodicTable: (zMax = 20) => Array.from({length: zMax}, (_, i) => elements.element(i + 1)),
    elementQuanta: z => elements.element(z).topologyPi,
    molarMass: z => elements.element(z).massAmu,
    elementBlock: z => {const t = electronConfig(z).split(" "); return t[t.length - 1][1];},
    valence: z => {
      const toks = electronConfig(z).split(" ");
      const maxN = Math.max(...toks.map(t => +t[0]));
      let v = toks.filter(t => +t[0] === maxN).reduce((s, t) => s + +t.slice(2), 0);
      for (const t of toks) {
        const n = +t[0], sub = t[1], cnt = +t.slice(2);
        if (n === maxN - 1 && sub === "d" && cnt < 10) v += cnt;
      }
      return v;
    },
    elementFamily: z => {
      const block = elements.elementBlock(z), v = elements.valenceElectrons(z);
      if (block === "f") return "Lanthanoid/Actinoid";
      if (block === "d") return "Transition metal";
      if (block === "s") return z === 2 ? "Noble gas" : (v === 1 ? "Alkali metal" : "Alkaline earth");
      if (v === 8) return "Noble gas";
      if (v === 7) return "Halogen";
      return "Non-metal / metalloid / post-transition";
    },
    nuclearShellReport: z => {
      const _pad = (s, w, right) => {s = String(s);
        while (s.length < w) s = right ? " " + s : s + " "; return s;};
      const _fix = (x, d) => x.toFixed(d);
      const _comma = x => {const s = x.toFixed(1).split(".");
        s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ","); return s.join(".");};
      const a = elements.element(z);
      const lines = ["Z=" + z + " " + a.symbol + "  - n-level Deuterium nuclei (Book 3 p.92)"];
      for (const sh of nuclearShellFill(z)) {
        lines.push("  " + sh.letter + " (n=" + sh.n + "): " + _pad(sh.deuterons, 2, true) + "/" +
          _pad(sh.capacity, 2, false) + " deuterons x " + _pad(_fix(sh.mevEach, 1), 7, true) +
          " MeV = " + _pad(_fix(sh.mevTotal, 1), 10, true) + " MeV");
      }
      lines.push("  + " + z + " electrons x " + _fix(ELECTRON_KEV, 3) + " keV");
      lines.push("  = " + _comma(nuclearMassMev(z)) + " MeV  ->  " + _fix(elements.nuclearMassAmu(z), 3) +
        " amu (flat base model: " + _fix(a.massAmu, 3) + " amu)");
      return lines.join("\n");
    },
  };
  const ELEMENT_ACIDS = {hydrochloric: "HCl", nitric: "HNO3", sulfuric: "H2SO4",
    phosphoric: "H3PO4", carbonic: "H2CO3", acetic: "C2H4O2", oxalic: "C2H2O4", citric: "C6H8O7"};
  const ELEMENT_BASES = {sodium_hydroxide: "NaOH", potassium_hydroxide: "KOH",
    ammonia: "NH3", calcium_hydroxide: "CaO2H2"};

  /* ---- cosmology ---- */
  const BODIES = {
    sun: {mass: 1.98892e30, radius: 6.9634e8},
    mercury: {mass: 3.3011e23, radius: 2.4397e6},
    venus: {mass: 4.8675e24, radius: 6.0518e6},
    earth: {mass: 5.9736e24, radius: 6.371e6},
    moon: {mass: 7.3477e22, radius: 1.7374e6},
    mars: {mass: 6.4171e23, radius: 3.3895e6},
    jupiter: {mass: 1.8982e27, radius: 6.9911e7},
    saturn: {mass: 5.6834e26, radius: 5.8232e7},
    uranus: {mass: 8.6810e25, radius: 2.5362e7},
    neptune: {mass: 1.02413e26, radius: 2.4622e7},
  };
  const cosmology = {
    BODIES,
    gravityForce: (m1, m2, r) => G * m1 * m2 / (r * r),
    surfaceGravity: (M, r) => G * M / (r * r),
    escapeVelocity: (M, r) => Math.sqrt(2 * G * M / r),
    orbitalVelocity: (M, r) => Math.sqrt(G * M / r),
    grFromGandSR: (g, sr) => g + sr,           // 4piG + 4piSR = 8piGR
    vacuumImpedance: () => EPSILON_0 * MU_0,    // 1/c^2
    bodyEscapeVelocity: n => Math.sqrt(2 * G * BODIES[n].mass / BODIES[n].radius),
    einsteinKappa: () => EINSTEIN_KAPPA,
    emToGravityRatio: () => (1 / (4 * PI * EPSILON_0)) / G,
    cosmicEnergyBudget: () => COSMIC,
    keplerPeriod: (a, M) => 2 * PI * Math.sqrt(a ** 3 / (G * M)),
    keplerSemimajor: (T, M) => Math.cbrt(G * M * T * T / (4 * PI * PI)),
    redshiftDoppler: v => {const b = v / C; return Math.sqrt((1 + b) / (1 - b)) - 1;},
    redshiftEnergyFalloff: (r, r0 = 1) => (r0 / r) ** 2,
    FORCE_STRENGTHS: {strong: 1e38, electromagnetic: 1e36, weak: 1e2, gravity: 1},
    FUSION_FRACTION: 1 / 3600,
    annihilationEnergy: m => m * C2,
    fusionEnergy: m => (1 / 3600) * m * C2,
    lightDeflection: (M, r) => 4 * G * M / (C2 * r),
    gravitationalRedshift: (M, r) => 1 / Math.sqrt(1 - 2 * G * M / (r * C2)) - 1,
    gemPinchRadius: M => 2 * G * M / C2,
    forceStrength: f => cosmology.FORCE_STRENGTHS[f],
    gravitationalAcceleration: (M, r) => G * M / (r * r),
    gravitationalPotentialEnergy: (m1, m2, r) => -G * m1 * m2 / r,
    gravityFieldDensity: density => 4 * PI * G * density,
    gravityGeometricMean: (m1, m2) => Math.sqrt(m1 * m2),
    lightDeflectionNewtonian: (M, r) => 2 * G * M / (C2 * r),
    mercuryPrecession: () => 43.0,                 // arcsec/century (Book 4 p.171)
    pioneerAnomaly: () => 8.74e-10,                // m/s^2 (Book 4 p.178)
    fissionQuantaRelease: (parentQuanta, daughterQuanta) => parentQuanta - daughterQuanta.reduce((s, d) => s + d, 0),
    quantaToEnergy: quanta => quanta * H,
    matterFromEnergy: E => E / (C2 * C2),
    matterDensity: emMassDensity => emMassDensity / (C2 * C2),
    bodyMass: name => BODIES[name.toLowerCase()].mass,
    bodyRadius: name => BODIES[name.toLowerCase()].radius,
    bodySurfaceGravity: name => {const b = BODIES[name.toLowerCase()]; return G * b.mass / (b.radius * b.radius);},
    gravitationalBindingEnergy: (mass, radius) => 3 * G * mass * mass / (5 * radius),
    rocheLimit: (primaryRadius, primaryDensity, satelliteDensity) => primaryRadius * Math.cbrt(2 * primaryDensity / satelliteDensity),
    tidalAcceleration: (mass, r, dr) => 2 * G * mass * dr / (r ** 3),
    gravitationalTimeDilation: (mass, r) => Math.sqrt(1 - 2 * G * mass / (r * C2)),
    poissonNewton: density => 4 * PI * G * density,
    poissonEinstein: density => 8 * PI * G * density,
    weightForce: (mass, g = 9.80665) => mass * g,
    stellarClass: massSolar => {
      const table = [["O", 16.0], ["B", 2.1], ["A", 1.4], ["F", 1.04], ["G", 0.8], ["K", 0.45], ["M", 0.0]];
      for (const [cls, lo] of table) if (massSolar >= lo) return cls;
      return "M";
    },
    planetDistanceKm: planet => {
      const LIGHT_SECOND_KM = 299792.458;
      const PLANET_LIGHT_SECONDS = {mercury: 192, venus: 360, earth: 499, mars: 759,
        jupiter: 2595, saturn: 4759, uranus: 9575, neptune: 14976};
      return PLANET_LIGHT_SECONDS[planet.toLowerCase()] * LIGHT_SECOND_KM;
    },
    gemFieldEquations: () => ({gaussGravity: "div E_g = -4*pi*G*rho", noGravimagneticMonopole: "div B_g = 0",
      faradayGravity: "curl E_g = -dB_g/dt", ampereGravity: "curl B_g = -(4*pi*G/c^2)*J + (1/c^2)*dE_g/dt"}),
    gemGravityFieldDivergence: density => -4 * PI * G * density,
    nettConvergentForce: (gravForce, emForce) => gravForce + emForce,
    galaxyRotationVelocity: (enclosedMass, r, emForce = 0, orbitingMass = 1) =>
      Math.sqrt(r * (G * enclosedMass * orbitingMass / (r * r) + emForce) / orbitingMass),
    darkMatterMomenta: frequency => H * frequency,
    darkEnergyMomenta: (mass, velocity) => 2 * mass * velocity * velocity,
    FUSION_VS_PINCH_RATIO: 3600,
    stellarCollapseEnergy: massKg => massKg * C2,
    fusionEfficiency: (kind = "hot") => ({hot: 1.0, cold: 0.125}[kind.toLowerCase()]),
  };

  /* ---- geometrics ---- */
  // Classical Platonic solids — kept only for Kelvin's p19 COMPARISON.
  const PLATONIC = {tetrahedron: [4, 6, 4], cube: [6, 12, 8], octahedron: [8, 12, 6],
    dodecahedron: [12, 30, 20], icosahedron: [20, 30, 12]};
  // Kelvin's actual particle solids are DELTAHEDRA (all-triangle faces, Book 5 p20).
  // NB: the lepton's dodeca-deltahedron has 12 TRIANGLE faces (12,18,8), NOT the
  // Platonic dodecahedron's 12 pentagons (12,30,20).
  const DELTAHEDRA = {"tetra-deltahedron": [4, 6, 4], "octa-deltahedron": [8, 12, 6],
    "dodeca-deltahedron": [12, 18, 8], "icoso-deltahedron": [20, 30, 12]};
  // particle -> [deltahedron, topology_pi (=faces), mass_energy_pi]
  const PARTICLE_SOLID = {tetryon: ["tetra-deltahedron", 4, 4], quark: ["octa-deltahedron", 8, 12],
    lepton: ["dodeca-deltahedron", 12, 12], baryon: ["icoso-deltahedron", 20, 36]};
  const SQRT2 = Math.sqrt(2), SQRT5 = Math.sqrt(5);
  const _AREA = {tetrahedron: a => SQRT3 * a * a, cube: a => 6 * a * a,
    octahedron: a => 2 * SQRT3 * a * a,
    dodecahedron: a => 3 * Math.sqrt(25 + 10 * SQRT5) * a * a, icosahedron: a => 5 * SQRT3 * a * a};
  const _VOL = {tetrahedron: a => a ** 3 / (6 * SQRT2), cube: a => a ** 3,
    octahedron: a => (SQRT2 / 3) * a ** 3, dodecahedron: a => (15 + 7 * SQRT5) / 4 * a ** 3,
    icosahedron: a => 5 * (3 + SQRT5) / 12 * a ** 3};
  // PHI is defined at the top of the module (parity with constants.PHI)
  const _DELTA_VOL = {"tetra-deltahedron": a => a ** 3 / (6 * SQRT2),
    "octa-deltahedron": a => (SQRT2 / 3) * a ** 3,
    "dodeca-deltahedron": a => 0.859493 * a ** 3,   // snub disphenoid
    "icoso-deltahedron": a => 5 * (3 + SQRT5) / 12 * a ** 3};
  const geometrics = {
    PLATONIC, DELTAHEDRA, PARTICLE_SOLID, PHI,
    equilateralArea: s => (SQRT3 / 4) * s * s,
    equilateralHeight: s => (SQRT3 / 2) * s,
    inradius: s => s / (2 * SQRT3), circumradius: s => s / SQRT3,
    perimeter: s => 3 * s,
    incircleArea: s => PI * (s / (2 * SQRT3)) ** 2,
    circumcircleArea: s => PI * (s / SQRT3) ** 2,
    hexagonArea: s => (3 * SQRT3 / 2) * s * s,
    regularPolygonArea: (n, s) => 0.25 * n * s * s / Math.tan(PI / n),
    polygonInteriorAngle: n => (n - 2) * 180 / n,
    polygonExteriorAngle: n => 360 / n,
    eutrigonC2: (a, b) => a * a + b * b - a * b,
    triangularNumber: n => n * (n + 1) / 2,
    squareFromOdds: n => n * n,
    sumOfCubes: n => (n * (n + 1) / 2) ** 2,
    geometricMean: (a, b) => Math.sqrt(a * b),
    goldenRatio: () => PHI,
    fourthPower: n => n ** 4,
    twinTriangularSquare: n => n * (n + 1) / 2 + (n - 1) * n / 2,
    binomial: (n, k) => {let r = 1; for (let i = 0; i < k; i++) r = r * (n - i) / (i + 1); return Math.round(r);},
    pascalRow: n => Array.from({length: n + 1}, (_, k) => geometrics.binomial(n, k)),
    lawOfCosines: (a, b, Cdeg) => Math.sqrt(a * a + b * b - 2 * a * b * Math.cos(Cdeg * PI / 180)),
    geometricSeriesSum: (r, terms) => terms == null ? 1 / (1 - r) : (1 - r ** terms) / (1 - r),
    dihedralAngle: solid => ({tetrahedron: Math.acos(1 / 3) * 180 / PI, cube: 90,
      octahedron: Math.acos(-1 / 3) * 180 / PI, dodecahedron: Math.acos(-1 / SQRT5) * 180 / PI,
      icosahedron: Math.acos(-SQRT5 / 3) * 180 / PI}[solid]),
    eulerCharacteristic: solid => {const [f, e, v] = (DELTAHEDRA[solid] || PLATONIC[solid]); return f - e + v;},
    platonicMetrics: (solid, edge = 1) => ({area: _AREA[solid](edge), volume: _VOL[solid](edge)}),
    deltahedronMetrics: (solid, edge = 1) => {const [f] = DELTAHEDRA[solid];
      return {area: f * (SQRT3 / 4) * edge * edge, volume: _DELTA_VOL[solid](edge)};},
    solidForParticle: p => {const [s, topo, me] = PARTICLE_SOLID[p], [f, e, v] = DELTAHEDRA[s];
      return {solid: s, faces: f, edges: e, vertices: v, topologyPi: topo, massEnergyPi: me};},
    apothem: (n, s) => s / (2 * Math.tan(PI / n)),
    regularPolygonPerimeter: (n, s) => n * s,
    regularPolygonMetrics: (n, s) => ({perimeter: n * s, apothem: s / (2 * Math.tan(PI / n)),
      area: 0.25 * n * s * s / Math.tan(PI / n), interiorAngle: (n - 2) * 180 / n, exteriorAngle: 360 / n}),
    vivianiDistanceSum: s => (SQRT3 / 2) * s,
    incircleToTriangleRatio: () => PI / (3 * SQRT3),
    areaPerimeterRatio: () => 1 / (12 * SQRT3),
    eutrigonIdentity: (a, b, c) => (a * b) - (a * a + b * b - c * c),
    nthOdd: n => 2 * n - 1,
    nthEven: n => 2 * n,
    pentagonalNumber: n => Math.floor(n * (3 * n - 1) / 2),
    tetrahedralNumber: n => Math.floor(n * (n + 1) * (n + 2) / 6),
    squarePyramidalNumber: n => Math.floor(n * (n + 1) * (2 * n + 1) / 6),
    goldenPower: n => PHI ** n,
    taylorExp: (x, terms = 12) => {let s = 0, f = 1; for (let k = 0; k < terms; k++) {if (k > 0) f *= k; s += x ** k / f;} return s;},
    taylorSin: (x, terms = 10) => {let s = 0; for (let k = 0; k < terms; k++) {let f = 1; for (let i = 2; i <= 2 * k + 1; i++) f *= i; s += (-1) ** k * x ** (2 * k + 1) / f;} return s;},
    taylorCos: (x, terms = 10) => {let s = 0; for (let k = 0; k < terms; k++) {let f = 1; for (let i = 2; i <= 2 * k; i++) f *= i; s += (-1) ** k * x ** (2 * k) / f;} return s;},
    eulerIdentity: () => ({re: Math.cos(PI) + 1, im: Math.sin(PI)}),
    cPowerLadder: n => C ** n,
    keplerBouwkamp: (terms = 1000) => {let p = 1; for (let n = 3; n <= terms; n++) p *= Math.cos(PI / n); return p;},
    // Golden ratio phi from George Odom's construction (Book 5 p.182): equilateral triangle
    // inscribed in a circle; midpoints P,Q of two sides, extend PQ to the circle at R -> PQ:QR = phi.
    odomGoldenRatio: () => {
      const a = [0, 1], b = [-Math.sqrt(3) / 2, -0.5], c = [Math.sqrt(3) / 2, -0.5];
      const p = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], q = [(a[0] + c[0]) / 2, (a[1] + c[1]) / 2];
      const xR = Math.sqrt(1 - q[1] * q[1]);
      return (q[0] - p[0]) / (xR - q[0]);
    },
    // Kelvin's KE energy "diamond" is a golden rhombus (Book 5 p.183): diagonals in ratio phi:1.
    goldenRhombus: (shortDiagonal = 1) => {
      const sD = shortDiagonal, lD = PHI * sD;
      const acute = 2 * Math.atan2(sD / 2, lD / 2) * 180 / PI;
      return {shortDiagonal: sD, longDiagonal: lD, diagonalRatio: PHI, side: Math.hypot(lD / 2, sD / 2),
        acuteAngleDeg: acute, obtuseAngleDeg: 180 - acute, area: lD * sD / 2};
    },
    sinDeg: a => Math.sin(a * PI / 180),
    cosDeg: a => Math.cos(a * PI / 180),
    tanDeg: a => Math.tan(a * PI / 180),
    cartesianToPolar: (x, y) => [Math.hypot(x, y), Math.atan2(y, x) * 180 / PI],
    polarToCartesian: (r, thetaDeg) => {const t = thetaDeg * PI / 180; return [r * Math.cos(t), r * Math.sin(t)];},
    sideFromArea: area => Math.sqrt(4 * area / SQRT3),
    eulerInequalityOk: (R, r) => R >= 2 * r - 1e-12,
    baselSum: terms => {let s = 0; for (let n = 1; n <= terms; n++) s += 1 / (n * n); return s;},
    piContent: shape => ({triangle: 1, square: 2, hexagon: 4, circle: 2}[shape]) * PI,
    particleSolidMetrics: (particle, edge = 1) => {const info = geometrics.solidForParticle(particle);
      const m = geometrics.deltahedronMetrics(info.solid, edge); info.area = m.area; info.volume = m.volume; return info;},
    imaginaryRotation: (x, y, quarterTurns = 1) => {for (let i = 0; i < ((quarterTurns % 4) + 4) % 4; i++) {const t = x; x = -y; y = t;} return [x, y];},
    iPower: n => [[1, 0], [0, 1], [-1, 0], [0, -1]][((n % 4) + 4) % 4],
    oddAsSquareDifference: n => n * n - (n - 1) * (n - 1),
    equilateralDistribution: n => {if (n < 1) return []; const out = [];
      for (let i = 1; i <= n; i++) out.push(i); for (let i = n - 1; i >= 1; i--) out.push(i); return out;},
    probabilityFromAmplitude: amplitude => amplitude * amplitude,
    infinitiesExist: () => false,
  };

  /* ---- kinematics ---- */
  const kinematics = {
    velocity: (dx, dt) => dx / dt, acceleration: (dv, dt) => dv / dt,
    force: (m, a) => m * a, momentum: (m, v) => m * v,
    impulse: (F, t) => F * t, work: (F, d) => F * d, power: (W, t) => W / t,
    kineticEnergy: (m, v) => 0.5 * m * v * v,  // ⚠ classical ½mv², comparison only (his = energy.scalarEnergy E=mv²)
    centripetalAcceleration: (v, r) => v * v / r,
    shmRestoringForce: (k, x) => -k * x,
    shmPeriod: (m, k) => 2 * PI * Math.sqrt(m / k),
    shmFrequency: (m, k) => 1 / (2 * PI * Math.sqrt(m / k)),
  };

  /* ---- thermodynamics ---- */
  const R_GAS = 8.314462618;
  const thermodynamics = {
    K_B, R_GAS,
    entropyBoltzmann: W => K_B * Math.log(W),
    entropyClausius: (Q, T) => Q / T,
    idealGasPressure: (n, T, V) => n * R_GAS * T / V,
    idealGasVolume: (n, T, P) => n * R_GAS * T / P,
    idealGasTemperature: (P, V, n) => P * V / (n * R_GAS),
    idealGasMoles: (P, V, T) => P * V / (R_GAS * T),
    thermalEnergy: T => K_B * T,
    pressureEnergyDensity: (E, V) => E / V,
    internalEnergy: (n, T, dof = 3) => (dof / 2) * n * R_GAS * T,
    carnotEfficiency: (Th, Tc) => 1 - Tc / Th,
    bekensteinHawkingEntropy: A => A * K_B * C ** 3 / (4 * G * H_BAR),
  };

  /* ---- statistics ---- */
  const statistics = {
    bornRule: a => a * a,
    gaussian: (x, mu = 0, s = 1) => 1 / (s * Math.sqrt(2 * PI)) * Math.exp(-((x - mu) ** 2) / (2 * s * s)),
    binomialProbability: (n, k, p) => geometrics.binomial(n, k) * p ** k * (1 - p) ** (n - k),
    heisenbergMinMomentum: dx => H_BAR / (2 * dx),
    heisenbergMinEnergy: dt => H_BAR / (2 * dt),
    normalEmpiricalRule: () => [0.6827, 0.9545, 0.9973],
    standardDeviation: v => {const mu = v.reduce((a, b) => a + b, 0) / v.length;
      return Math.sqrt(v.reduce((a, x) => a + (x - mu) ** 2, 0) / v.length);},
    zScore: (x, mu, s) => (x - mu) / s,
    shannonEntropy: ps => -ps.filter(p => p > 0).reduce((a, p) => a + p * Math.log2(p), 0),
  };

  /* ---- number theory ---- */
  const numbertheory = {
    digitalRoot: n => n === 0 ? 0 : 1 + (Math.abs(n) - 1) % 9,
    isPrime: n => {if (n < 2) return false; if (n < 4) return true; if (n % 2 === 0) return false;
      for (let i = 3; i * i <= n; i += 2) if (n % i === 0) return false; return true;},
    isTwinPrimeForm: n => n % 6 === 1 || n % 6 === 5,
    mersenne: n => 2 ** n - 1,
    isMersennePrime: n => numbertheory.isPrime(n) && numbertheory.isPrime(2 ** n - 1),
    fibonacci: n => {let a = 0, b = 1; for (let i = 0; i < n; i++) [a, b] = [b, a + b]; return a;},
    fibonacciRatio: n => numbertheory.fibonacci(n + 1) / numbertheory.fibonacci(n),
    lucas: n => {let a = 2, b = 1; for (let i = 0; i < n; i++) [a, b] = [b, a + b]; return a;},
    isPerfectNumber: n => {if (n < 2) return false; let s = 0;
      for (let d = 1; d < n; d++) if (n % d === 0) s += d; return s === n;},
    goldbachPair: n => {for (let p = 2; p <= n; p++) if (numbertheory.isPrime(p) && numbertheory.isPrime(n - p)) return [p, n - p]; return [];},
    primesUpTo: limit => {
      if (limit < 2) return [];
      const sieve = new Array(limit + 1).fill(true);
      sieve[0] = sieve[1] = false;
      for (let i = 2; i * i <= limit; i++) if (sieve[i])
        for (let j = i * i; j <= limit; j += i) sieve[j] = false;
      const out = []; for (let i = 0; i <= limit; i++) if (sieve[i]) out.push(i); return out;
    },
    primeAsSquareDifference: n => {
      if (n % 2 === 0) throw new Error("only odd numbers are a difference of consecutive squares");
      const k = (n + 1) / 2 | 0; return [k, k - 1];
    },
  };

  /* ---- music ---- */
  const NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const JUST = {unison: [1,1], minor_third: [6,5], major_third: [5,4], fourth: [4,3],
    fifth: [3,2], major_sixth: [5,3], octave: [2,1]};
  const music = {
    NOTES,
    noteIndex: note => NOTES.indexOf(note.toUpperCase()),
    noteToPhase: note => NOTES.indexOf(note.toUpperCase()) * 30,
    intervalRatio: name => {const [a, b] = JUST[name]; return a / b;},
    intervalFromFrequencies: (lo, hi) => hi / lo,
    equalTemperedFrequency: midi => 440 * 2 ** ((midi - 69) / 12),
    semitonesToRatio: s => 2 ** (s / 12),
    noteFrequency: (note, octave = 4) => 440 * 2 ** ((12 * (octave + 1) + NOTES.indexOf(note.toUpperCase()) - 69) / 12),
    circleOfFifths: () => {const o = []; let i = 0; for (let k = 0; k < 12; k++) {o.push(NOTES[i % 12]); i += 7;} return o;},
    scaleRatios: (scale = "major") => {
      const scales = {
        major: [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2],
        pentatonic: [1, 9/8, 5/4, 3/2, 5/3, 2],
        chromatic: Array.from({length: 13}, (_, i) => 2 ** (i / 12)),
      };
      return scales[scale.toLowerCase()];
    },
  };

  /* ---- biochem ---- */
  const AMINO_ACIDS = {glycine: "C2H5NO2", alanine: "C3H7NO2", serine: "C3H7NO3",
    valine: "C5H11NO2", leucine: "C6H13NO2", lysine: "C6H14N2O2", glutamate: "C5H9NO4",
    phenylalanine: "C9H11NO2", tyrosine: "C9H11NO3", tryptophan: "C11H12N2O2"};
  const SUGARS = {glucose: "C6H12O6", fructose: "C6H12O6", ribose: "C5H10O5",
    deoxyribose: "C5H10O4", sucrose: "C12H22O11"};
  const BASES = {adenine: "C5H5N5", guanine: "C5H5N5O", cytosine: "C4H5N3O",
    thymine: "C5H6N2O2", uracil: "C4H4N2O2"};
  const biochem = {
    WATER_QUANTA: 768, CARBOHYDRATE_UNIT: 1272, AMINO_ACIDS, SUGARS, BASES,
    moleculeQuanta: f => elements.moleculeTopologyPi(f),
    aminoAcidQuanta: name => elements.moleculeTopologyPi(AMINO_ACIDS[name.toLowerCase()]),
    sugarQuanta: name => elements.moleculeTopologyPi(SUGARS[name.toLowerCase()]),
    baseQuanta: name => elements.moleculeTopologyPi(BASES[name.toLowerCase()]),
    complementaryBase: (base, rna = false) => {
      const DNA = {adenine: "thymine", thymine: "adenine", guanine: "cytosine", cytosine: "guanine"};
      const RNA = {adenine: "uracil", uracil: "adenine", guanine: "cytosine", cytosine: "guanine"};
      return (rna ? RNA : DNA)[base.toLowerCase()];},
    basePairQuanta: (base, rna = false) => biochem.baseQuanta(base) + biochem.baseQuanta(biochem.complementaryBase(base, rna)),
    peptideQuanta: res => res.reduce((s, r) => s + biochem.aminoAcidQuanta(r), 0) - 768 * (res.length - 1),
    polysaccharideQuanta: (mono, n) => n * biochem.sugarQuanta(mono) - 768 * (n - 1),
    condensationWater: bonds => 768 * bonds,
    nucleotideQuanta: (base, deoxy = false) => {
      const sugar = deoxy ? "deoxyribose" : "ribose";
      const phosphate = elements.moleculeTopologyPi("H3PO4");
      return biochem.baseQuanta(base) + biochem.sugarQuanta(sugar) + phosphate - 2 * 768;
    },
    functionalGroupQuanta: group => {
      const FUNCTIONAL_GROUPS = {CH: 552, CH2: 600, CH3: 648, OH: 720,
        NH2: 684, NO2: 1932, NO3: 2604, COOH: null};
      const v = FUNCTIONAL_GROUPS[group];
      return v == null ? elements.moleculeTopologyPi(group) : v;
    },
  };

  /* ---- geometry primitives ---- */
  /* ---- dynamics (his-method interactions: emission, absorption, GEM pinch, forces) ---- */
  // KEM_EV declared at the top (constants block) — parity with constants.py
  const FUSION_FRACTION = 1 / 3600;      // stellar p-p release = 1/3600 of full pinch
  const dynamics = {
    KEM_EV, FUSION_FRACTION,
    levelEnergyEv: n => -KEM_EV / (n * n),
    shellQuanta: n => 12 * n * n,
    emitPhoton(nHigh, nLow) {
      if (nHigh <= nLow) throw new Error("emission requires nHigh > nLow");
      const energyEv = Math.abs(dynamics.levelEnergyEv(nHigh) - dynamics.levelEnergyEv(nLow));
      const energyJ = energyEv * ELEMENTARY_CHARGE;
      const wavelengthM = H * C / energyJ;
      const quanta = dynamics.shellQuanta(nHigh) - dynamics.shellQuanta(nLow);
      return {kind: "emission", before: `electron n${nHigh}`, after: `electron n${nLow} + photon`,
        quanta, energyJ, energyEv, wavelengthM,
        detail: {photon: "diamond (even quanta, neutral)", evenQuanta: quanta}};
    },
    absorbPhoton(nLow, photonEnergyEv, maxLevel = 50) {
      let best = null, bestErr = 1e9;
      for (let n = nLow + 1; n <= maxLevel; n++) {
        const e = Math.abs(dynamics.levelEnergyEv(n) - dynamics.levelEnergyEv(nLow));
        if (Math.abs(e - photonEnergyEv) < bestErr) { best = n; bestErr = Math.abs(e - photonEnergyEv); }
      }
      const ionised = photonEnergyEv >= Math.abs(dynamics.levelEnergyEv(nLow));
      const after = ionised ? "free electron (ionised)" : `electron n${best}`;
      const quanta = best ? (dynamics.shellQuanta(best) - dynamics.shellQuanta(nLow)) : 0;
      return {kind: "absorption", before: `electron n${nLow} + photon`, after,
        quanta, energyEv: photonEnergyEv, energyJ: photonEnergyEv * ELEMENTARY_CHARGE,
        detail: {reachedLevel: best, ionised}};
    },
    pinch(massKg) {
      const energyJ = massKg * C2;
      return {kind: "pinch", before: `Matter ${massKg.toExponential(3)} kg`, after: "radiant 2D EM mass-energy",
        quanta: 0, energyJ, energyEv: energyJ / ELEMENTARY_CHARGE, wavelengthM: 0,
        detail: {efficiency: 1, note: "Matter -> light+heat (stellar core)"}};
    },
    fusion(massKg) {
      const energyJ = FUSION_FRACTION * massKg * C2;
      return {kind: "fusion", before: `Matter ${massKg.toExponential(3)} kg`, after: "radiant energy (partial)",
        quanta: 0, energyJ, energyEv: energyJ / ELEMENTARY_CHARGE, wavelengthM: 0,
        detail: {efficiency: FUSION_FRACTION}};
    },
    pairCreation(photonEnergyJ) {
      const threshold = 2 * N_ELECTRON * M_Q * C2;
      const makesPair = photonEnergyJ >= threshold;
      return {kind: "pair_creation", before: "photon", after: makesPair ? "e- + e+ pair" : "photon (below threshold)",
        quanta: 0, energyJ: photonEnergyJ, energyEv: photonEnergyJ / ELEMENTARY_CHARGE, wavelengthM: 0,
        detail: {thresholdJ: threshold, createsPair: makesPair}};
    },
    chargeInteraction(p1, p2, r) {
      const q1 = (p1 != null && p1.chargeE !== undefined) ? p1.chargeE * ELEMENTARY_CHARGE : p1;
      const q2 = (p2 != null && p2.chargeE !== undefined) ? p2.chargeE * ELEMENTARY_CHARGE : p2;
      const f = (1 / (4 * PI * EPSILON_0)) * q1 * q2 / (r * r);
      let direction;
      if (q1 === 0 || q2 === 0) direction = "neutral";
      else if ((q1 > 0) === (q2 > 0)) direction = "repel";
      else direction = "attract";
      return {kind: "electromagnetic", direction, forceN: Math.abs(f), detail: {q1, q2, seeks: "equilibrium"}};
    },
    strongInteraction(fasciaSignA, fasciaSignB) {
      let direction;
      if (fasciaSignA === 0 || fasciaSignB === 0) direction = "neutral";
      else if (fasciaSignA === fasciaSignB) direction = "repel";
      else direction = "attract";
      return {kind: "strong", direction, forceN: 0, detail: {fascia: [fasciaSignA, fasciaSignB]}};
    },
    seekEquilibrium(...particles) {
      const cw = particles.reduce((s, p) => s + p.cw, 0);
      const ccw = particles.reduce((s, p) => s + p.ccw, 0);
      return {cw, ccw, netQuanta: cw - ccw, netChargeE: (cw - ccw) / 12, neutral: cw === ccw};
    },
    spectralEmission(series, nHigh) {
      return dynamics.emitPhoton(nHigh, SERIES[series.toLowerCase()]);
    },
  };

  const geometry = {
    unitsInTriangle: n => n * n,
    unitsInRow: r => 2 * r - 1,
    isSquare: n => {const s = Math.round(Math.sqrt(n)); return s * s === n;},
    equilateralArea: s => (SQRT3 / 4) * s * s,
    // EM field quantum geometries (flat tilings of n² triangles):
    // boson = 1 triangle (n²); photon = a DIAMOND of 2 triangles (2n², neutral, planar, c).
    bosonQuanta: n => n * n,
    photonQuanta: n => 2 * n * n,
    fieldQuanta: (fascia, n) => fascia * n * n,   // boson1 photon2 tetryon4 lepton12
    photonVertices: (size = 1) => {const h = (SQRT3 / 2) * size;
      return [[0, h, 0], [-size / 2, 0, 0], [0, -h, 0], [size / 2, 0, 0]];},
    LEVEL_COLOURS,
    PROPERTY_COLOURS: {momentum: "Pink", positive: "Red", neutral: "Blue",
      negative: "Black", energy: "Maroon", mass: "Blue", chargeGeometry: "Gold"},
    levelColour: level => LEVEL_COLOURS[level % 10],
    upDownInRow: r => [r, r - 1],
    oddSumToSquare: n => {let s = 0; for (let r = 1; r <= n; r++) s += 2 * r - 1; return s;},
    positiveTetryon: (level = 1) => ({level, cw: 4, ccw: 0, fascia: 4, netChargeQuanta: 4,
      isNeutral: false, units: 4 * level * level}),
    negativeTetryon: (level = 1) => ({level, cw: 0, ccw: 4, fascia: 4, netChargeQuanta: -4,
      isNeutral: false, units: 4 * level * level}),
    neutralTetryon: (level = 1) => ({level, cw: 2, ccw: 2, fascia: 4, netChargeQuanta: 0,
      isNeutral: true, units: 4 * level * level}),
  };

  // --- units: the Tetryonic physics-units map (Book 1 p.40) — ported from units.py ---
  const UNITS = {
    wavelength:        ["λ", "m", "spatial extent"],
    velocity:          ["v", "m/s", "1D, vector"],
    acceleration:      ["a", "m/s²", "Δv/Δt"],
    frequency:         ["f", "1/s", "f = 2v (longitudinal cycles)"],
    linear_momentum:   ["p", "kg·m/s", "p = mv"],
    force:             ["F", "kg·m/s²", "F = ma = dp/dt"],
    energy:            ["E", "kg·m²/s²", "E = mv² = hv²"],
    qam:               ["Ω", "m²/s", "quantised angular momentum (hidden constant)"],
    planck_constant:   ["h", "kg·m²/s", "h = mΩ = quantum of action & of mass"],
    em_mass:           ["m", "kg", "2D planar energy/second = E/c²"],
    matter:            ["M", "kg", "3D tetrahedral topology = E/c⁴"],
    charge:            ["q", "kg·s", "mass·QAM/second = Ω/c² per fascia"],
    electric_constant: ["ε₀", "F/m", "= 1/(μ₀c²)"],
    magnetic_constant: ["μ₀", "H/m", "= 1/(ε₀c²) = 4π×10⁻⁷"],
    current:           ["I", "kg/s", "charged Matter in motion"],
    celeritas_squared: ["c²", "m²/s²", "proportionality constant between coordinate systems"]};
  const units = {
    UNITS,
    describe: q => { const u = UNITS[q]; return q + ": " + u[0] + " [" + u[1] + "] — " + u[2]; },
    allUnits: () => Object.keys(UNITS).map(q => units.describe(q)),
    colourCodes: () => ({energy_level: geometry.LEVEL_COLOURS, physics_property: geometry.PROPERTY_COLOURS})};

  return {version: "0.13.0", constants, geometry, energy, charge, fields, levels,
    spectra, electrical, waves, radiation, optics, particles, elements, cosmology, geometrics,
    thermodynamics, statistics, numbertheory, music, biochem, kinematics, matter, dynamics, units};
}));

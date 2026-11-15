# Engineering Rebuild

Hands-on log of rebuilding my electronics and computer-engineering skills, from logic gates on a breadboard up to a RISC-V CPU on an FPGA.

**Background:** B.E. in Electronics and Communication Engineering (2022).
**Goal:** embedded firmware, FPGA, hardware validation and design-verification roles.
**Method:** every circuit is simulated first, then built on real hardware, then documented here with expected vs measured results and the bugs I hit along the way.

---

## Progress

| # | Project | Concepts | Simulated | Built | Date |
|---|---------|----------|:---------:|:-----:|------|
| 01 | [NAND and AND gates](01-nand-and-gates/) | Logic gates, truth tables, 74xx pinouts | ✅ | ✅ | 2026-11-15 |
| 02 | [Half adder](02-half-adder/) | XOR + AND, binary addition | ✅ | ✅ | 2026-11-15 |
<!-- progress-end -->

**Coming next:** 2-to-1 multiplexer → full adder → 4-bit ripple-carry adder → flip-flops and counters → Verilog on FPGA.

---

## Tools

| Type | Tool |
|------|------|
| Simulation | [Tinkercad Circuits](https://www.tinkercad.com/circuits) |
| Hardware | Solderless breadboard, MB102 5 V power module, 74LS-series logic ICs, LEDs, 1 kΩ resistors |
| Measurement | Digital multimeter (KAIWEETS HT118A) |
| Automation | [`tools/add_build.py`](tools/add_build.py): creates each build's folder, resizes photos and generates the README |
| Coming next | Verilog (Icarus Verilog, GTKWave), Python, C, FPGA (Digilent Basys 3) |

---

## Repository structure

```
engineering-rebuild/
├── README.md                  ← this page
├── 01-nand-and-gates/         ← first logic gates on real hardware
├── 02-half-adder/             ← first arithmetic circuit
└── tools/
    └── add_build.py           ← script that scaffolds each new build
```

Each project folder contains a README with the design, wiring, expected vs measured results, and the bugs found along the way.

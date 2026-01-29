<!--
This file is used to generate your project datasheet.
Please fill in the information below and delete any unused sections.

You can also include images in this folder and reference them in the markdown.
Each image must be less than 512 kb in size, and the combined size of all images
must be less than 1 MB.
-->

## How it works

A D latch is a level-sensitive storage element that stores one bit of data.  
The latch has two primary inputs: a data input (D) and an enable signal (EN).

When the enable signal is asserted high, the latch becomes transparent and the
output Q follows the value of the data input D. When the enable signal is
deasserted low, the latch holds its previous output value, regardless of
changes on the data input.

An active-low reset signal (`rst_n`) is included in this design. When `rst_n` is
low, the output Q is forced to zero, clearing the stored state of the latch.

This behavior allows the D latch to be used as a basic memory element in digital
systems.

The functional behavior of the latch can be summarized as:
- If `rst_n = 0`, then `Q = 0`
- If `rst_n = 1` and `EN = 1`, then `Q = D`
- If `rst_n = 1` and `EN = 0`, then `Q` holds its previous value

---

## How to test

The design can be tested by applying different values to the D and EN inputs
while observing the output Q.

1. Assert the reset (`rst_n = 0`) and verify that Q is cleared to 0.
2. Deassert reset (`rst_n = 1`).
3. Set `EN = 1` and toggle `D`. The output Q should follow the value of D.
4. Set `EN = 0` and change `D`. The output Q should remain unchanged.
5. Reassert `EN = 1` and verify that Q updates to match D again.

The provided cocotb testbench applies these test cases and checks that the
output behaves as expected.

---

## External hardware

No external hardware is required for this project.

---

## Pin assignment

### Inputs
- `ui_in[0]` : D (Data input)
- `ui_in[1]` : EN (Enable)
- `rst_n`    : Active-low reset

### Outputs
- `uo_out[0]` : Q (Latch output)

Unused pins are left unconnected.

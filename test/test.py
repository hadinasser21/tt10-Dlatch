# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

def set_ui(dut, d, en):
    # ui_in[0]=D, ui_in[1]=EN
    dut.ui_in.value = ((en & 1) << 1) | ((d & 1) << 0)

def qbit(dut):
    return int(dut.uo_out.value) & 1

async def wait_q(dut, expected, timeout_us=800, step_ns=500):
    """Poll until Q matches expected or timeout (Icarus-safe, no callbacks)."""
    steps = int((timeout_us * 1000) / step_ns)  # us -> ns
    for _ in range(steps):
        if qbit(dut) == expected:
            return
        await Timer(step_ns, units="ns")
    raise AssertionError(
        f"Timeout waiting for Q={expected}. Final Q={qbit(dut)} uo_out={dut.uo_out.value} ui_in={dut.ui_in.value} rst_n={dut.rst_n.value}"
    )

@cocotb.test()
async def test_dlatch(dut):
    # Clock required by framework; latch doesn't use it functionally
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await Timer(100, units="us")
    dut.rst_n.value = 1
    await Timer(100, units="us")
    assert qbit(dut) == 0

    # --------- LATCH-SAFE STIMULUS (avoid EN/D changing together) ---------

    # 1) Prepare D=1 while latch is CLOSED (EN=0)
    set_ui(dut, d=1, en=0)
    await Timer(50, units="us")

    # 2) OPEN latch (EN=1) with D stable -> Q should eventually become 1
    set_ui(dut, d=1, en=1)
    await wait_q(dut, expected=1, timeout_us=900, step_ns=500)

    # 3) CLOSE latch (EN=0) while keeping D=1 stable
    set_ui(dut, d=1, en=0)
    await Timer(50, units="us")

    # 4) Now change D=0 while latch is CLOSED -> Q must HOLD 1
    set_ui(dut, d=0, en=0)
    await Timer(100, units="us")
    assert qbit(dut) == 1

    # 5) OPEN latch again with D=0 stable -> Q should eventually become 0
    set_ui(dut, d=0, en=1)
    await wait_q(dut, expected=0, timeout_us=900, step_ns=500)

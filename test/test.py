# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

def set_ui(dut, d, en):
    dut.ui_in.value = ((en & 1) << 1) | ((d & 1) << 0)

def qbit(dut):
    return int(dut.uo_out.value) & 1

async def wait_q(dut, expected, timeout_us=600, step_ns=100):
    """
    Poll uo_out[0] until it equals expected or timeout.
    Works even when RisingEdge callbacks are not supported by the simulator.
    """
    steps = int((timeout_us * 1000) / step_ns)  # us -> ns
    for _ in range(steps):
        if qbit(dut) == expected:
            return
        await Timer(step_ns, units="ns")
    raise AssertionError(f"Timeout waiting for Q={expected}. Final Q={qbit(dut)} uo_out={dut.uo_out.value}")

@cocotb.test()
async def test_dlatch(dut):
    # Clock required by framework, latch doesn't use it
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await Timer(50, units="us")
    dut.rst_n.value = 1
    await Timer(50, units="us")
    assert qbit(dut) == 0

    # EN=1, D=1 -> Q should become 1 (gate-level may take ~200us)
    set_ui(dut, d=1, en=1)
    await wait_q(dut, expected=1, timeout_us=600, step_ns=200)

    # EN=0, D=0 -> Q holds 1
    set_ui(dut, d=0, en=0)
    await Timer(50, units="us")
    assert qbit(dut) == 1

    # EN=1, D=0 -> Q should become 0
    set_ui(dut, d=0, en=1)
    await wait_q(dut, expected=0, timeout_us=600, step_ns=200)

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def set_ui(dut, d, en):
    # ui_in[0] = D, ui_in[1] = EN
    dut.ui_in.value = ((en & 1) << 1) | ((d & 1) << 0)

@cocotb.test()
async def test_dlatch(dut):
    # Start clock (even though latch doesn't need it, framework expects a clock)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset (give GL sim a bit more time)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)
    assert (int(dut.uo_out.value) & 1) == 0

    # EN=1, D=1 -> Q becomes 1
    set_ui(dut, d=1, en=1)
    await ClockCycles(dut.clk, 10)
    assert (int(dut.uo_out.value) & 1) == 1

    # EN=0, D=0 -> Q holds (stays 1)
    set_ui(dut, d=0, en=0)
    await ClockCycles(dut.clk, 10)
    assert (int(dut.uo_out.value) & 1) == 1

    # EN=1 again, D=0 -> Q updates to 0
    set_ui(dut, d=0, en=1)
    await ClockCycles(dut.clk, 10)
    assert (int(dut.uo_out.value) & 1) == 0

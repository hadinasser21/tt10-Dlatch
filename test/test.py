# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_dlatch(dut):
    # Start clock (even though latch doesn't need it, framework expects a clock)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out[0].value == 0

    # EN=1, D=1 -> Q becomes 1
    dut.ui_in[1].value = 1  # EN
    dut.ui_in[0].value = 1  # D
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out[0].value == 1

    # EN=0, D toggles -> Q holds (stays 1)
    dut.ui_in[1].value = 0  # EN
    dut.ui_in[0].value = 0  # D
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out[0].value == 1

    # EN=1 again, D=0 -> Q updates to 0
    dut.ui_in[1].value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out[0].value == 0


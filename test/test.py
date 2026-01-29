# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, with_timeout

def set_ui(dut, d, en):
    dut.ui_in.value = ((en & 1) << 1) | ((d & 1) << 0)

@cocotb.test()
async def test_dlatch(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await Timer(50, units="us")
    dut.rst_n.value = 1
    await Timer(50, units="us")
    assert (int(dut.uo_out.value) & 1) == 0

    # EN=1, D=1 → wait for real latch propagation
    set_ui(dut, d=1, en=1)
    await with_timeout(RisingEdge(dut.uo_out[0]), 500, "us")
    assert (int(dut.uo_out.value) & 1) == 1

    # EN=0, D=0 → Q holds
    set_ui(dut, d=0, en=0)
    await Timer(100, units="us")
    assert (int(dut.uo_out.value) & 1) == 1

    # EN=1, D=0 → Q updates low
    set_ui(dut, d=0, en=1)
    await Timer(200, units="us")
    assert (int(dut.uo_out.value) & 1) == 0

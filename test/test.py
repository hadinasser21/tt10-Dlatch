# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

def set_ui(dut, d, en):
    dut.ui_in.value = ((en & 1) << 1) | ((d & 1) << 0)

@cocotb.test()
async def test_dlatch(dut):
    # Clock is required by framework, but not functionally used
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await Timer(100, units="ns")

    dut.rst_n.value = 1
    await Timer(100, units="ns")
    assert (int(dut.uo_out.value) & 1) == 0

    # EN=1, D=1 → Q should update
    set_ui(dut, d=1, en=1)
    await Timer(100, units="ns")
    assert (int(dut.uo_out.value) & 1) == 1

    # EN=0, D=0 → Q should hold
    set_ui(dut, d=0, en=0)
    await Timer(100, units="ns")
    assert (int(dut.uo_out.value) & 1) == 1

    # EN=1, D=0 → Q updates
    set_ui(dut, d=0, en=1)
    await Timer(100, units="ns")
    assert (int(dut.uo_out.value) & 1) == 0

/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none
module tt_um_nasser_hadi_dlatch(
  input  wire [7:0] ui_in,
  output wire [7:0] uo_out,
  input  wire [7:0] uio_in,
  output wire [7:0] uio_out,
  output wire [7:0] uio_oe,
  input  wire       ena,
  input  wire       clk,
  input  wire       rst_n
);

  wire D  = ui_in[0];
  wire EN = ui_in[1];

  reg Q;

  // ✅ Intentional latch
  always_latch begin
    if (!rst_n)
      Q <= 1'b0;
    else if (EN)
      Q <= D;
    // else: holds previous Q (latch behavior)
  end

  assign uo_out[0]   = Q;
  assign uo_out[7:1] = 7'b0;

  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  wire _unused = &{ena, clk, ui_in[7:2], uio_in};

endmodule


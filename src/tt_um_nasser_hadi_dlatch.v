/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_nasser_hadi_dlatch (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (0=input, 1=output)
    input  wire       ena,       // always 1 when powered
    input  wire       clk,       // available but not required for a latch
    input  wire       rst_n       // active-low reset
);

    wire D  = ui_in[0];
    wire EN = ui_in[1];

    reg Q;

    // Level-sensitive D latch:
    // - when EN=1, Q follows D
    // - when EN=0, Q holds last value
    // - when rst_n=0, Q clears to 0
    always @(*) begin
        if (!rst_n)
            Q = 1'b0;
        else if (EN)
            Q = D;
        // else: no assignment -> latch holds
    end

    // Outputs
    assign uo_out[0] = Q;
    assign uo_out[7:1] = 7'b0;

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Prevent unused warnings (keep style consistent with manual)
    wire _unused = &{ena, clk, ui_in[7:2], uio_in};

endmodule

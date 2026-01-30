`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // ✅ Bit-level aliases for waveform visibility
  wire d_bit;
  wire en_bit;
  wire q_bit;

  assign d_bit  = ui_in[0];   // D input
  assign en_bit = ui_in[1];   // Enable
  assign q_bit  = uo_out[0];  // Q output

  // Dump the signals to a VCD file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.vcd");

    // dump everything (keeps existing behavior)
    $dumpvars(0, tb);

    // ✅ force single-bit signals into the VCD
    $dumpvars(1, d_bit);
    $dumpvars(1, en_bit);
    $dumpvars(1, q_bit);
    $dumpvars(1, clk);
    $dumpvars(1, rst_n);

    #1;
  end

  // Replace tt_um_example with your module name:
  tt_um_nasser_hadi_dlatch user_project (

`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path
      .ena    (ena),      // enable
      .clk    (clk),      // clock (not used by latch but required)
      .rst_n  (rst_n)     // active-low reset
  );

endmodule

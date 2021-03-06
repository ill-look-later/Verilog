module prng_parallel_tb;

	parameter CLK_PERIOD = 20;

   integer        file;

	reg            clk;
	reg            nRst;
   reg            update;
   reg            reseed;
   reg   [7:0]    seed;
   wire  [7:0]    rand;
   wire  [7:0]    rand8_1;
   wire  [31:0]   rand32;
	
   prng_parallel prng_parallel(
			`ifdef POST_SYNTHESIS
			.clk	      (clk        ),
			.nRst	      (nRst       ),
		   .update     (update     ),
         .reseed     (reseed     ),
         . \seed[7]  (seed[7]    ),
         . \seed[6]  (seed[6]    ),
         . \seed[5]  (seed[5]    ),
         . \seed[4]  (seed[4]    ),
         . \seed[3]  (seed[3]    ),
         . \seed[2]  (seed[2]    ),
         . \seed[1]  (seed[1]    ),
         . \seed[0]  (seed[0]    ),
         . \rand[7]  (rand[7]    ),
         . \rand[6]  (rand[6]    ),
         . \rand[5]  (rand[5]    ),
         . \rand[4]  (rand[4]    ),
         . \rand[3]  (rand[3]    ),
         . \rand[2]  (rand[2]    ),
         . \rand[1]  (rand[1]    ),
         . \rand[0]  (rand[0]    )
      `else
			.clk	      (clk        ),
			.nRst	      (nRst       ),
         .update     (update     ),
         .reseed     (reseed     ),
		   .seed       (seed       ),
         .rand       (rand       )
      `endif		
   );


   
   
   initial begin
		while(1) begin
			#(CLK_PERIOD/2) clk = 0;
			#(CLK_PERIOD/2) clk = 1;
		end	end

	initial begin
		`ifdef POST_SYNTHESIS
			$dumpfile("prng_parallel_syn.vcd");
			$dumpvars(0,prng_parallel_tb);
		`else
			$dumpfile("prng_parallel.vcd");
			$dumpvars(0,prng_parallel_tb);
		`endif
	end
      
   task plant;
      input [7:0] value;
      begin
         #1000    reseed   = 1;
         #1000    seed     = value;
         #100     reseed   = 0;
         #100000  reseed   = 0;
      end
   endtask

	initial begin
					update   = 1;
               nRst     = 1;
		#100		nRst     = 0;
		#100		nRst     = 1;
		         plant(8'h55);      
               plant(8'h66);      
               plant(8'h77);      
               plant(8'h00);      
               plant(8'hFF);      
               plant(8'h34);      
               plant(8'hAC);      
               plant(8'h34);    
               
               file = $fopen("prng_parallel.txt","w");
               repeat(100000) begin
                  @(posedge clk);
                   $fwrite(file,"%d\n",rand);
               end
               $fclose(file);

               update   = 0;      
               plant(8'h55);      
               plant(8'h12);      
               plant(8'h12);
               update   = 1;      
               plant(8'h12);      
               plant(8'h66);      
               plant(8'h77);
               $finish;
	end



endmodule

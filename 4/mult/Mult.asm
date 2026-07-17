// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.

// R3 = 1
// R2 = 0
// while R0 >= R3:
//   if R0 & R3:
//     R2 += R1
//   R1 += R1 
//   R3 += R3

// R3=1
@R3
M=1
// R2 = 0
@R2
M=0
// while R0 >= R3:
(LOOP)
@R0
D=M
@R3
D=D-M
@END
D;JLT
// if R0 & R3:
@R0
D=M
@R3
D=D&M
@INC
D;JEQ
// R2 += R1
@R1
D=M
@R2
M=D+M
(INC)
// R1 += R1
@R1
D=M
M=D+M
// R3 += R3
@R3
D=M
M=D+M
@LOOP
0;JMP
(END)
@END
0;JMP




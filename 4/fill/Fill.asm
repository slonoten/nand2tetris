// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

// R0 = SCREEN
// R1 = 0
// while True:
//   if KBD == 0:
//     if R1 != 0:
//       R1 == 0
//       R0 == SCREEN
//   else:
//     if R1 == 0:
//       R1 = -1
//       R0 == SCREEN
//   if R0 == KBD
//     R0 = SCREEN
//   RAM[R0] = R1

// R0 = SCREEN
@SCREEN
D=A
@R0
M=D
// R1 = 0
@R1
M=0
// while True:
(LOOP)
//   if KBD == 0:
@KBD
D=M
@KEYPRESSED
D;JNE
//     if R1 != 0:
@R1
D=M
@CHECK
D;JEQ
//       R1 == 0
@R1
M=0
//       R0 == SCREEN
@SCREEN
D=A
@R0
M=D
@CHECK
0;JMP
//   else:
(KEYPRESSED)
//     if R1 == 0:
@R1
D=M
@CHECK
D;JNE
//       R1 = -1
@R1
M=-1
//       R0 == SCREEN
@SCREEN
D=A
@R0
M=D
(CHECK)
//   if R0 == KBD # End of screen
@R0
D=M
@KBD
D=D-A
@WRITESCREEN
D;JNE
//     R0 = SCREEN
@SCREEN
D=A
@R0
M=D
(WRITESCREEN)
//   RAM[R0] = R1
@R1
D=M
@R0
A=M
M=D
// R0 += 1
@R0
M=M+1
@LOOP
0;JMP
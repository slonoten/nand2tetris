// Init SP
@256
D=A
@SP
M=D

// Init locals
@1024
D=A
@LCL
M=D

// Put 255 to local 3
@255
D=A
@1027
M=D

// push local 3
// local 3 -> D
@3
D=A
@LCL
A=D+M
D=M
// D -> [SP++]
@SP
A=M 
M=D
@SP
M=M+1

// Check
// [256] ==255
// [SP] == 257

// pop local 7
// target addr -> TMP
@7
D=A
@LCL
D=D+M
@TMP
M=D
// [--SP] -> D
@SP
M=M-1
A=M
D=M
// D -> local 7
@TMP
A=M
M=D
// Final loop
(END)
@END
0;JMP

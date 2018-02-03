go   0                  ; program to sum integers 1 to 10
0      ld   2 .count     ; r2 has value of counter
ldi  3 .vals     ; r3 points to first value
ldi  1 0       ; r1 contains sum
.loop  add  1 *3      ; r1 = r1 + next array value
inc  1
dec  2
bnz  2 .loop
sys  1 16
dw   0
.count dw   10
.vals  dw   1
dw   0
16     dw   0
end

	.data
	.text
	.globl main
	.ent main
main:	
	beq $0, $0, C0
C1:	
	li $v0, 11
	li $a0, '\n'
	syscall
	b, I0
C0:	
	addi $t1, $0, 1
	beq $t1, $0, C2
C3:	
	addi $a0, $0, 5
	li $v0, 1
	syscall
	b, I1
C2:	
	addi $a0, $0, 7
	li $v0, 1
	syscall
I1:	
I0:	
	addi $a0, $0, 9
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	.end main
For this lab, I am working with Mahmoud Khattab as my partner. I have prepared a solution for Question #3, while he has prepared solutions for Questions #1 and #2. I believe that this is a fair split of the work due to the fact that Question #3 is the most labour intensive. 

QUESTION #3

No, a recursive descent parser for the grammar stated in the question in not possible. This is because both of the productions from V start with the same non-terminal, I. 

V -> I
V -> I "[" E "]"

This does not make it clear which production to choose. These productions can be simplified to the following

V -> I [ "[" E "]" ]

This accepts the same language and will ensure that the parser always chooses the correct production. 

------------------------------------------------------------------------------------------------------------------

NOTE: The executable file that I have submitted (script.out) was compiled on Mills. However, if there is any problem running it, I have included in my submission the source file (script.c). Therefore, the executable could be easily recreated using 

gcc -o script.out script.c
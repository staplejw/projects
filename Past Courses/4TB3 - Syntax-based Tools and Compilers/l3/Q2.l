/*** Definition section ***/

%{
/* C code to be copied verbatim */
#include <stdio.h>
%}


%option noyywrap

%%
    /*** Rules section ***/


^.{256}.*$  {
    fprintf(stderr, "pathname too long\n");
}

^.*[^a-zA-Z0-9\.\/[:space:]]+.*$ {
    fprintf(stderr, "invalid character\n");
}

^.*[a-zA-Z0-9\.]{15}[a-zA-Z\.]*.*$ {
    fprintf(stderr, "component too long\n");
}


\/?[a-zA-Z0-9\.]{0,14}(\/[a-zA-Z0-9\.]{0,14})*\/?  {

    int err = 0; // keep track of error so we don't display reduced path if it is badly formed.
    //printf("Saw a path: %s\n", yytext);

    // Count the letter in the array
    int cnt = 0;
    while (yytext[cnt] != '\0'){
        cnt++;
    }
    cnt++; // extra char for null terminal
    char redPath[cnt]; // Will need at most cnt chars to build reduced path
    //printf("cnt: %d\n", cnt);
    

    int i = 0; // index for input string
    int j = 0; // index for output string being built
    
    int in_comp = 0; //track if we are in a component


    while (i < cnt){

        // Case it is a compononent delimiter
        if (yytext[i] == '/'){
            // If we're in a component or at the start, add a slash to reduced path
            if (in_comp || j == 0) redPath[j++] = '/';
            
            // Skip past consecutive slashes
            while (yytext[i] == '/'){
                i++;
            }
            in_comp = 0; // No longer in component

        } 
        // Case it is a letter
        else if ((yytext[i] >= 65 && yytext[i] <= 90) || (yytext[i] >= 97 && yytext[i] <= 122) || (yytext[i] >= 48 && yytext[i] <= 57)){
            in_comp = 1; //In a component now
            redPath[j++] = yytext[i++]; //Add char and move on

            
            
        }
        // Case it is a dot
        else if (yytext[i] == '.'){

            if (in_comp) redPath[j++] = yytext[i++]; //If we know we are already in component just add it

            // If ./ just move on
            else if (yytext[i+1] == '/' || yytext[i+1] == 0) i += 2; 

            // If next char is also a dot
            else if (yytext[i+1] == '.'){
                // Case ../
                if (yytext[i+2] == '/' || yytext[i+2] == 0){
                    if (j == 0){ // No previous component to back track.
                        fprintf(stderr, "malformed pathname\n");
                        err = 1;
                        break;
                    }else{
                        i += 3; // Move ahead in input string
                        while (j > 0){ // Back track to end of last component/beginning of string
                            j--;
                            if (j == 0) break;
                            if (redPath[j-1] == '/') break;
                        } 
                    }
                    
                }
                else{ //Otherwise, we are in a component
                    in_comp = 1;
                    redPath[j++] = yytext[i++];
                }
            }

            else{ // Otherwise, we are in a componenet
                in_comp = 1;
                redPath[j++] = yytext[i++];
            }
        }
        else if(yytext[i] == 0){ // Got to the end of the input string!
            redPath[j] = yytext[i++];
        }
   
    }

    if (!err){
        redPath[j] = 0; // Make sure string is null terminated
        if (j-1 > 0 && redPath[j-1] == '/') redPath[j-1] = 0; // Remove trailing slash
        printf("Reduced path: %s\n", redPath);
    }

}

.|\n    {   /* Ignore all other characters. */   }

%%
/*** C Code section ***/

int main(void)
{
    /* Call the lexer, then quit. */
    yylex();
    return 0;
}

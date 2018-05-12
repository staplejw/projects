#####################################################
# QUESTION 1:										#
#####################################################

My attribute grammar rules can be seen in the triple quote python comments in P0.py. Here are some notes about my modifications to the compiler.

- Selector: I have added attribute rules for this production and have changed the compiler accordingly.

- Factor: No changes made here.

- Term: I have added attribute rules for this production and have changed the compiler accordingly.

- SimpleExpression: I have added attribute rules for this production and have changed the compiler accordingly.

- Expression: I have added attribute rules for this production and have changed the compiler accordingly.

- CompoundStatement: No changes made here.

- Statement: To ensure that all statements start a new line, I have added a call to 'writeln' at the beginning of every rule for the statement producution. I have completed the attribute rules for all rules in this production and have changed the compiler accordingly.

- Type: I have added the parameter, l, as input for this function because it is possible for a type to have different levels of indentation. I have completed the attribute rules for all rules in this production and have changed the compiler accordingly.

- TypedIds: I have added the parameter, l, as input for this function because it is possible for typed ids to have different levels of indentation. I have completed the attribute rules for all rules in this production and have changed the compiler accordingly.

- Declarations: I have added the parameter, l, as input for this function because it is possible for declarations to have different levels of indentation. I have completed the attribute rules for all rules in this production and have changed the compiler accordingly.

#####################################################
# QUESTION 3:										#
#####################################################

I have modified the comment() method in SC.py so that when a comment is encountered, this method will write '{', then the comment characters, and then writes '}' to stdout. So, instead of the comments being ignored, they are just simply printed on the same line as they begin.

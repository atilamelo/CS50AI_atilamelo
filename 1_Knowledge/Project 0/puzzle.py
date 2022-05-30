from re import A
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Informations about the game 
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    #Informations about the problem
    Or(And(AKnight, AKnave), AKnave),

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

knowledge1 = And(
    # Informations about the game 

    # A can be a knight or a knave, but not both 
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B can be a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Information about the problem 

    # The sentence is true or A is a Knave
    Or(And(AKnave, BKnave), AKnave),
    # If A is a Knave, so the afirmation about B is false, therefore B is a Knight
    Implication(AKnave, BKnight) 

)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# A is a knave, B is a Knight

knowledge2 = And(
    #### Informations about the game #### 

    # A can be a knight or a knave, but not both 
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B can be a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    #### Information about the problem ####

    # "We are the same kind", if this affirmation is false, so A is a Knave
    Or(
        Or(And(AKnight, BKnight), And(AKnave, BKnave)), # Or both are knight, or both are knave
        AKnave # Or this afirmattion is True
    ),

    # "We are of different kind", if this is false, so B is a Knave
    Or(
        Or(And(AKnight, BKnave), And(AKnave, BKnight)), # Or A is a Knight and B is a Knave, or A is a Knave and B is a Knight
        BKnight # Or this afirmattion is True
    )    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. 
# Comment: A is possibily a knight
# B says "A said 'I am a knave'."
# Comment: B is a Knave
# B says "C is a knave."
# Comment: C is not a knave, because B is a Knight. So C is a Knight
# C says "A is a knight."
# Comment: C is right, A is a Knight, so C too is a knight.

# A is a Knight
# B is a Knave
# c is a Knight

knowledge3 = And(
    #### Informations about the game #### 

    # A can be a knight or a knave, but not both 
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B can be a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # C can be a knight or a knave, but not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    #### Informations about the problem ####

    # A says either "I am a knight." or "I am a knave.", but you don't know which. 
    Or(Or(AKnave, AKnight), AKnave),
    Not(And(Or(AKnave, AKnight), AKnave)), # Both informations cannot be true

    # All afirmations are true, or B is a Knave
    Or(
        And(
            # B says "A said 'I am a knave'."
            Or(AKnave, BKnave),
            Not(And(AKnave, BKnave)), # But not both
            # B says "C is a knave."
            Or(CKnave, BKnave),
            Not(And(CKnave, BKnave)) # But not both
        ),
        BKnave
    ),

    # C says "A is a knight."
    Or(AKnight, CKnave),
    Not(And(AKnight, CKnave))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

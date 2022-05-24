# Regular Expression / DFA Construction

This project takes in a regular expression with certain operations, generates a DFA for that expression, and allows the user to see if strings match the regular expression. If `r` and `s` are both regular expressions, then so are the following:

- `(rs)`
- `(r + s)`
- `(r)*`

where `(rs)` is the concatenation of `r` and `s`, `(r + s)` is the union of `r` and `s`, and `(r)*` is the Kleene closure of `r`. Without parenthesis, the `*` operator has the highest precedence, the concatenation operator the next level of precedence, and the `+` the lowest level of precedence. `^` represents an empty regular expression.

## Usage

First, copy the repository to your own machine. Instructions for cloning the repository can be found at [Github's documented instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

Once you are in the directory containing the files you may need to run `pip install -r requirements.txt` to install the required [(Python Lex-Yacc)](https://www.dabeaz.com/ply/) package.

To execute the program you can run `python3 RE.py` which provide a prompt `REGEX:` where you can enter a regular expression using the above rules that is terminated by the `;` character.

Examples of valid responses include `(a+b)*aa(a+b)*;` and `(42)*(abc);`. If you don't wish to enter a regular expression and wish to terminate the program you can type `exit;` at the prompt.

Once you have entered a valid regular expression you will be provided with another prompt `INPUT STRING:` where you can enter a string to be matched that is terminated by the `;` character. If the input string matches the regular expression then `MATCH` will be displayed on screen, otherwise `NO MATCH` will be displayed. If you wish to stop matching input strings you can type `exit;` at the prompt to be taken back to the `REGEX:` prompt where you can enter another regular expression or type `exit;` again to terminate the program.

Optionally, you can execute the program with `python3 RE.py -dfa` which will display the [Deterministic Finite Automata](https://en.wikipedia.org/wiki/Deterministic_finite_automaton) that was generated for your request.

## Sample

```text
python3 RE.py
REGEX: (a+b)*aa(a+b)*;
  INPUT STRING: aa;
  MATCH
  INPUT STRING: ababababab;
  NO MATCH
  INPUT STRING: abaabbabbb;
  MATCH
  INPUT STRING: bb;
  NO MATCH
  INPUT STRING: exit;
REGEX: exit;
```

```text
python3 RE.py -dfa
REGEX: (a+b)*aa(a+b)*;
start_state({1, 2, 3})
delta({1, 2, 3},a,{1, 2, 3, 4})
delta({1, 2, 3},b,{1, 2, 3})
delta({1, 2, 3, 4},a,{1, 2, 3, 4, 5, 6, 7})
delta({1, 2, 3, 4},b,{1, 2, 3})
delta({1, 2, 3, 4, 5, 6, 7},a,{1, 2, 3, 4, 5, 6, 7})
delta({1, 2, 3, 4, 5, 6, 7},b,{1, 2, 3, 5, 6, 7})
delta({1, 2, 3, 5, 6, 7},a,{1, 2, 3, 4, 5, 6, 7})
delta({1, 2, 3, 5, 6, 7},b,{1, 2, 3, 5, 6, 7})
final_state({1, 2, 3, 4, 5, 6, 7})
final_state({1, 2, 3, 5, 6, 7})
  INPUT STRING: abab;
  NO MATCH
  INPUT STRING: abaabb;
  MATCH
  INPUT STRING: exit
REGEX: exit;
```

import re
from uuid import uuid4

def pattern_handler(source: str) -> str:
    """
    ## Anonimous Functions
    Create anonimous functions similar to JavaScript.

    ### Examples
    ```py
    (param1, ...) => 
        x = do_something(param1)
        x * 2 # <- last expression is returned (unless it ends with ";")
        ; # <- this indicates the end of the function

    # You can also have 1 line functions
    (param1, ...) => x = do_something(param1);  # <- as long as it ends with ";"
    ```
    """

    pattern: re.Pattern = re.compile(
        r"""
        \(                      # Function Arguments Start Parenthesis
        ([a-zA-Z0-9,_\s]*)      # Function Arguments
        \)                      # Function Arguments End Parenthesis
        \s?                     # Optional Whitespace
        =>                      # Arrow token (only used for sintax)
        \s?                     
        ([-!$%^&*()_+|~=`\[\]:";'<>?,.\/a-zA-Z0-9\s]+) # function Body
        ;                       # End of function Body
        """,
        re.VERBOSE
    ) 

    for match in pattern.finditer(source):

        params, func_content = match.groups()
        s, e = match.start(),  match.end()

        if not params or not func_content:
            continue

        # fo cases when a comma get into function content
        func_end = ""

        func_content = func_content.strip()

        if "," in func_content:
            func_content, *func_end = func_content.split(",", maxsplit=1)
            func_end.insert(0, ",")

            func_end = "".join(func_end)

        # func creation
        func_name = "__func_" + str(uuid4())[4:12].replace("-", "")

        func = f'def {func_name}({params}):\n\t'

        func_sentences  = [*map(lambda x: x.strip(), func_content.split("\n"))]

        if len(func_sentences) == 1:
            func += f"return {func_sentences[0]}"

        else:
            # if last sentence is doesnt end with ";" add return
            if not func_sentences[-1].endswith(";"):
                func_sentences[-1] = "return " + func_sentences[-1]

            func += "\n\t".join(func_sentences)

        # replace sintax with func name
        source = source[:s] + func_name + func_end + source[e:]

        # append func at source (this happens after because start and end world change)
        source = func + "\n" + source

    return source

from parsimonious.grammar import Grammar, NodeVisitor

# \lx headword (starts Entry)
# \va variant 1 (starts Variant in Entry)
# \va variant 2 (ends 1st Variant and starts 2nd Variant in Entry)
# \ve variant comment
# \ps part of speech 1 (ends 2nd Variant & starts Sense in Entry)
# \ge English gloss 1
# \xv Vernacular example 1 (starts Example in Sense)
# \xe English translation 1
# \xv Vernacular example 2 (ends 1st Example & starts 2nd Example in Sense)
# \xe English translation 2
# \de English definition 1
# \ps part of speech 2 (ends 2nd Example & 1st Sense & starts 2nd Sense in Entry)
# \ge English gloss 2
# \de English definition 2
# \se subentry 1 (ends 2nd Sense & starts Subentry in Entry)
# \ps part of speech 3 (starts Sense in Subentry)
# \ge English gloss 3
# \se subentry 2 (ends Sense and 1st Subentry & starts 2nd Subentry in Entry)
# \ps part of speech 4 (starts Sense in 2nd Subentry)
# \ge English gloss 4
# \dt date modified (ends Sense & 2nd Subentry & falls back to Entry since dates are only allowed in Entry)

# \lx earth # headword (starts Entry)
# \ps v. n. # part of speech 1 (starts Sense in Entry)
# \gv സമ്പാദിക്കുക # Vernacular gloss 1
# \ps  # part of speech 2 (ends 1st Sense & starts 2nd Sense in Entry)
# \gv നേടുക # Vernacular gloss 2
# \ps  # part of speech 3 (ends 2nd Sense & starts 3rd Sense in Entry)
# \gv തേടിക്കൊള്ളുക # Vernacular gloss 3
# \se earth # subentry 1 (ends 2nd Sense & starts Subentry in Entry)
# \ps  # part of speech 4 (starts Sense in Subentry)
# \gv ദേഹണ്ഡിച്ചുണ്ടാക്കുക # Vernacular gloss 4
# \se earth # subentry 2 (ends Sense and 1st Subentry & starts 2nd Subentry in Entry)
# \ps  # part of speech 5 (starts Sense in 2nd Subentry)
# \gv കൂലികിട്ടുക # Vernacular gloss 5
# \dt 29/6/2019 # date modified (ends Sense & 2nd Subentry & falls back to Entry since dates are only allowed in Entry)

# Earth, v. n. സമ്പാദിക്കുന്നു, നെടുന്നു, തെടിക്കൊള്ളുന്നു; ദേഹണ്ഡിച്ചുണ്ടാക്കുന്നു; കൂലികിട്ടുന്നു

# [
#     {
#         "lx": "earth",
#         "dt": "2019-06-29",
#         "senses":
#         [
#             {
#                 "ps": "v. n.",
#                 "gv": "സമ്പാദിക്കുക",
#             },
#             {
#                 "ps": "v. n.",
#                 "gv": "നേടുക",
#             },            
#             {
#                 "ps": "v. n.",
#                 "gv": "തേടിക്കൊള്ളുക",
#             },            
#         ],
#         "se":
#         [
#             {
#                 "senses":
#                 [
#                     {
#                         "ps": "v. n.",
#                         "gv": "ദേഹണ്ഡിച്ചുണ്ടാക്കുക",
#                     },            
#                 ],
#             },
#             {
#                 "senses":
#                 [
#                     {
#                         "ps": "v. n.",
#                         "gv": "കൂലികിട്ടുക",
#                     },            
#                 ],
#             },
#         ]
#     },
# ]

data = """
A, art. ഒരു
Aback, ad. പുറകൊട്ട, പിന്നൊക്കം
Abaft, ad. പിമ്പുറത്തെക്ക, കപ്പലിൻറ അമരത്തെക്ക
Abandon, v. a. വിട്ടൊഴിയുന്നു, ത്യജിക്കുന്നു, പരിത്യാഗം ചെയ്യുന്നു; ഉപെക്ഷിക്കുന്നു, കൈവിടുന്നു
Abandoned, a. വിട്ടൊഴിയപ്പെട്ട,ത്യജിക്കപ്പെട്ട; ഉപെക്ഷിക്കപ്പെട്ട, കൈവിടപ്പെട്ട; മഹാ കെട്ട, ദുഷ്ടതയുള്ള, വഷളായുള്ള, മഹാ ചീത്ത
Abandonment, s. വിട്ടൊഴിവ, പരിത്യാഗം; ഉപെക്ഷണം, കൈവെടിച്ചിൽ
"""


grammar = Grammar(
    r"""
    expr       = (entry / emptyline )*
    entry      = headword comma pos ws senses subentry* emptyline
    headword   = ~"[A-Z 0-9]*"i
    pos        = (ws ~"[a-z]+\.")+
    senses     = (sense comma)* sense
    subentry   = semicolon ws senses
    sense      = (ml ws ml)* ml
    ml         = ~"[\u0d00-\u0d7f]*"
    semicolon  = ~";"
    comma      = ~","
    ws         = ~"\s*"
    emptyline  = ws+
    """
)

class DictVisitor(NodeVisitor):

    def visit_expr(self, node, visited_children):
        """ Returns the overall output. """
        output = []
        for child in visited_children:
            if type(child[0]) == dict:
                output.append(child[0])

        return output
    
    def visit_entry(self, node, visited_children):
        """ Returns the overall output. """
        output = {"lx": visited_children[0]}
        return output

    def visit_headword(self, node, visited_children):
        return node.text
    
    def visit_sense(self, node, visited_children):
        pass

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node
        
def main():
    tree = grammar.parse(data)
    dv = DictVisitor()
    output = dv.visit(tree)
    print(output)

if __name__ == "__main__":
    main()

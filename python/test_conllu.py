from InputProcessing.Parsers import CoNLLU
import re


def tokenizeRegex( txt: str, sent_regex: re.Pattern, regex: re.Pattern) -> list[str]:
    """
    Tokenise la chaîne de caractères à l'aide d'une expression régulière.
    """

    sents = sent_regex.findall(txt)

    return [[tok for tok in regex.findall(sentence.strip().replace('\n', ' ')) if tok != ''] for sentence in sents]

grm = re.compile(r"""
(?:etc\.|p\.ex\.|cf\.|M\.|MM\.) |
(\w+['’]? |
\- |
[^\s\w]+ |
\n) 
""", flags=re.X)

grm_sents = re.compile(r"""
.*?[\.\?!]+
""", flags=re.X | re.U | re.S)

"""conllu = CoNLLU()

with open(r"D:\documents\COURS\Master IDL\M1\S2\Programmation Web et base de données pour le TAL\TEST CORPORA\corpus 3\test.conllu", mode="r", encoding="utf-8") as f:
    content = f.read()


doc = conllu.parse(content, "test.txt")


print()"""


with open(r"D:\documents\COURS\Master IDL\M1\S2\Programmation Web et base de données pour le TAL\TEST CORPORA\corpus 3\contes_bruns_balzac.txt", 
          mode="r", encoding="utf-8") as f:
    ct = f.read()

    sentences = tokenizeRegex(ct, grm_sents, grm)
    output = ""

    for i, sent in enumerate(sentences, 1):

        print(f"phrase {i} / {len(sentences)}")

        if len(sent) != 0:

            output += "# sent_id = " + str(i) + '\n'

            for j, tok in enumerate(sent, 1):
                output += str(j) + '\t' + tok + "\t_\t_\t_\t_\t_\t_\t_\t_" + '\n'

            output += '\n'


    with open(r"D:\documents\COURS\Master IDL\M1\S2\Programmation Web et base de données pour le TAL\TEST CORPORA\corpus 3\contes_bruns_balzac.conllu", 
              mode="w", encoding="utf-8") as f:
        f.write(output)

    print("Done! :)")
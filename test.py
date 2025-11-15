from backend.rag_engine import ask
questions = [
    "Quels sont les droits garantis aux femmes en Tunisie ?",
    "Quelles libertés fondamentales sont protégées ?",
    "Comment se déroule le divorce selon la loi ?",
    "Quel est le rôle du président de la République ?",
    "Comment les lois sont votées ?",
    "Quels sont les droits des enfants ?",
    "comment on peut candidater a  la poste de president de la republique?"
]

for q in questions:
    print("\n❓", q)
    print(ask(q))
    print("\n" + "="*80 + "\n")
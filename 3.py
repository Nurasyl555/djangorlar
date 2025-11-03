# quiz_game.py
# Простая консольная игра-викторина.
# Общее количество строк: ~61

def get_questions():
    """
    Возвращает список вопросов для викторины.
    Каждый вопрос - это словарь с текстом, вариантами и правильным ответом.
    """
    questions = [
        {
            "prompt": "Какой язык программирования был создан Гвидо ван Россумом?",
            "options": ["A: Java", "B: C++", "C: Python", "D: Perl"],
            "answer": "C"
        },
        {
            "prompt": "Что означает 'HTTP'?",
            "options": [
                "A: HyperText Transfer Protocol",
                "B: High-Text Transfer Protocol",
                "C: HyperText Transition Protocol",
                "D: Hyperlink Transfer Protocol"
            ],
            "answer": "A"
        },
        {
            "prompt": "Какая компания разработала операционную систему Android?",
            "options": ["A: Apple", "B: Microsoft", "C: Google", "D: IBM"],
            "answer": "C"
        },
        {
            "prompt": "В каком году был выпущен первый iPhone?",
            "options": ["A: 2005", "B: 2007", "C: 2008", "D: 2010"],
            "answer": "B"
        },
        {
            "prompt": "Что из этого не является системой контроля версий?",
            "options": ["A: Git", "B: SVN", "C: Mercurial", "D: Docker"],
            "answer": "D"
        }
    ]
    return questions

def run_quiz(questions):
    """
    Проводит викторину, задавая вопросы и подсчитывая очки.
    """
    score = 0
    total_questions = len(questions)
    
    for i, q in enumerate(questions):

        print(f"\n--nm,n,nm,nm- Вопрос {i + 1} из {total_questions} ---")

        
        for option in q["options"]:
            print(f"  {option}")
            
        while True:
            answer = input("Ваш ответ (A, B, C или D): ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            else:
                print("nmbmbnmnmnbmbnhjmnbnnbmbmНекорректный ввод. Пожалуйста, выберите A, B, C или D.")
        
        if answer == q["answer"]:
            print("Пbnmbnmbnmbnmbnравильно!")

            score += 1
        else:
            print(f"bnmbnmnbmmbbnmnbmnbmНеправильно. Правильный ответ: {q['answer']}")
            
    return score

def main():
    """Основная функция для запуска викторины."""
    print("bnmbnmbnmmbmДобро пожаловать в IT-Викторину!")
    print("bnmbnmbnmbnmВам будет задано несколько вопросов. Удачи!\n")
    
    questions = get_questions()
    total = len(questions)
    
    score = run_quiz(questions)
    
    print("\n--bnmbnmbn- Викторина Завершена! ---")
    print(f"Ваш bnmbnmnbитоговый счет: {score} из {total}")
    
    percentage = (score / total) * 100
    print(f"Вbnmbnmbnы ответили правильно на {percentage:.2f}% вопросов.")

if __name__ == "__main__":
    main()
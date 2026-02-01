"""
Класс с вопросами викторины
"""


class Question:
    """Класс для представления одного вопроса"""
    
    def __init__(self, question_text: str, options: list, correct_answer: int, image_url: str):
        """
        Инициализация вопроса
        
        Args:
            question_text: Текст вопроса
            options: Список вариантов ответов
            correct_answer: Индекс правильного ответа (0-based)
            image_url: URL или путь к изображению
        """
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
        self.image_url = image_url
    
    def is_correct(self, answer_index: int) -> bool:
        """Проверить, правильный ли ответ"""
        return answer_index == self.correct_answer
    
    def get_correct_answer_text(self) -> str:
        """Получить текст правильного ответа"""
        return self.options[self.correct_answer]


class QuizQuestions:
    """Класс с набором вопросов викторины"""
    
    def __init__(self):
        """Инициализация вопросов викторины"""
        self.questions = [
            Question(
                question_text="Какая планета является самой большой в Солнечной системе?",
                options=["Земля", "Юпитер", "Сатурн", "Марс"],
                correct_answer=1,
                image_url="https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=800"
            ),
            Question(
                question_text="Сколько континентов на Земле?",
                options=["5", "6", "7", "8"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800"
            ),
            Question(
                question_text="Какое животное изображено на логотипе WWF?",
                options=["Тигр", "Слон", "Панда", "Лев"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=800"
            ),
            Question(
                question_text="В каком году был запущен первый искусственный спутник Земли?",
                options=["1955", "1957", "1960", "1965"],
                correct_answer=1,
                image_url="https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=800"
            ),
            Question(
                question_text="Какой язык программирования использует логотип со змеей?",
                options=["Java", "JavaScript", "Python", "Ruby"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800"
            ),
            Question(
                question_text="Сколько струн у классической гитары?",
                options=["4", "5", "6", "7"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800"
            ),
            Question(
                question_text="Какой элемент обозначается символом Au в периодической таблице?",
                options=["Серебро", "Золото", "Алюминий", "Медь"],
                correct_answer=1,
                image_url="https://images.unsplash.com/photo-1610375461246-83df859d849d?w=800"
            ),
            Question(
                question_text="В каком году была построена Эйфелева башня?",
                options=["1887", "1889", "1891", "1895"],
                correct_answer=1,
                image_url="https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=800"
            ),
            Question(
                question_text="Какая самая длинная река в мире?",
                options=["Нил", "Амазонка", "Янцзы", "Миссисипи"],
                correct_answer=0,
                image_url="https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800"
            ),
            Question(
                question_text="Сколько клеток на шахматной доске?",
                options=["32", "48", "64", "81"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=800"
            ),
            Question(
                question_text="Какой газ составляет большую часть атмосферы Земли?",
                options=["Кислород", "Углекислый газ", "Азот", "Водород"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800"
            ),
            Question(
                question_text="В каком году был основан Google?",
                options=["1996", "1998", "2000", "2002"],
                correct_answer=1,
                image_url="https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=800"
            ),
            Question(
                question_text="Сколько костей в теле взрослого человека?",
                options=["186", "206", "226", "246"],
                correct_answer=1,
                image_url="https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=800"
            ),
            Question(
                question_text="Какая страна подарила США Статую Свободы?",
                options=["Великобритания", "Испания", "Франция", "Италия"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1508962914676-134849a727f0?w=800"
            ),
            Question(
                question_text="Какая скорость света в вакууме (приблизительно)?",
                options=["100,000 км/с", "200,000 км/с", "300,000 км/с", "400,000 км/с"],
                correct_answer=2,
                image_url="https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800"
            ),
        ]
    
    def get_question(self, index: int) -> Question:
        """Получить вопрос по индексу"""
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
    
    def get_total_questions(self) -> int:
        """Получить общее количество вопросов"""
        return len(self.questions)

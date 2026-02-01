"""
Класс для управления данными пользователей
"""


class UserStats:
    """Класс для хранения статистики пользователя"""
    
    def __init__(self, user_id: int):
        """
        Инициализация статистики пользователя
        
        Args:
            user_id: ID пользователя в Telegram
        """
        self.user_id = user_id
        self.current_question = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.quiz_completed = False
    
    def reset(self):
        """Сбросить статистику пользователя"""
        self.current_question = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.quiz_completed = False
    
    def add_correct_answer(self):
        """Добавить правильный ответ"""
        self.correct_answers += 1
    
    def add_wrong_answer(self):
        """Добавить неправильный ответ"""
        self.wrong_answers += 1
    
    def next_question(self):
        """Перейти к следующему вопросу"""
        self.current_question += 1
    
    def get_total_answers(self) -> int:
        """Получить общее количество ответов"""
        return self.correct_answers + self.wrong_answers
    
    def get_percentage(self) -> float:
        """Получить процент правильных ответов"""
        total = self.get_total_answers()
        if total == 0:
            return 0.0
        return round((self.correct_answers / total) * 100, 2)
    
    def mark_as_completed(self):
        """Отметить викторину как завершенную"""
        self.quiz_completed = True


class UserManager:
    """Класс для управления пользователями"""
    
    def __init__(self):
        """Инициализация менеджера пользователей"""
        self.users = {}
    
    def get_or_create_user(self, user_id: int) -> UserStats:
        """
        Получить или создать пользователя
        
        Args:
            user_id: ID пользователя в Telegram
            
        Returns:
            UserStats: Объект статистики пользователя
        """
        if user_id not in self.users:
            self.users[user_id] = UserStats(user_id)
        return self.users[user_id]
    
    def reset_user(self, user_id: int):
        """
        Сбросить статистику пользователя
        
        Args:
            user_id: ID пользователя в Telegram
        """
        user = self.get_or_create_user(user_id)
        user.reset()
    
    def record_answer(self, user_id: int, is_correct: bool):
        """
        Записать ответ пользователя
        
        Args:
            user_id: ID пользователя в Telegram
            is_correct: Правильный ли ответ
        """
        user = self.get_or_create_user(user_id)
        if is_correct:
            user.add_correct_answer()
        else:
            user.add_wrong_answer()
        user.next_question()
    
    def get_user_stats(self, user_id: int) -> UserStats:
        """
        Получить статистику пользователя
        
        Args:
            user_id: ID пользователя в Telegram
            
        Returns:
            UserStats: Объект статистики пользователя
        """
        return self.get_or_create_user(user_id)
    
    def is_quiz_completed(self, user_id: int, total_questions: int) -> bool:
        """
        Проверить, завершена ли викторина
        
        Args:
            user_id: ID пользователя в Telegram
            total_questions: Общее количество вопросов
            
        Returns:
            bool: True если викторина завершена
        """
        user = self.get_or_create_user(user_id)
        return user.current_question >= total_questions

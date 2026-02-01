# 🎨 Кастомизация и расширение бота

## 📝 Как добавить свои вопросы

### Изменение существующих вопросов

Откройте файл `questions.py` и измените вопросы в списке `self.questions`:

```python
Question(
    question_text="Ваш вопрос здесь?",
    options=["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
    correct_answer=0,  # Индекс правильного ответа (0 = первый вариант)
    image_url="https://ссылка-на-картинку.jpg"
)
```

### Добавление новых вопросов

Просто добавьте новый объект `Question` в список:

```python
self.questions = [
    # Существующие вопросы...
    
    # Ваш новый вопрос
    Question(
        question_text="Столица России?",
        options=["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"],
        correct_answer=0,
        image_url="https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800"
    ),
]
```

## 🖼️ Работа с изображениями

### Способ 1: Использование URL (текущий)

```python
image_url="https://images.unsplash.com/photo-123456?w=800"
```

**Плюсы:**
- Не занимает место на диске
- Легко менять

**Минусы:**
- Требует интернет
- Может перестать работать, если ссылка устареет

### Способ 2: Локальные файлы

1. Создайте папку `images` в корне проекта
2. Поместите туда изображения (q1.jpg, q2.jpg и т.д.)
3. Измените в `questions.py`:

```python
image_url="images/q1.jpg"
```

### Способ 3: Telegram File ID (самый быстрый)

После того как картинка загружена в Telegram один раз, можно использовать её file_id:

```python
image_url="AgACAgIAAxkBAAIC..."  # File ID из Telegram
```

## 🎯 Изменение количества вопросов

Если хотите больше или меньше 15 вопросов:

1. **Откройте `config.py`**
2. **Измените константу:**

```python
TOTAL_QUESTIONS = 20  # Вместо 15
```

3. **Добавьте соответствующее количество вопросов в `questions.py`**

## 💬 Кастомизация сообщений

Все сообщения бота находятся в `config.py`. Вы можете изменить их:

```python
WELCOME_MESSAGE = """
🎮 Ваше приветственное сообщение здесь!

Любой текст, который вы хотите показать пользователю.
"""

CORRECT_ANSWER = "🎉 Молодец! Это правильный ответ!"
WRONG_ANSWER = "😢 Увы, это неправильно. Правильный ответ: {correct}"
```

## 🏆 Добавление рейтинговой системы

### Шаг 1: Модифицируйте `user_manager.py`

Добавьте метод для сохранения лучшего результата:

```python
class UserStats:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_question = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.quiz_completed = False
        self.best_score = 0  # Новое поле
    
    def update_best_score(self):
        """Обновить лучший результат"""
        current_percentage = self.get_percentage()
        if current_percentage > self.best_score:
            self.best_score = current_percentage
            return True
        return False
```

### Шаг 2: Модифицируйте `quiz_manager.py`

Добавьте отображение лучшего результата:

```python
async def send_final_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    user_stats = self.user_manager.get_user_stats(user_id)
    percentage = user_stats.get_percentage()
    
    # Проверяем, улучшил ли пользователь свой рекорд
    is_new_record = user_stats.update_best_score()
    
    message = self.config.FINAL_STATS_MESSAGE.format(
        correct=user_stats.correct_answers,
        wrong=user_stats.wrong_answers,
        total=self.config.TOTAL_QUESTIONS,
        percentage=percentage,
        result_comment=self.config.get_result_comment(percentage)
    )
    
    if is_new_record:
        message += "\n\n🏆 Новый личный рекорд!"
    else:
        message += f"\n\n📊 Ваш лучший результат: {user_stats.best_score}%"
    
    # ... остальной код
```

## 🎮 Добавление таймера на вопросы

### Модификация `quiz_manager.py`:

```python
import asyncio

async def send_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    # ... существующий код отправки вопроса ...
    
    # Добавляем таймер (например, 30 секунд)
    context.user_data['question_time'] = asyncio.get_event_loop().time()

async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем время ответа
    if 'question_time' in context.user_data:
        elapsed_time = asyncio.get_event_loop().time() - context.user_data['question_time']
        
        if elapsed_time > 30:  # 30 секунд
            await query.answer("⏰ Время вышло!")
            # Засчитываем как неправильный ответ
            is_correct = False
        else:
            # ... обычная проверка ответа ...
```

## 📊 Сохранение статистики в файл

### Добавьте в `user_manager.py`:

```python
import json
import os

class UserManager:
    def __init__(self):
        self.users = {}
        self.stats_file = "user_stats.json"
        self.load_stats()
    
    def load_stats(self):
        """Загрузить статистику из файла"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, stats_data in data.items():
                        user = UserStats(int(user_id))
                        user.correct_answers = stats_data.get('correct_answers', 0)
                        user.wrong_answers = stats_data.get('wrong_answers', 0)
                        user.best_score = stats_data.get('best_score', 0)
                        self.users[int(user_id)] = user
            except Exception as e:
                print(f"Ошибка загрузки статистики: {e}")
    
    def save_stats(self):
        """Сохранить статистику в файл"""
        data = {}
        for user_id, user in self.users.items():
            data[user_id] = {
                'correct_answers': user.correct_answers,
                'wrong_answers': user.wrong_answers,
                'best_score': user.best_score
            }
        
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения статистики: {e}")
```

Вызывайте `save_stats()` после каждой викторины.

## 🌟 Добавление уровней сложности

### Модифицируйте `questions.py`:

```python
class Question:
    def __init__(self, question_text: str, options: list, correct_answer: int, 
                 image_url: str, difficulty: str = "medium"):
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
        self.image_url = image_url
        self.difficulty = difficulty  # easy, medium, hard

class QuizQuestions:
    def __init__(self):
        self.questions = {
            'easy': [],
            'medium': [],
            'hard': []
        }
        self._init_questions()
    
    def _init_questions(self):
        # Легкие вопросы
        self.questions['easy'].append(
            Question(
                question_text="Сколько дней в неделе?",
                options=["5", "6", "7", "8"],
                correct_answer=2,
                image_url="...",
                difficulty="easy"
            )
        )
        
        # Средние вопросы
        self.questions['medium'].append(
            Question(
                question_text="Какая планета самая большая?",
                options=["Земля", "Юпитер", "Сатурн", "Марс"],
                correct_answer=1,
                image_url="...",
                difficulty="medium"
            )
        )
        
        # Сложные вопросы
        self.questions['hard'].append(
            Question(
                question_text="В каком году изобретен транзистор?",
                options=["1945", "1947", "1950", "1952"],
                correct_answer=1,
                image_url="...",
                difficulty="hard"
            )
        )
```

## 🎨 Добавление кнопки "Поделиться результатами"

### Модифицируйте `quiz_manager.py`:

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def send_final_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    # ... код отправки результатов ...
    
    # Создаем кнопку для шеринга
    share_text = f"Я прошел викторину и набрал {percentage}% правильных ответов!"
    share_url = f"https://t.me/share/url?url=https://t.me/your_bot_name&text={share_text}"
    
    keyboard = [
        [InlineKeyboardButton("📤 Поделиться результатом", url=share_url)],
        [InlineKeyboardButton("🔄 Пройти еще раз", callback_data="restart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.message.reply_text(message, reply_markup=reply_markup)
```

## 🏅 Добавление достижений (achievements)

### Создайте новый файл `achievements.py`:

```python
class Achievement:
    def __init__(self, name: str, description: str, condition):
        self.name = name
        self.description = description
        self.condition = condition

class AchievementManager:
    def __init__(self):
        self.achievements = [
            Achievement(
                "Первые шаги", 
                "Ответить правильно на 5 вопросов",
                lambda stats: stats.correct_answers >= 5
            ),
            Achievement(
                "Эксперт", 
                "Набрать 80% правильных ответов",
                lambda stats: stats.get_percentage() >= 80
            ),
            Achievement(
                "Перфекционист", 
                "Ответить правильно на все вопросы",
                lambda stats: stats.get_percentage() == 100
            ),
        ]
    
    def check_achievements(self, user_stats):
        """Проверить, какие достижения получил пользователь"""
        earned = []
        for achievement in self.achievements:
            if achievement.condition(user_stats):
                earned.append(achievement)
        return earned
```

## 📱 Добавление inline-режима

Позволяет пользователям использовать бота в любом чате.

### Добавьте в `bot.py`:

```python
from telegram import InlineQueryResultArticle, InputTextMessageContent

async def inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик inline-запросов"""
    query = update.inline_query.query
    
    if not query:
        return
    
    results = [
        InlineQueryResultArticle(
            id="1",
            title="Начать викторину",
            input_message_content=InputTextMessageContent(
                "Нажмите /start чтобы начать викторину!"
            ),
            description="Проверьте свои знания!"
        )
    ]
    
    await update.inline_query.answer(results)

# В register_handlers добавьте:
from telegram.ext import InlineQueryHandler
self.application.add_handler(InlineQueryHandler(self.inline_query))
```

Не забудьте включить inline-режим в BotFather командой `/setinline`.

## 🎉 Готово!

Теперь у вас есть полноценный бот с возможностью кастомизации!

**Полезные ссылки:**
- [Документация Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot примеры](https://docs.python-telegram-bot.org/en/stable/examples.html)

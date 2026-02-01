"""
Класс для управления логикой викторины
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Config
from questions import QuizQuestions
from user_manager import UserManager


class QuizManager:
    """Класс для управления викториной"""
    
    def __init__(self):
        """Инициализация менеджера викторины"""
        self.questions = QuizQuestions()
        self.user_manager = UserManager()
        self.config = Config()
    
    async def send_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """
        Отправить вопрос пользователю
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
            user_id: ID пользователя
        """
        user_stats = self.user_manager.get_user_stats(user_id)
        current_q = user_stats.current_question
        
        # Проверяем, не закончилась ли викторина
        if self.user_manager.is_quiz_completed(user_id, self.config.TOTAL_QUESTIONS):
            await self.send_final_results(update, context, user_id)
            return
        
        # Получаем текущий вопрос
        question = self.questions.get_question(current_q)
        
        if question is None:
            await update.message.reply_text("❌ Ошибка: вопрос не найден!")
            return
        
        # Формируем клавиатуру с вариантами ответов
        keyboard = []
        for i, option in enumerate(question.options):
            # Создаем callback_data в формате "answer_индекс"
            callback_data = f"answer_{i}"
            keyboard.append([InlineKeyboardButton(option, callback_data=callback_data)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Формируем текст сообщения
        question_text = f"❓ Вопрос {current_q + 1} из {self.config.TOTAL_QUESTIONS}\n\n"
        question_text += f"{question.question_text}"
        
        # Пытаемся отправить фото с вопросом
        try:
            if update.callback_query:
                await update.callback_query.message.reply_photo(
                    photo=question.image_url,
                    caption=question_text,
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_photo(
                    photo=question.image_url,
                    caption=question_text,
                    reply_markup=reply_markup
                )
        except Exception as e:
            # Если не удалось отправить фото, отправляем только текст
            print(f"Ошибка при отправке фото: {e}")
            if update.callback_query:
                await update.callback_query.message.reply_text(
                    text=question_text,
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(
                    text=question_text,
                    reply_markup=reply_markup
                )
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработать ответ пользователя
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user_stats = self.user_manager.get_user_stats(user_id)
        
        # Получаем индекс ответа из callback_data
        answer_index = int(query.data.split('_')[1])
        
        # Получаем текущий вопрос
        question = self.questions.get_question(user_stats.current_question)
        
        # Проверяем ответ
        is_correct = question.is_correct(answer_index)
        
        # Записываем ответ
        self.user_manager.record_answer(user_id, is_correct)
        
        # Формируем сообщение с результатом
        if is_correct:
            result_message = self.config.CORRECT_ANSWER
        else:
            result_message = self.config.WRONG_ANSWER.format(
                correct=question.get_correct_answer_text()
            )
        
        # Отправляем результат
        await query.edit_message_caption(
            caption=f"{query.message.caption}\n\n{result_message}"
        )
        
        # Отправляем следующий вопрос или результаты
        if self.user_manager.is_quiz_completed(user_id, self.config.TOTAL_QUESTIONS):
            await self.send_final_results(update, context, user_id)
        else:
            await self.send_question(update, context, user_id)
    
    async def send_final_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """
        Отправить финальные результаты
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
            user_id: ID пользователя
        """
        user_stats = self.user_manager.get_user_stats(user_id)
        percentage = user_stats.get_percentage()
        
        message = self.config.FINAL_STATS_MESSAGE.format(
            correct=user_stats.correct_answers,
            wrong=user_stats.wrong_answers,
            total=self.config.TOTAL_QUESTIONS,
            percentage=percentage,
            result_comment=self.config.get_result_comment(percentage)
        )
        
        # Отмечаем викторину как завершенную
        user_stats.mark_as_completed()
        
        if update.callback_query:
            await update.callback_query.message.reply_text(message)
        else:
            await update.message.reply_text(message)
    
    async def send_current_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """
        Отправить текущую статистику
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
            user_id: ID пользователя
        """
        user_stats = self.user_manager.get_user_stats(user_id)
        
        if user_stats.get_total_answers() == 0:
            await update.message.reply_text(
                "📊 У вас пока нет статистики. Начните викторину командой /start"
            )
            return
        
        percentage = user_stats.get_percentage()
        
        message = self.config.STATS_MESSAGE.format(
            correct=user_stats.correct_answers,
            wrong=user_stats.wrong_answers,
            total=user_stats.get_total_answers(),
            percentage=percentage,
            result_comment=self.config.get_result_comment(percentage)
        )
        
        await update.message.reply_text(message)
    
    def restart_quiz(self, user_id: int):
        """
        Перезапустить викторину для пользователя
        
        Args:
            user_id: ID пользователя
        """
        self.user_manager.reset_user(user_id)

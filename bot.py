"""
Главный файл Telegram-бота с викториной
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import Config
from quiz_manager import QuizManager


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class QuizBot:
    """Класс Telegram-бота с викториной"""
    
    def __init__(self):
        """Инициализация бота"""
        self.config = Config()
        self.quiz_manager = QuizManager()
        self.application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        # Регистрация обработчиков команд
        self.register_handlers()
    
    def register_handlers(self):
        """Регистрация обработчиков команд и callback"""
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("restart", self.restart_command))
        
        # Callback для ответов на вопросы
        self.application.add_handler(CallbackQueryHandler(self.handle_answer, pattern="^answer_"))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик команды /start
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        logger.info(f"User {user_id} ({user_name}) started the quiz")
        
        # Сбрасываем статистику пользователя
        self.quiz_manager.restart_quiz(user_id)
        
        # Отправляем приветственное сообщение
        welcome_text = f"👋 Привет, {user_name}!\n\n{self.config.WELCOME_MESSAGE}"
        await update.message.reply_text(welcome_text)
        
        # Начинаем викторину
        await update.message.reply_text(self.config.START_QUIZ_MESSAGE)
        await self.quiz_manager.send_question(update, context, user_id)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик команды /help
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        logger.info(f"User {update.effective_user.id} requested help")
        await update.message.reply_text(self.config.HELP_MESSAGE)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик команды /stats
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested stats")
        await self.quiz_manager.send_current_stats(update, context, user_id)
    
    async def restart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик команды /restart
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        user_id = update.effective_user.id
        logger.info(f"User {user_id} restarted the quiz")
        
        # Сбрасываем статистику
        self.quiz_manager.restart_quiz(user_id)
        
        await update.message.reply_text("🔄 Викторина перезапущена!\n\n" + self.config.START_QUIZ_MESSAGE)
        await self.quiz_manager.send_question(update, context, user_id)
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик ответов на вопросы
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        user_id = update.effective_user.id
        logger.info(f"User {user_id} answered question")
        await self.quiz_manager.handle_answer(update, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработчик ошибок
        
        Args:
            update: Объект обновления от Telegram
            context: Контекст бота
        """
        logger.error(f"Update {update} caused error {context.error}")
    
    def run(self):
        """Запуск бота"""
        logger.info("Starting bot...")
        
        # Добавляем обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        # Запускаем бота
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Главная функция"""
    try:
        bot = QuizBot()
        bot.run()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Ошибка конфигурации: {e}")
        print("\n📝 Создайте файл .env и добавьте в него:")
        print("BOT_TOKEN=your_bot_token_here")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Критическая ошибка: {e}")


if __name__ == '__main__':
    main()

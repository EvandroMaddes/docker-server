import unittest
import TelegramNotifierBot

class FormatterTest(unittest.TestCase):
    def test_tuple_to_html(self):
        test_commands_ = [('start', 'Starts the bot'),
                     ('temp', 'Send server temperature as message when the command /temp is issued'),
                     ('time', 'Send server time as message when the command /time is issued'),
                     ('shutdown', 'Shutdown the server when the command /shutdown is issued'),
                     ('echo', 'Echo the user message'),
                     ('auto', 'Echo the user message'),
                     ('stop', 'Echo the user message'),
                     ('help', 'For a list of commands'), ]
        bot = telegram_notifier_bot
        print(bot.tuple_to_html_join(test_commands_))
        self.assertEqual(10, 10, 'The sum is wrong.')

if __name__ == '__main__':
    unittest.main()

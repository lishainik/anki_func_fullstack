import random
import sys
import time
from typing import Dict, Tuple

STOP_WORD = 'СТОП'


def load_words(filename: str = 'words.txt') -> Dict[str, str]:
    """Загружает пары слов и переводов из файла.

    Args:
        filename: Имя файла со словарём.

    Returns:
        Словарь, содержащий слова и их переводы.
    """
    dictionary = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    continue
                key, value = parts[0].strip(), parts[1].strip()
                dictionary[key] = value
    except FileNotFoundError:
        print(f'Файл {filename} не найден.')
        sys.exit(1)

    return dictionary


def print_statistics(score: int, total_time: float):
    """Выводит статистику игры.

    Args:
        score: Количество правильных ответов.
        total_time: Общее время игры в секундах, округленное до двух знаков.
    """
    if score > 0:
        average_time = total_time / score
        average_time_message = f'{average_time:.2f} сек.'
    else:
        average_time_message = '—'

    print(
        f'Ваш итоговый счет: {score}\n'
        f'Время игры: {total_time:.2f} секунд '
        f'(среднее время: {average_time_message})\n'
    )


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """Запрашивает перевод слова и проверяет ответ.

    Args:
        word: Слово, для которого требуется перевод.
        correct: Правильный перевод слова.

    Returns:
        Кортеж из трёх значений:
        признак команды STOP,
        результат проверки ответа,
        время ответа в секундах.
    """
    print(f'Переведите слово: {word}')

    start_time = time.time()

    answer = input('Ваш ответ: ')

    if answer.strip().upper() == STOP_WORD:
        return True, False, 0.0

    answer_time = time.time() - start_time

    is_correct = answer.strip().lower() == correct.strip().lower()

    return False, is_correct, answer_time


def play_game(words: Dict[str, str], stop_on_mistake: bool = False):
    """Запускает игровой цикл.

    Args:
        words: Словарь слов и их переводов.
        stop_on_mistake: Завершать игру после первой ошибки.
    """
    if not words:
        print('Словарь пуст. Добавьте слова перед началом игры.')
        return

    total_time = 0
    score = 0
    answer_count = 0

    key_list = list(words.keys())

    while True:
        random.shuffle(key_list)

        for random_key in key_list:
            correct_answer = words[random_key]

            is_stop, is_correct, answer_time = ask_and_check(
                random_key,
                correct_answer,
            )

            if is_stop:
                if stop_on_mistake:
                    print('Выход из режима по запросу пользователя.')
                print_statistics(score, total_time)
                return

            total_time += answer_time
            answer_count += 1

            if is_correct:
                score += 1
                print(f'Верно! Время ответа: {answer_time:.2f} секунд')
            else:
                print(f'Ошибка! Неверно. Правильный ответ: {correct_answer}.')
                print_statistics(score, total_time)

                if stop_on_mistake:
                    return


def start_game(words: Dict[str, str]):
    """Запускает игру с текущим словарём.

    Args:
        words: Словарь слов и их переводов.
    """
    print('Начинаем игру! Чтобы закончить, введите СТОП')
    play_game(words)


def train_until_mistake(words: Dict[str, str]):
    """Запускает тренировку до первой ошибки.

    Args:
        words: Словарь слов и их переводов.
    """
    print('Режим: Игра до первой ошибки! Чтобы выйти вручную, введите СТОП')
    play_game(words, stop_on_mistake=True)


def add_words(words: Dict[str, str]):
    """Добавляет новые слова и их переводы в словарь.

    Args:
        words: Словарь слов и их переводов.
    """
    print('Чтобы закончить, введите СТОП')

    while True:
        input_word = input('Введите слово: ').strip()

        if input_word.upper() == STOP_WORD:
            break

        if not input_word:
            print('Слово не может быть пустым. Попробуйте ещё раз.')
            continue

        existing_word = next(
            (key for key in words.keys() if key.lower() == input_word.lower()),
            None,
        )

        if existing_word:
            print(
                f'Слово "{input_word}" уже существует. '
                f'Перевод будет обновлен. '
                f'Старый перевод: "{words[existing_word]}"'
            )

        input_translation = input('Введите перевод: ').strip()

        if input_translation.upper() == STOP_WORD:
            break

        words[input_word.strip()] = input_translation.strip()


def show_all_words(words: Dict[str, str]):
    """Выводит все слова и их переводы из словаря.

    Args:
        words: Словарь слов и их переводов.
    """
    all_words = []

    for key, value in words.items():
        all_words.append(f'{key} - {value}')

    print('; '.join(all_words))


def save_words(words: Dict[str, str], filename: str = 'words.txt'):
    """Сохраняет слова в текстовый файл.

    Args:
        words: Словарь слов и их переводов.
        filename: Путь к файлу.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for key, value in words.items():
                file.write(f'{key},{value}\n')

        print(f'Было сохранено {len(words)} слов в файл {filename}')

    except Exception as e:
        print(f'Ошибка при сохранении слов: {e}')


def main():
    """Главная функция программы."""
    words = load_words()
    print(f'Было загружено {len(words)} слов из файла words.txt')

    while True:
        menu = '''Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        '''
        print(menu)
        menu_choice = input('Пункт меню: ')

        if menu_choice == '1':
            start_game(words)

        elif menu_choice == '2':
            add_words(words)

        elif menu_choice == '3':
            train_until_mistake(words)

        elif menu_choice == '4':
            show_all_words(words)

        elif menu_choice == '5':
            save_words(words)
            print('До скорого!')
            sys.exit()

        else:
            print('Неизвестный пункт меню')


if __name__ == '__main__':
    main()

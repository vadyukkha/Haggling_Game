import os
import asyncio
import subprocess
import shutil
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

async def run_game(game_path: str, folder_name: str, message: types.Message):
    try:
        terminal_process = await asyncio.create_subprocess_shell("/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cd_command = f"cd {game_path}"
        terminal_process.stdin.write(cd_command.encode() + b'\n')
        await terminal_process.stdin.drain()

        start_game_command = "./game"
        terminal_process.stdin.write(start_game_command.encode() + b'\n')
        await terminal_process.stdin.drain()

        await asyncio.sleep(5) 

        bd_file_path = f'../Game/bd/result_{folder_name}.txt'
        user_folder_path = f'../Game/Users/{folder_name}'

        if os.path.exists(bd_file_path):
            document = FSInputFile(bd_file_path)
            await bot.send_document(message.chat.id, document)
            await message.reply("Для запуска игры снова, используй старт и повторяй действия\n")
            os.remove(bd_file_path)
            os.remove("../Game/src/teamname.txt")
        else:
            await message.reply("Файл результатов не найден")

        if os.path.exists(user_folder_path):
            shutil.rmtree(user_folder_path)


    except Exception as e:
        print(f"Ошибка при запуске терминала или выполнении команды: {e}")
        

class Form(StatesGroup):
    folder_name = State()
    cpp_file = State()

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.folder_name)
    await message.reply(f"Привет! Перед началом рекомендую ознакомиться с некоторыми тонкостями работы программы.\n"
                        "Используй функцию в файле следующим образом:\n\n"
                        "#ifdef _WIN32 \n"
                        "#define EXPORT __declspec(dllexport) \n"
                        "#else \n"
                        '#define EXPORT __attribute__((visibility("default"))) \n'
                        "#endif \n"
                        "\n"
                        'extern "C" EXPORT int decide(int turn, int cost_hat, int cost_book, int cost_ball, int count_hat, int count_book, int count_ball)\n\n'
                        "Затем отправляй мне название своего файл\n"
                        "Название файла должно обязательно совпадать с тем, что вы введете.")


@router.message(Form.folder_name)
async def process_folder_name(message: types.Message, state: FSMContext):
    folder_name = message.text
    await state.update_data(folder_name=folder_name)
    
    folder_path = os.path.join("../Game/Users", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    await message.reply(f'Теперь отправьте мне cpp файл')

    game_cpp_path = os.path.join("../Game/src", "teamname.txt")
    with open(game_cpp_path, 'w') as game_file:
        game_file.write(f"{folder_name}")

    await state.set_state(Form.cpp_file)

@router.message(Form.cpp_file)
async def process_cpp_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    folder_name = data['folder_name']
    folder_path = os.path.join("../Game/Users", folder_name)

    cpp_file = message.document
    file_name = cpp_file.file_name

    if not file_name.endswith('.cpp'):
        await message.reply("Отправьте файл с расширением .cpp")
        return

    file_path = os.path.join(folder_path, file_name)
    await bot.download(cpp_file, file_path)

    await message.reply(f'Файл "{file_name}" сохранен. Скоро скину вам результаты вашей стратегии против ботов')

    try:
        # Компиляция файла в библиотеку .dylib
        dylib_name = file_name.replace('.cpp', '.dylib')
        dylib_path = os.path.join(folder_path, dylib_name)
        compile_command = [
            "g++",
            "-shared",
            "-o", dylib_path,
            file_path,
            "-std=c++20"
        ]
        subprocess.run(compile_command, check=True)
        
        game_path = os.path.join("../Game/src", "game.cpp")
        game_executable_path = os.path.join("../Game/src", "game")
        compile_game_command = [
            "g++",
            "-o", game_executable_path,
            game_path,
            "-ldl",
            "-std=c++20"
        ]
        subprocess.run(compile_game_command, check=True)

        await run_game("../Game/src", folder_name, message)

    except subprocess.CalledProcessError as e:
        await message.reply(f'Ошибка компиляции файла "{file_name}": {e}')
    
    await state.clear()

dp.include_router(router)

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())

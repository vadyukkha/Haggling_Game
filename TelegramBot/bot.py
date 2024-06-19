import os
import asyncio
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

class Form(StatesGroup):
    folder_name = State()
    cpp_file = State()

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.folder_name)
    await message.reply("Привет! Введите название команды")

@router.message(Form.folder_name)
async def process_folder_name(message: types.Message, state: FSMContext):
    folder_name = message.text
    await state.update_data(folder_name=folder_name)
    
    folder_path = os.path.join("../Users", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    await message.reply(f'Команда "{folder_name}" добавлена. Теперь отправьте мне cpp файл')

    await state.set_state(Form.cpp_file)

@router.message(Form.cpp_file)
async def process_cpp_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    folder_name = data['folder_name']
    folder_path = os.path.join("../Users", folder_name)

    cpp_file = message.document
    file_name = cpp_file.file_name

    if not file_name.endswith('.cpp'):
        await message.reply("Отправьте файл с расширением .cpp")
        return

    file_path = os.path.join(folder_path, file_name)
    await bot.download(cpp_file, file_path)

    await message.reply(f'Файл "{file_name}" сохранен')

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
    except subprocess.CalledProcessError as e:
        await message.reply(f'Ошибка компиляции файла "{file_name}": {e}')
    
    await state.clear()

dp.include_router(router)

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())

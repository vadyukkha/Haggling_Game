#!/bin/bash

# Компилируем game
echo "Compiling game..."
g++ -o game game.cpp -ldl -std=c++20

# Проверяем успешность компиляции game
if [ $? -ne 0 ]; then
    echo "Error: Compilation of game failed."
    exit 1
fi

echo "Compilation of game successful."

# Запускаем игру
echo "Running game..."
./game

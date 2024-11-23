#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "game.hpp"
#include "board.hpp"
#include "move.hpp"
#include <memory>
#include <windows.h>
#include <iostream>
#include <fstream>

// Додаємо функцію логування
void log_error(const char* message) {
    std::ofstream log_file("hasami_shogi_error.log", std::ios::app);
    if (log_file.is_open()) {
        log_file << message << std::endl;
        log_file.close();
    }
}

extern "C" {
    // Додаємо функцію ініціалізації DLL
    BOOL APIENTRY DllMain(HANDLE hModule, DWORD reason, LPVOID lpReserved) {
        switch (reason) {
            case DLL_PROCESS_ATTACH:
                log_error("DLL_PROCESS_ATTACH");
                break;
            case DLL_PROCESS_DETACH:
                log_error("DLL_PROCESS_DETACH");
                break;
        }
        return TRUE;
    }
}

// Решта коду залишається тим самим...
using namespace hasami_shogi;

// Global game instance
static std::unique_ptr<Game> game_instance;

// Error handling helper
static void set_error(const char* message) {
    PyErr_SetString(PyExc_RuntimeError, message);
}

static PyObject* create_game(PyObject* self, PyObject* args) {
    try {
        int mode;
        if (!PyArg_ParseTuple(args, "i", &mode)) {
            set_error("Invalid arguments for create_game");
            return NULL;
        }
        
        game_instance = std::make_unique<Game>(static_cast<Game::GameMode>(mode));
        Py_RETURN_NONE;
    }
    catch (const std::exception& e) {
        set_error(e.what());
        return NULL;
    }
}

static PyObject* make_move(PyObject* self, PyObject* args) {
    try {
        if (!game_instance) {
            set_error("Game not initialized");
            return NULL;
        }

        int fromRow, fromCol, toRow, toCol;
        if (!PyArg_ParseTuple(args, "iiii", &fromRow, &fromCol, &toRow, &toCol)) {
            set_error("Invalid arguments for make_move");
            return NULL;
        }
        
        Move move(fromRow, fromCol, toRow, toCol);
        bool result = game_instance->makeMove(move);
        
        return PyBool_FromLong(result);
    }
    catch (const std::exception& e) {
        set_error(e.what());
        return NULL;
    }
}

static PyObject* get_current_player(PyObject* self, PyObject* args) {
    try {
        if (!game_instance) {
            set_error("Game not initialized");
            return NULL;
        }
        
        int player = static_cast<int>(game_instance->getCurrentPlayer());
        return PyLong_FromLong(player);
    }
    catch (const std::exception& e) {
        set_error(e.what());
        return NULL;
    }
}

static PyObject* get_board_state(PyObject* self, PyObject* args) {
    try {
        if (!game_instance) {
            set_error("Game not initialized");
            return NULL;
        }

        const Board& board = game_instance->getBoard();
        PyObject* list = PyList_New(9);
        
        for (int i = 0; i < 9; i++) {
            PyObject* row = PyList_New(9);
            for (int j = 0; j < 9; j++) {
                int piece = static_cast<int>(board.getPiece(i, j));
                PyObject* value = PyLong_FromLong(piece);
                PyList_SET_ITEM(row, j, value);
            }
            PyList_SET_ITEM(list, i, row);
        }
        
        return list;
    }
    catch (const std::exception& e) {
        set_error(e.what());
        return NULL;
    }
}

static PyObject* undo_move(PyObject* self, PyObject* args) {
    try {
        if (!game_instance) {
            set_error("Game not initialized");
            return NULL;
        }
        
        bool result = game_instance->undoLastMove();
        return PyBool_FromLong(result);
    }
    catch (const std::exception& e) {
        set_error(e.what());
        return NULL;
    }
}

static PyMethodDef HasamiShogiMethods[] = {
    {"create_game", create_game, METH_VARARGS, "Create a new game instance"},
    {"make_move", make_move, METH_VARARGS, "Make a move"},
    {"get_current_player", get_current_player, METH_VARARGS, "Get current player"},
    {"get_board_state", get_board_state, METH_VARARGS, "Get board state"},
    {"undo_move", undo_move, METH_VARARGS, "Undo last move"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hasami_shogi_module = {
    PyModuleDef_HEAD_INIT,
    "hasami_shogi",
    "Hasami Shogi game module",
    -1,
    HasamiShogiMethods
};

PyMODINIT_FUNC PyInit_hasami_shogi(void) {
    try {
        PyObject* m = PyModule_Create(&hasami_shogi_module);
        if (m == NULL) {
            return NULL;
        }
        
        // Add constants to the module
        PyModule_AddIntConstant(m, "PLAYER_BLACK", 0);
        PyModule_AddIntConstant(m, "PLAYER_WHITE", 1);
        PyModule_AddIntConstant(m, "GAME_MODE_PVP", 0);
        PyModule_AddIntConstant(m, "GAME_MODE_AI_EASY", 1);
        PyModule_AddIntConstant(m, "GAME_MODE_AI_MEDIUM", 2);
        PyModule_AddIntConstant(m, "GAME_MODE_AI_HARD", 3);
        
        return m;
    }
    catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}
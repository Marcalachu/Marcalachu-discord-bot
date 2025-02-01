import discord
from discord.ext import commands
import random
import asyncio
import json

# Configuración del bot

intents = discord.Intents.default()
intents.message_content = True  # Habilitar el intent de contenido de mensajes
intents.reactions = True  # Habilitar el uso de reacciones
bot = commands.Bot(command_prefix='!', intents=intents)

# Variables para el juego Snake
snake_body = []
food_position = (0, 0)
snake_direction = "RIGHT"
snake_game_active = False
snake_players = 0  # Contador de jugadores en Snake

# Variables para el juego Akinator
akinator_questions = [
    "¿Es un personaje real?",
    "¿Es un personaje de una película?",
    "¿Es un superhéroe?",
    "¿Es un personaje de un videojuego?",
    "¿Es un personaje de una serie de televisión?"
]
akinator_players = 0  # Contador de jugadores en Akinator

# Creador del bot
creator = "Marcalachu"  # Nombre del creador del bot

# Cargar el árbol de decisiones desde un archivo JSON
def load_decision_tree():
    try:
        with open('decision_tree.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Crear árbol de decisiones inicial en caso de fallo
        return {
            "¿Es un personaje real?": {
                "sí": {
                    "¿Es un científico?": {
                        "sí": {
                            "¿Es conocido por su trabajo en física?": {
                                "sí": "Albert Einstein",
                                "no": "Marie Curie"
                            }
                        },
                        "no": {
                            "¿Es un político?": {
                                "sí": {
                                    "¿Es un presidente?": {
                                        "sí": "Barack Obama",
                                        "no": "Angela Merkel"
                                    }
                                },
                                "no": {
                                    "¿Es un youtuber?": {
                                        "sí": {
                                            "¿Es un gamer?": {
                                                "sí": "PewDiePie",
                                                "no": "Lilly Singh"
                                            }
                                        },
                                        "no": "Elon Musk"
                                    }
                                }
                            }
                        }
                    },
                    "¿Es un artista?": {
                        "sí": {
                            "¿Es un músico?": {
                                "sí": {
                                    "¿Es un cantante de rock?": {
                                        "sí": "Freddie Mercury",
                                        "no": "Beyoncé"
                                    }
                                },
                                "no": "Pablo Picasso"
                            }
                        },
                        "no": {
                            "¿Es un escritor?": {
                                "sí": {
                                    "¿Es conocido por novelas de ciencia ficción?": {
                                        "sí": "Isaac Asimov",
                                        "no": "Gabriel García Márquez"
                                    }
                                },
                                "no": {
                                    "¿Es un director de cine?": {
                                        "sí": "Steven Spielberg",
                                        "no": "J.K. Rowling"
                                    }
                                }
                            }
                        }
                    }
                },
                "no": {
                    "¿Es un superhéroe?": {
                        "sí": {
                            "¿Es de Marvel?": {
                                "sí": {
                                    "¿Es parte de los Vengadores?": {
                                        "sí": "Iron Man",
                                        "no": "Deadpool"
                                    }
                                },
                                "no": "Batman"
                            }
                        },
                        "no": {
                            "¿Es un personaje de dibujos animados?": {
                                "sí": {
                                    "¿Es de Disney?": {
                                        "sí": "Mickey Mouse",
                                        "no": "Bugs Bunny"
                                    }
                                },
                                "no": "Shrek"
                            }
                        }
                    },
                    "¿Es un personaje de videojuegos?": {
                        "sí": {
                            "¿Es un personaje de Nintendo?": {
                                "sí": "Mario",
                                "no": "Master Chief"
                            }
                        },
                        "no": {
                            "¿Es un personaje de libros?": {
                                "sí": {
                                    "¿Es de Harry Potter?": {
                                        "sí": "Harry Potter",
                                        "no": "Frodo Baggins"
                                    }
                                },
                                "no": "Sherlock Holmes"
                            }
                        }
                    }
                }
            },
            "¿Es un personaje de ficción?": {
                "sí": {
                    "¿Es un personaje de una serie de televisión?": {
                        "sí": {
                            "¿Es un personaje principal?": {
                                "sí": "Walter White",
                                "no": "Jim Halpert"
                            }
                        },
                        "no": {
                            "¿Es un personaje de una película?": {
                                "sí": {
                                    "¿Es un villano?": {
                                        "sí": "Darth Vader",
                                        "no": "Harry Potter"
                                    }
                                },
                                "no": "Gandalf"
                            }
                        }
                    },
                    "¿Es un personaje de un libro?": {
                        "sí": {
                            "¿Es de una novela clásica?": {
                                "sí": "Elizabeth Bennet",
                                "no": "Katniss Everdeen"
                            }
                        },
                        "no": {
                            "¿Es un personaje de un videojuego?": {
                                "sí": {
                                    "¿Es un personaje de acción?": {
                                        "sí": "Lara Croft",
                                        "no": "Kirby"
                                    }
                                },
                                "no": "SpongeBob SquarePants"
                            }
                        }
                    }
                },
                "no": {
                    "¿Es un animal?": {
                        "sí": {
                            "¿Es un animal doméstico?": {
                                "sí": "Perro",
                                "no": "Elefante"
                            }
                        }
                    }
                }
            }
        }



        # Guardar el árbol de decisiones
def save_decision_tree(tree):
            with open('decision_tree.json', 'w') as f:
                json.dump(tree, f)

        # Comando para jugar Akinator
@bot.command()
async def akinator(ctx):
            decision_tree = load_decision_tree()
            await ctx.send("¡Comencemos a jugar Akinator! Piensa en un personaje y yo intentaré adivinarlo.")

            current_node = decision_tree

            while isinstance(current_node, dict):
                for question, answers in current_node.items():
                    await ctx.send(question)
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    try:
                        response = await bot.wait_for('message', check=check, timeout=15.0)
                        response = response.content.lower()

                        if response in ["sí", "si", "yes", "y"]:
                            current_node = answers["sí"]
                        elif response in ["no", "n", "nope"]:
                            current_node = answers["no"]
                        else:
                            await ctx.send("Por favor, responde con 'sí' o 'no'.")
                            continue
                    except asyncio.TimeoutError:
                        await ctx.send("¡Tiempo agotado! El juego ha terminado.")
                        return

            # Adivinar el personaje
            guessed_character = current_node
            await ctx.send(f"¡Creo que el personaje en el que pensabas es {guessed_character}!")

            # Confirmar si el personaje es correcto
            await ctx.send("¿Es correcto? (sí/no)")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await bot.wait_for('message', check=check, timeout=15.0)
                if response.content.lower() in ["sí", "si", "yes", "y"]:
                    await ctx.send("¡Genial! Me alegra haber adivinado correctamente.")
                elif response.content.lower() in ["no", "n", "nope"]:
                    # Aquí se capturan y actualizan nuevas respuestas
                    await ctx.send("¡Oh no! ¿Cuál era el personaje?")
                    new_character = await bot.wait_for('message', check=check, timeout=15.0)
                    await ctx.send("¿Qué pregunta podría ayudarme a adivinarlo?")
                    new_question = await bot.wait_for('message', check=check, timeout=15.0)

                    # Actualizar el árbol de decisiones
                    decision_tree[new_question.content] = {
                        "sí": new_character.content,
                        "no": guessed_character
                    }
                    save_decision_tree(decision_tree)
                    await ctx.send("¡Gracias! He aprendido algo nuevo.")
                else:
                    await ctx.send("No entendí tu respuesta. Por favor, responde 'sí' o 'no'.")
            except asyncio.TimeoutError:
                await ctx.send("¡Tiempo agotado! El juego ha terminado.")

     # Variables globales para el juego Snake
snake_body = []
food_position = (0, 0)
snake_direction = "RIGHT"
snake_game_active = False
def render_board():
                 board = ""
                 for y in range(10):
                     for x in range(10):
                         if (x, y) == snake_body[0]:  # La cabeza de la serpiente
                             board += "👤"  # Emoji para la cabeza
                         elif (x, y) in snake_body:
                             board += "🐍"  # Emoji para el cuerpo
                         elif (x, y) == food_position:
                             board += "🍏"  # Emoji para la comida
                         else:
                             board += "⬜"  # Emoji para el espacio vacío
                     board += "\n"
                 return board

def update_snake_position():
                 global snake_body, food_position, snake_game_active
                 head_x, head_y = snake_body[0]

                 # Actualizar la posición de la cabeza de la serpiente según la dirección
                 if snake_direction == "LEFT":
                      head_x -= 1
                 elif snake_direction == "RIGHT":
                      head_x += 1
                 elif snake_direction == "UP":
                      head_y -= 1
                 elif snake_direction == "DOWN":
                      head_y += 1
                  # Verificar colisiones
                 if head_x < 0 or head_x >= 10 or head_y < 0 or head_y >= 10 or (head_x, head_y) in snake_body:
                      snake_game_active = False
                      return
                  # Comprobar si la serpiente ha comido
                 if (head_x, head_y) == food_position:
                      snake_body.insert(0, (head_x, head_y))
                      # Generar nueva posición de comida
                      while True:
                          new_food_position = (random.randint(0, 9), random.randint(0, 9))
                          if new_food_position not in snake_body:
                              food_position = new_food_position
                              break
                 else:
                      snake_body.insert(0, (head_x, head_y))
                      snake_body.pop()
def handle_input(input_str):
    global snake_direction
    if input_str.lower() == "izquierda":
        snake_direction = "LEFT"
    elif input_str.lower() == "derecha":
        snake_direction = "RIGHT"
    elif input_str.lower() == "arriba":
        snake_direction = "UP"
    elif input_str.lower() == "abajo":
        snake_direction = "DOWN"
@bot.command()
async def snake(ctx):
                 global snake_body, food_position, snake_direction, snake_game_active
                 snake_body = [(0, 0)]
                 food_position = (random.randint(0, 9), random.randint(0, 9))
                 snake_direction = "RIGHT"
                 snake_game_active = True

                 await ctx.send("¡Comenzando el juego Snake! Usa las reacciones para moverte. 🐍🍏")
                 game_board = await ctx.send(render_board())
                 await game_board.add_reaction("⬅️")
                 await game_board.add_reaction("➡️")
                 await game_board.add_reaction("⬆️")
                 await game_board.add_reaction("⬇️")

                 def check(reaction, user):
                     return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️", "⬆️", "⬇️"]

                 while snake_game_active:
                     try:
                         reaction, user = await bot.wait_for('reaction_add', check=check, timeout=10.0)
                         # Actualizar dirección según la reacción
                         if str(reaction.emoji) == "⬅️":
                             snake_direction = "LEFT"
                         elif str(reaction.emoji) == "➡️":
                             snake_direction = "RIGHT"
                         elif str(reaction.emoji) == "⬆️":
                             snake_direction = "UP"
                         elif str(reaction.emoji) == "⬇️":
                             snake_direction = "DOWN"

                         # Actualizar la posición de la serpiente
                         update_snake_position()
                         await game_board.edit(content=render_board())
                         await asyncio.sleep(0.5)  # Ajusta el tiempo según sea necesario

                     except asyncio.TimeoutError:
                         snake_game_active = False
                         await ctx.send("¡Tiempo agotado! El juego ha terminado.")

                 await ctx.send("¡Juego de Snake terminado!")

@bot.event
async def on_ready():
                 print(f'Conectado como {bot.user.name} (ID: {bot.user.id})')
                 print('------')
                 await bot.change_presence(activity=discord.Game(name="¡Bienvenido! Usa !snake o !akinator Made by Marcalachu"))
bot.run("your token here")
import random
from .translator import Translator

class JokeGenerator:
    def __init__(self):
        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why do Java developers wear glasses? Because they can't C#.",
            "How do you comfort a JavaScript bug? You console it.",
            "Why do Python programmers prefer snakes? Because they don’t like exceptions.",
            "Why did the developer go broke? Because he used up all his cache.",
            "What do you call a group of 8 hobbits? A hobbyte.",
            "Why don't programmers like nature? It has too many bugs.",
            "How many programmers does it take to change a light bulb? None, that’s a hardware issue.",
            "Why was the JavaScript developer sad? Because he didn’t know how to 'null' his feelings.",
            "Why do programmers hate nature? It has too many bugs.",
            "How do programmers open a bottle? They install `bottle.py`.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the JavaScript developer sad? Because he didn’t know how to `null` his feelings.",
            "Why do Java developers wear glasses? Because they can't C#.",
            "What is a programmer’s favorite type of music? Algo-rhythm.",
            "Why did the computer get cold? Because it left its Windows open.",
            "How do you comfort a JavaScript bug? You console it.",
            "Why do programmers prefer keyboards over mice? They don’t want to deal with point-and-click.",
            "Why did the developer go broke? Because he used up all his cache.",
            "Why don’t robots ever get tired? They’re wired for energy efficiency.",
            "How many programmers does it take to change a light bulb? None, that’s a hardware issue.",
            "Why don’t programmers like to climb stairs? Because they prefer recursion.",
            "Why was the computer stressed? It had too many tabs open.",
            "Why did the computer go to the doctor? It caught a virus.",
            "Why do programmers love coffee? It’s their favorite part of the Java stack.",
            "How does a computer get drunk? With screenshots.",
            "Why are assembly programmers always so calm? Because they can handle all their interrupts.",
            "Why do programmers love UNIX? Because it’s shell-tered from errors.",
            "What’s a computer’s favorite beat? Byte by byte.",
            "Why did the Python programmer break up with their partner? They couldn’t handle the exceptions.",
            "Why don’t programmers trust numbers? Because they’re always floating.",
            "Why do developers hate working on weekends? Because they don’t want to commit.",
            "How do you know if a programmer is an extrovert? They look at your shoes when they talk to you.",
            "Why was the programmer always so happy? He had a lot of 'try' in his life.",
            "Why don’t programmers like nature documentaries? They can’t handle all the trees.",
            "Why did the web developer go broke? Because they lost their domain.",
            "Why do programmers love gaming chairs? They support multi-threading.",
            "What’s a coder’s favorite dance move? The back-end flip.",
            "Why did the function refuse to go out with the variable? It said they had no class.",
            "Why was the smartphone always smiling? Because it had a lot of contacts.",
            "Why don’t hackers play cards? They’re afraid of the deck being stacked against them.",
            "Why are AI developers bad at relationships? They can’t handle real-life input.",
            "Why did the IT guy cross the road? To patch the other side.",
            "Why did the hard drive go on a diet? It had too many bytes.",
            "Why don’t cloud engineers ever get lost? They’ve always got a backup plan.",
            "Why do laptops never tell jokes? They’d just crash and burn.",
            "What did the network say to the server? 'I feel connected to you.'",
            "Why don’t servers get invited to parties? They always crash.",
            "Why are backups important? Because to err is human, but to restore is divine.",
            "What’s a computer’s favorite snack? Microchips.",
            "Why did the keyboard quit its job? It didn’t get a good return.",
            "Why don’t keyboards like parties? Too much space bar.",
            "Why did the binary tree feel lonely? It didn’t have enough branches.",
            "What do you call a rude programmer? A bit shift.",
            "Why do programmers hate time zones? Because they have no time for nonsense.",
            "What’s a computer’s favorite animal? A RAM.",
            "Why was the database so moody? It had too many relationships.",
            "Why don’t computers like seafood? They’re afraid of getting clams.",
            "Why did the computer sit in the corner? Because it needed to process some stuff.",
            "Why do programmers prefer Git? They love branching out.",
            "Why was the software engineer bad at dating? They couldn’t find the right connection.",
            "What’s a programmer’s favorite workout? Push-ups and pull requests.",
            "Why don’t programmers play hide and seek? They don’t want to deal with infinite loops.",
            "What’s the difference between a bug and a feature? Marketing.",
            "Why was the debugger so good at finding bugs? It had a great breakpoint.",
            "What’s a web developer’s favorite drink? JavaScript shake.",
            "Why do programmers love spreadsheets? They’re cell-f-taught.",
            "Why was the database administrator so calm? They always kept their cool in transactions.",
            "Why do programmers prefer dogs? They respond to commands."
        ]
        self.translator = Translator()

    def get_random_joke(self):
        """Returns a random joke."""
        return random.choice(self.jokes)

    def get_translated_joke(self, target_language="es"):
        """Returns a random joke translated to the target language."""
        joke = self.get_random_joke()
        return self.translator.translate(joke, target_language)

    def add_joke(self, joke):
        """Adds a new joke to the list."""
        self.jokes.append(joke)

    def get_all_jokes(self):
        """Returns a list of all jokes."""
        return self.jokes

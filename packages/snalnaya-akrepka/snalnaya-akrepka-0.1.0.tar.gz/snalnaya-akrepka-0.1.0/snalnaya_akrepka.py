from time import sleep
from os import system

def say(text):
	input(f"""
    _____     ____________
   /     \   | {text}    
  |   _   |   ----------	
  |  | \  |
  |  |  | |
  |  |  | |
  |  |  | |
  |		|
  | 	|
   \ __/    
    """)
	
def animated_say(text,number,delay):
	for i in range(number):
		print(f"""
    _____     ____________
   /     \   | {text.upper()}    
  |   _   |   ----------	
  |  | \  |
  |  |  | |
  |  |  | |
  |  |  | |
  |     |
  |     |
   \ __/    
    """)
		sleep(delay)
		system('cls||clear')
		print(f"""
    _____     ____________
   /     \   | {text}    
  |   _   |   ----------	
  |  | \  |
  |  |  | |
  |  |  | |
  |  |  | |
  |     |
  |     |
   \ __/
   """)   
		sleep(delay)
		system('cls||clear') 
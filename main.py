from recorder import Recorder

def main():
    r = Recorder()
    try:
        r.listen()
    except KeyboardInterrupt:
        print("\n..Bye!")
    
    
    
main()
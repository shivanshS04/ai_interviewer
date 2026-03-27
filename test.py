from utils.generate_audio import generate_audio

def main():
    try:
        generate_audio("Hello world")
        print("Success")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    main()

from RecordedPeopleGenerator import RecordedPeopleGenerator

if __name__ == "__main__":
    generator = RecordedPeopleGenerator()
    people = generator.generate(1000000, threads=6)
    print(people)
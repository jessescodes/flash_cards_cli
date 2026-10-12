# flash_card_cli.main.py

from pathlib import Path

from database import DataBase
from models import FlashCard, FlashQueue


def main():
    running = True
    db_path = Path("flashcard.db")
    queue = FlashQueue()
    db = DataBase(db_path)

    print("=" * 80)
    print("initializing DB")
    from_db = db.get_all_cards()
    for line in from_db:
        card = FlashCard(*line)
        queue.push(card)
    print(f"found {len(queue)} flashcards in DB")
    print("=" * 80)

    menu = "MAIN_MENU"

    while running:
        if menu == "MAIN_MENU":
            print("=" * 80)
            print("What do you want to do? /numeric choice/")
            print("[1] study next card")
            print("[2] add a card")
            print("[3] exit study tool")

            main_menu_choice = input().strip()

            if main_menu_choice == "1":
                if len(queue) == 0:
                    print("card deck is empty, add a card")
                    continue
                card = queue.pop()
                assert card is not None
                menu = "CARD_FRONT"
                continue
            if main_menu_choice == "2":
                menu = "ADD_CARD"
                continue
            elif main_menu_choice == "3":
                running = False
                continue
            else:
                print("Please make a valid numeric input")
                continue

        elif menu == "CARD_FRONT":
            print("=" * 80)
            print("FRONT")
            print(f"{card.front}")
            print(".")
            print(".")
            print(".")
            print("=" * 80)
            print("[1] Flip Card")
            print("[2] Skip Card")
            print("[3] Go Back")
            print("[4] Exit")
            front_choice = input().strip()

            if front_choice == "1":
                menu = "CARD_BACK"
                continue
            elif front_choice == "2":
                assert card is not None
                card.grade = 1
                card.calculate_next_interval()
                queue.push(card)
                menu = "MAIN_MENU"
                continue
            elif front_choice == "3":
                menu = "MAIN_MENU"
                continue
            elif front_choice == "4":
                running = False
                continue
            else:
                print("Please make a valid numeric input")
                continue

        elif menu == "CARD_BACK":
            print("=" * 80)
            print("BACK")
            print(f"{card.back}")
            print(".")
            print(".")
            print(".")
            print("[1] Rate Card Dificulty")
            print("[2] Back To Card Front")
            print("[3] Back to Main Menu")
            print("[4] Exit CLI Tool")
            back_choice = input().strip()

            if back_choice == "1":
                card.grade = int(back_choice)
                card.calculate_next_interval()
                queue.push(card)
                menu = "MAIN_MENU"
                continue
            elif back_choice == "2":
                menu = "CARD_FRONT"
                continue
            elif back_choice == "3":
                menu = "MAIN_MENU"
                continue
            elif back_choice == "4":
                running = False
                continue
            else:
                print("Please make a valid numeric input")
                continue

        elif menu == "ADD_CARD":
            print("=" * 80)
            print("ADD A FLASHCARD")
            print("Plase Add question")
            add_front = input()
            print("=" * 80)
            print("Please Add the Answer")
            add_back = input()
            new_card = FlashCard(add_front, add_back)
            queue.push(new_card)
            db_entry = db.insert_card(
                new_card.front,
                new_card.back,
                new_card.EF,
                new_card.interval,
                new_card.review_timestamp,
            )
            new_card.id = db_entry
            print("=" * 80)
            print(f"Your Flashcard decks is now {len(queue)} cards long")
            print("Would you like to?")
            print("[1] Add Another Card")
            print("[2] Return to Main Menu")
            print("[3] Exit the CLI Tool")

            while True:
                add_choice = input()
                if add_choice == "1":
                    menu = "ADD_CARD"
                    break
                elif add_choice == "2":
                    menu = "MAIN_MENU"
                    break
                elif add_choice == "3":
                    running = False
                    break
                else:
                    print("please make a valid numeric selection")
                    continue


if __name__ == "__main__":
    main()

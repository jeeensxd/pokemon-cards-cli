import argparse
import csv
from pathlib import Path

from .db import init_db
from .models.pokeset import PokeSet
from .models.card import Card


def cmd_init_db(args):
    init_db()
    print("Database geïnitialiseerd.")


def cmd_add_set(args):
    code = args.code
    name = args.name

    existing = PokeSet.get_by_code(code)
    if existing:
        print(f"Set met code '{code}' bestaat al: {existing.name}")
        return

    s = PokeSet.create(code, name)
    print(f"Set toegevoegd: {s.id} - [{s.code}] {s.name}")


def cmd_list_sets(args):
    sets = PokeSet.get_all()
    if not sets:
        print("Geen sets gevonden.")
        return

    for s in sets:
        print(f"{s.id}: [{s.code}] {s.name}")


def cmd_import_sets(args):
    csv_path = Path(args.file)

    if not csv_path.exists():
        print(f"CSV-bestand '{csv_path}' niet gevonden.")
        return

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if not row or len(row) < 2:
                continue

            code = row[0].strip()
            name = row[1].strip()

            if code.lower() == "code":
                continue

            if PokeSet.get_by_code(code):
                continue

            PokeSet.create(code, name)
            print(f"Set geïmporteerd: [{code}] {name}")


def cmd_add_card(args):
    name = args.name
    set_code = args.set_code
    count = int(args.count)
    price = float(args.price)

    pokeset = PokeSet.get_by_code(set_code)
    if not pokeset:
        print(f"Set met code '{set_code}' niet gevonden.")
        return

    card = Card.create(
        name=name,
        set_id=pokeset.id,
        count=count,
        price=price
    )

    print(
        f"Kaart toegevoegd: {card.id} - {card.name} "
        f"({pokeset.code} - {pokeset.name}), count={card.count}, price={card.price}"
    )


def cmd_import_cards(args):
    csv_path = Path(args.file)

    if not csv_path.exists():
        print(f"CSV-bestand '{csv_path}' niet gevonden.")
        return

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if not row or len(row) < 4:
                continue

            name = row[0].strip()
            set_code = row[1].strip()
            count_str = row[2].strip()
            price_str = row[3].strip()

            if name.lower() == "name":
                continue

            pokeset = PokeSet.get_by_code(set_code)
            if not pokeset:
                print(f"Set '{set_code}' niet gevonden voor kaart '{name}', overslaan.")
                continue

            try:
                count = int(count_str)
                price = float(price_str)
            except ValueError:
                print(f"Fout in getallen bij kaart '{name}', overslaan.")
                continue

            Card.create(
                name=name,
                set_id=pokeset.id,
                count=count,
                price=price
            )

            print(
                f"Kaart geïmporteerd: {name} "
                f"({pokeset.code}), count={count}, price={price}"
            )


def cmd_list_cards(args):
    """
    Toon kaarten gegroepeerd per set, zodat het overzicht niet 'door elkaar' lijkt.
    """
    cards = Card.get_all_with_set()
    if not cards:
        print("Geen kaarten gevonden.")
        return

    # sorteren op set_code, dan op naam
    cards = sorted(cards, key=lambda c: (c["set_code"], c["name"]))

    current_set = None
    for c in cards:
        set_key = (c["set_code"], c["set_name"])
        total = c["count"] * c["price"]

        # Als we in een nieuwe set zitten: nieuw kopje
        if set_key != current_set:
            current_set = set_key
            print()  # lege lijn voor leesbaarheid
            print(f"=== [{c['set_code']}] {c['set_name']} ===")

        # kaart onder de set tonen
        print(
            f"  #{c['id']}: {c['name']} | count={c['count']} | "
            f"price={c['price']} | total={total:.2f}"
        )



def cmd_export_cards(args):
    output = Path(args.output)
    cards = Card.get_all_with_set()

    if not output.parent.exists():
        output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(
            ["id", "name", "set_code", "set_name", "count", "price", "total"]
        )

        for c in cards:
            total = c["count"] * c["price"]
            writer.writerow(
                [
                    c["id"],
                    c["name"],
                    c["set_code"],
                    c["set_name"],
                    c["count"],
                    c["price"],
                    f"{total:.2f}",
                ]
            )

    print(f"Export klaar: {output}")


def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init-db")
    p_init.set_defaults(func=cmd_init_db)

    p_add_set = subparsers.add_parser("add-set")
    p_add_set.add_argument("--code", required=True)
    p_add_set.add_argument("--name", required=True)
    p_add_set.set_defaults(func=cmd_add_set)

    p_list_sets = subparsers.add_parser("list-sets")
    p_list_sets.set_defaults(func=cmd_list_sets)

    p_import_sets = subparsers.add_parser("import-sets")
    p_import_sets.add_argument("--file", required=True)
    p_import_sets.set_defaults(func=cmd_import_sets)

    p_add_card = subparsers.add_parser("add-card")
    p_add_card.add_argument("--name", required=True)
    p_add_card.add_argument("--set-code", required=True)
    p_add_card.add_argument("--count", required=True)
    p_add_card.add_argument("--price", required=True)
    p_add_card.set_defaults(func=cmd_add_card)

    p_import_cards = subparsers.add_parser("import-cards")
    p_import_cards.add_argument("--file", required=True)
    p_import_cards.set_defaults(func=cmd_import_cards)

    p_list_cards = subparsers.add_parser("list-cards")
    p_list_cards.set_defaults(func=cmd_list_cards)

    p_export = subparsers.add_parser("export-cards")
    p_export.add_argument("--output", required=True)
    p_export.set_defaults(func=cmd_export_cards)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

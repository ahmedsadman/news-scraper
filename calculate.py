import os

def get_line_count(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return len(f.readlines()) - 2 # -2 to skip heading and final newline

def get_total_data():
    count = 0
    files = os.listdir('.')
    for file in files:
        if not '.csv' in file:
            continue
        count += get_line_count(file)
    return count

if __name__ == "__main__":
    count = get_total_data()
    print(f"Total Data: {count}")
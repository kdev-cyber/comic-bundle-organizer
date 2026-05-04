import os
import re
import shutil
from helpers import get_input

print("\n=== Comic Bundle Organizer v2 ===\n")

# ===== SETTINGS / INPUT =====

source_folder = get_input(
    "Enter the path to the comic bundle folder",
    r"C:\Users\K\Desktop\Comic Organizer Test"
)

series_name = get_input(
    "Enter the full series name",
    "The Game"
)

short_code = get_input(
    "Enter the short code (example: 9T), or leave blank",
    ""
)

dry_run = get_input(
    "Dry run mode? Preview only, no files moved. (y/n)",
    "y"
).lower() == "y"

# ===== VALIDATION =====

if not os.path.exists(source_folder):
    print("[ERROR] Folder does not exist.")
    exit()

if not os.path.isdir(source_folder):
    print("[ERROR] Path is not a folder.")
    exit()

if not series_name:
    print("[ERROR] Series name cannot be blank.")
    exit()

# ===== FINAL FOLDER STRUCTURE =====

issues_folder = os.path.join(source_folder, "Issues")
covers_folder = os.path.join(source_folder, "Covers")
manga_folder = os.path.join(source_folder, "Manga")
extras_folder = os.path.join(source_folder, "Extras")
photos_folder = os.path.join(source_folder, "Photos")
videos_folder = os.path.join(source_folder, "Videos")
scripts_folder = os.path.join(source_folder, "Scripts")
review_folder = os.path.join(source_folder, "Review")

destination_folders = [
    issues_folder,
    covers_folder,
    manga_folder,
    extras_folder,
    photos_folder,
    videos_folder,
    scripts_folder,
    review_folder,
]

if not dry_run:
    for folder in destination_folders:
        os.makedirs(folder, exist_ok=True)

# ===== HELPERS =====

def extract_issue_number(filename):
    match = re.search(r"(\d+)", filename)
    return match.group(1).zfill(2) if match else None

def is_image_file(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))

def is_video_file(filename):
    return filename.lower().endswith((".mp4", ".mkv", ".avi"))

def is_script_file(filename):
    return filename.lower().endswith((".txt", ".docx"))

def is_cover_file(filename):
    return "cover" in filename.lower()

def get_unique_path(folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(folder, filename)
    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(folder, f"{base}_DUPLICATE_{counter}{ext}")
        counter += 1

    return candidate

def move_file(src, dst_folder, new_name=None):
    filename = new_name if new_name else os.path.basename(src)
    dst_path = get_unique_path(dst_folder, filename)

    if dry_run:
        print(f"[DRY RUN] {os.path.basename(src)} -> {dst_path}")
    else:
        shutil.move(src, dst_path)
        print(f"[MOVE] {os.path.basename(src)} -> {dst_path}")

# ===== MAIN SORT =====

def process_file(file_path):
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()

    if ext in [".cbz", ".cbr", ".pdf"]:
        issue_num = extract_issue_number(filename)

        if issue_num:
            new_name = f"{series_name} - Issue {issue_num}{ext}"
            move_file(file_path, issues_folder, new_name)
        else:
            move_file(file_path, review_folder)

    elif is_image_file(filename):
        if is_cover_file(filename):
            move_file(file_path, covers_folder)
        else:
            move_file(file_path, extras_folder)

    elif is_video_file(filename):
        move_file(file_path, videos_folder)

    elif is_script_file(filename):
        move_file(file_path, scripts_folder)

    else:
        move_file(file_path, extras_folder)

# ===== RUN =====

for item in os.listdir(source_folder):
    item_path = os.path.join(source_folder, item)

    if os.path.isfile(item_path):
        process_file(item_path)

print("\n[DONE] Import completed successfully.")
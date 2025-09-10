# Find UWorld Questions - Anki Add-on

A beautiful Anki add-on that extracts UWorld question IDs from selected cards/notes in the Browser and organizes them by exam type (Step 1, Step 2, Step 3, COMLEX 1, COMLEX 2).

## Features

- **Beautiful UWorld-themed UI**: Clean blue and white color scheme matching UWorld's branding
- **Tab-based interface**: Switch between Step 1, Step 2, Step 3, COMLEX 1, and COMLEX 2
- **Copy to clipboard**: Copy comma-separated list with option to include/exclude spaces
- **Deduplication**: Automatically removes duplicate IDs
- **Sorting**: IDs are displayed in ascending numeric order
- **Count display**: Shows number of questions found for each category
- **Credits**: Made by [Yusuf Ashktorab](https://ashklab.com)

## Installation

1. Copy the `find_uworld_questions` folder to your Anki add-ons directory:
   - Windows: `%APPDATA%\Anki2\addons21\`
   - Mac: `~/Library/Application Support/Anki2/addons21/`
   - Linux: `~/.local/share/Anki2/addons21/`

2. Restart Anki

## Usage

1. Open the Anki Browser
2. Select one or more cards or notes that contain UWorld tags
3. Right-click and select "Find UWorld Questions..."
4. The dialog will show UWorld IDs organized by exam type
5. Use the tabs to switch between different exam types
6. Copy IDs to clipboard or export to a text file

## Supported Tag Formats

The add-on recognizes these UWorld tag patterns:

### Step 1
- `#AK_Step1_v12::#UWorld::Step::829`
- `#AK_Step1_v{number}::#UWorld::Step::{id}`

### Step 2
- `#AK_Step2_v12::#UWorld::Step::4406`
- `#AK_Step2_v{number}::#UWorld::Step::{id}`

### Step 3
- `#AK_Step3_v12::#UWorld::12574`
- `#AK_Step3_v{number}::#UWorld::{id}` (no ::Step segment)

### COMLEX 1
- `#AK_Step1_v12::#UWorld::COMLEX::26114`
- `#AK_Step1_v{number}::#UWorld::COMLEX::{id}`

### COMLEX 2
- `#AK_Step2_v12::#UWorld::COMLEX::26114`
- `#AK_Step2_v{number}::#UWorld::COMLEX::{id}`

## Requirements

- Anki 2.1.66 or later
- Qt6 support

## Screenshots

The add-on features a clean, modern interface with:
- UWorld logo and branding
- Tabbed navigation for different exam types
- Blue question IDs for easy visibility
- Professional styling throughout

## Troubleshooting

- Make sure you have selected cards/notes in the Browser before right-clicking
- Ensure your tags follow the exact format patterns shown above
- The add-on is case-sensitive for tag matching

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Yusuf Ashktorab**
- GitHub: [@yusufashk](https://github.com/yusufashk)
- Website: [ashklab.com](https://ashklab.com)

---

*Made with ❤️ for the medical student community*

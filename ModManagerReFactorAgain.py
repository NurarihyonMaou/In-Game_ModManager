import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

Variables = """[Constants]
; Mod Manager
global $ModID = {Mod_ID}
global $CharacterModID = {CharacterModID}

global $IncludedInMaxCount = 0
global $Nura_Manager_First_Run = 1

global $Resources_Set = 0

"""

Present_Section = """[Present]
; Mod Manager
if $\\NuraThings\\ModManager\\ModData\\Active_{Model} == 1
    if $Nura_Manager_First_Run == 1
        pre $\\NuraThings\\ModManager\\first_run = 1
        $Nura_Manager_First_Run = 0
    endif

    if $\\NuraThings\\ModManager\\config_mode > 0
        if $\\NuraThings\\ModManager\\CharSwap == 1
            $IncludedInMaxCount = 0
            $Resources_Set = 0
        endif

        if $IncludedInMaxCount == 0
            if $\\NuraThings\\ModManager\\currentCharMaxID < $ModID
                $\\NuraThings\\ModManager\\currentCharMaxID = $ModID
            endif
            $IncludedInMaxCount = 1
        endif
    endif

else if $IncludedInMaxCount == 1
    $IncludedInMaxCount = 0
    post $Resources_Set = 0
endif

if $\\NuraThings\\ModManager\\ModData\\Model == $ModID
    post $mod_enabled = 1

    if $Resources_Set == 0
        post Resource\\NuraThings\\ModManager\\ModPath = ref ResourceModPath unless_null
        post Resource\\NuraThings\\ModManager\\ModName = ref ResourceModName unless_null
        post Resource\\NuraThings\\ModManager\\ModAuthor = ref ResourceModAuthor unless_null
        post Resource\\NuraThings\\ModManager\\ModDescription = ref ResourceModDesc unless_null
        post Resource\\NuraThings\\ModManager\\ModLink = ref ResourceModLink unless_null
        post Resource\\NuraThings\\ModManager\\ModLogo = ref ResourceModLogo unless_null

        post $Resources_Set = 1
    endif

else
    post $mod_enabled = 0
    post $Resources_Set = 0
endif



"""


def collect_ini_files(root_path):
    """
    Recursively collects .ini files from the given root path,
    excluding unwanted directories and files.
    """
    ini_files = []
    ini_paths = []

    def process_folder(folder_path):
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                if 'BufferValues' in dirpath or 'disabled' in dirpath.lower():
                    continue

                file_path = os.path.join(dirpath, filename)
                if filename.endswith(".ini") and "desktop" not in filename.lower() \
                        and "ntuser" not in filename.lower() and "backup" not in filename.lower() \
                        and "disabled" not in filename.lower():
                    ini_files.append(filename)
                    ini_paths.append(file_path)

    # Use multithreading to improve performance in large directory trees
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_folder, root_path)]
        for future in as_completed(futures):
            future.result()

    return ini_files, ini_paths


def get_common_words(identifiers):
    """
    This function receives a list of identifiers (strings) and returns the longest common sequence of words.
    It splits identifiers into words and then finds the longest common sequence across all identifiers.
    """

    # Split identifiers into words using uppercase letter boundaries and underscores as delimiters
    def split_into_words(identifier):
        return re.findall(r'[A-Z][a-z]*|[a-z]+', identifier)

    # Split each identifier into a list of words
    split_identifiers = [split_into_words(identifier) for identifier in identifiers]

    # Find the longest common sequence of words
    if not split_identifiers:
        return ''

    # Start with the first identifier's words
    common_words = split_identifiers[0]

    # Iterate through the rest of the identifiers to find the common words
    for words in split_identifiers[1:]:
        common_words = [word for word, common_word in zip(common_words, words) if word == common_word]
        if not common_words:
            break  # No common words found

    # Return the joined string of common words
    return ''.join(common_words)


def parse_ini_sections(file_path):

    """
    Parses the sections of an .ini file, extracting sections that include 'IB = ResourceX',
    creates a backup of the file if it doesn't exist, processes sections, and updates the file,
    while preserving content outside sections.
    """
    sections = []
    pre_section_content = []  # Content before the first section
    post_section_content = []  # Content after the last section
    ib_sections = []
    ib_array = {}
    repetitive_identifiers = set()

    namespace = ''

    # Regex patterns
    section_start_regex = re.compile(r"^\[(?!;).*?\]")  # Matches section headers
    ib_regex = re.compile(r"ib\s*=\s*(Resource|null).*", re.IGNORECASE)  # Matches 'IB = ResourceX'
    hash_regex = re.compile(r"hash\s*=\s*(\S+)", re.IGNORECASE)  # Captures 'hash = Hash'

    # Backup file logic
    backup_file_path = os.path.join(
        os.path.dirname(file_path),
        f"DISABLED_ModManagerBackup_{os.path.basename(file_path)}"
    )

    if not os.path.exists(backup_file_path):
        try:
            print(f"Creating backup: {backup_file_path}")
            with open(file_path, 'r', encoding='utf-8') as original_file:
                with open(backup_file_path, 'w', encoding='utf-8') as backup_file:
                    backup_file.write(original_file.read())
        except Exception as e:
            print(f"Error creating backup: {e}")
            return

    print(f"Processing file: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines.append('[')

            current_section = None
            in_section = False

            for line in lines:
                stripped_line = line.strip()

                if stripped_line == '[':
                    continue

                # Namespace detection
                if 'namespace' in stripped_line:
                    namespace = stripped_line
                    continue

                # Detect section headers
                if section_start_regex.match(stripped_line):
                    in_section = True
                    if current_section:  # Save the previous section
                        sections.append(current_section)
                    current_section = {'header': stripped_line, 'content': []}

                elif in_section and current_section:
                    current_section['content'].append(line.rstrip())

                elif not in_section:
                    pre_section_content.append(line.rstrip())

                elif not stripped_line:  # Preserve empty lines
                    if current_section:
                        current_section['content'].append(line.rstrip())

            # If a section was open at the end of the file, save it
            if current_section:
                sections.append(current_section)

    except UnicodeDecodeError:
        print(f"Error decoding file: {file_path}. Retrying with 'latin-1'.")
        with open(file_path, 'r', encoding='latin-1') as file:
            lines = file.readlines()
            lines.append('[')

            current_section = None
            in_section = False

            for line in lines:
                stripped_line = line.strip()

                if stripped_line == '[':
                    continue

                # Namespace detection
                if 'namespace' in stripped_line:
                    namespace = stripped_line
                    continue

                # Detect section headers
                if section_start_regex.match(stripped_line):
                    in_section = True
                    if current_section:  # Save the previous section
                        sections.append(current_section)
                    current_section = {'header': stripped_line, 'content': []}

                elif in_section and current_section:
                    current_section['content'].append(line.rstrip())

                elif not in_section:
                    pre_section_content.append(line.rstrip())

                elif not stripped_line:  # Preserve empty lines
                    if current_section:
                        current_section['content'].append(line.rstrip())

            # If a section was open at the end of the file, save it
            if current_section:
                sections.append(current_section)

    # Process sections for IB identifiers and hashes
    for section in sections:
        header = section['header']
        content = "\n".join(section['content'])

        # Check for IB entry directly in the section
        if ib_regex.search(content):
            # Handle IB section as before
            ib_sections.append(section)
        else:
            # Look for `run = CommandList...` in the section content
            commandlist_matches = re.findall(r"run\s*=\s*(CommandList\S+)", content, re.IGNORECASE)
            found_ib = False  # Flag to determine if IB was found in CommandLists

            for commandlist_name in commandlist_matches:
                # Locate the referenced CommandList section
                commandlist_section = next(
                    (s for s in sections if s['header'].strip("[]") == commandlist_name), None
                )

                if commandlist_section:
                    # Check for IB entry in the CommandList section
                    commandlist_content = "\n".join(commandlist_section['content'])
                    if ib_regex.search(commandlist_content):
                        # If found, treat the original section as an IB section
                        ib_sections.append(section)
                        found_ib = True
                        break  # Stop searching further CommandLists if one is valid

            # If no IB is found in the section or its referenced CommandLists, skip it
            if not found_ib:
                print(f"Section {header} is not an IB section (no valid `ib = Resource` found).")
                continue

        # Process IB section logic (identical to previous processing for hash, match indexes, etc.)
        hash_match = hash_regex.search(content)
        if hash_match:
            hash_value = hash_match.group(1).strip()

            # Extract optional match_first_index and match_index_count
            match_first_index = None
            match_index_count = None

            match_first_index_match = re.search(r"match_first_index\s*=\s*(\d+)", content)
            if match_first_index_match:
                match_first_index = int(match_first_index_match.group(1).strip())

            match_index_count_match = re.search(r"match_index_count\s*=\s*(\d+)", content)
            if match_index_count_match:
                match_index_count = int(match_index_count_match.group(1).strip())

            # Extract identifier from the header
            identifier = header.strip("[]")  # Remove square brackets
            identifier = re.sub(r"^(TextureOverride|ShaderOverride)", "", identifier).strip()  # Remove prefix

            repetitive_identifiers.add(identifier)

            if namespace == '':
                # Find the index where "Mods" is located and slice the path from there
                mods_index = file_path.lower().find("mods")  # Use lower() for case-insensitive matching
                if mods_index != -1:
                    namespace = file_path[mods_index + len("Mods"):]
                else:
                    namespace = file_path  # If "Mods" is not found, return the whole path

            if namespace not in ib_array:
                ib_array[namespace] = {}  # Initialize the namespace if it doesn't exist

            if identifier not in ib_array[namespace]:
                ib_array[namespace][identifier] = []  # Initialize the identifier if it doesn't exist

            # Check if hash is already in the array for this identifier
            hash_entry = {
                "hash": hash_value,
                "match_first_index": match_first_index,
                "match_index_count": match_index_count
            }

            # Avoid adding duplicates
            if not any(entry["hash"] == hash_value for entry in ib_array[namespace][identifier]):
                ib_array[namespace][identifier].append(hash_entry)
            else:
                print(f"Duplicate hash {repr(hash_value)} ignored for identifier {identifier}")

    # Update the .ini file with processed sections and preserved content
    global Variables
    global Present_Section

    try:
        with open(file_path, 'w', encoding = 'utf-8') as file:
            # Write pre-section content
            for line in pre_section_content:
                file.write(line + '\n')

            updated_sections = process_sections(sections)
            print("Before grab_resources:", updated_sections)

            updated_sections, resources = grab_resources(updated_sections, ib_array)
            print("After grab_resources:", updated_sections)

            # Write sections
            for section in updated_sections:
                if 'header' not in section or 'content' not in section:
                    print("Invalid section detected, skipping:", section)
                    continue
                file.write(section['header'] + '\n')
                for line in section['content']:
                    file.write(line + '\n')
                file.write('\n')  # Add a blank line between sections

            # Write post-section content
            for line in post_section_content:
                file.write(line + '\n')

            print(resources)
            file.write('\n\n'+resources)

            new_variables = []
            temp_variables = Variables

            for resource in resources.splitlines():
                resource = resource.replace('Resource', 'Model').replace("Diffuse", "").replace("IB", "").replace("Position", "").replace("Texcoord", "").replace(".", "").strip("[]")
                if resource is not '' and resource not in new_variables:
                    new_variables.append(resource)

            print(resources)
            for new_variable in new_variables:
                temp_variables += f"\n\nglobal ${new_variable} = 1"

            print(temp_variables, "YEGSEG")
            file.write('\n\n'+temp_variables)
            file.write('\n\n' + Present_Section)

        print(f"Updated .ini file: {file_path}")
    except Exception as e:
        print(f"Error updating .ini file: {e}")

    print(f"Finished processing file: {file_path}")
    return sections, ib_sections, ib_array, repetitive_identifiers


def process_all_ini_files(ini_paths):
    """
    Processes all .ini files in parallel, parsing their sections and
    extracting identifiers, IB sections, and IB hashes grouped by identifier.
    """
    all_sections = []
    all_ib_sections = []
    all_ib_array = {}
    all_identifiers = set()

    def parse_file(file_path):
        # Your implementation of parse_ini_sections()
        return parse_ini_sections(file_path)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(parse_file, path) for path in ini_paths]
        for future in as_completed(futures):
            sections, ib_sections, ib_array, identifiers = future.result()
            all_sections.extend(sections)
            all_ib_sections.extend(ib_sections)

            # Merge IB hashes by namespace and identifier
            for namespace, namespace_identifiers in ib_array.items():
                if namespace not in all_ib_array:
                    all_ib_array[namespace] = {}

                # Merge hashes for each identifier
                for identifier, hashes in namespace_identifiers.items():
                    if identifier not in all_ib_array[namespace]:
                        all_ib_array[namespace][identifier] = []

                    # Avoid duplicate hashes
                    for hash_value in hashes:
                        if hash_value not in all_ib_array[namespace][identifier]:
                            all_ib_array[namespace][identifier].append(hash_value)

            # Update all_identifiers with the identifiers from the current file
            all_identifiers.update(identifiers)

    return all_sections, all_ib_sections, all_ib_array, all_identifiers


def process_sections(sections, rabbit_thing=False):
    """
    Processes sections in a header-content format to add missing match_priority, allow_duplicate_hash, and conditionals.
    Ensures sections conform to the expected structure with proper indentation, preserving original order.

    Parameters:
        sections (list): List of sections, each a dictionary with 'header' and 'content'.
        rabbit_thing (bool): Whether to apply RabbitThing-specific logic.

    Returns:
        list: List of sections with an added 'modified' flag indicating if they were updated.
    """
    target_strings = ['match_priority', 'allow_duplicate_hash', 'match_first_index', 'match_index_count']
    processed_sections = []

    for section in sections:
        # Validate section structure
        if not isinstance(section, dict) or 'header' not in section or 'content' not in section:
            print(f"Skipping section: Expected dictionary with 'header' and 'content', got {type(section).__name__} -> {section}")
            continue

        header = section['header']
        content = section['content']
        original_content = list(content)  # Copy of the original content for comparison
        has_match_priority = any(
            key in line for line in content for key in target_strings
        )
        max_index = -1

        # Find the max index of target_strings in the content
        if has_match_priority:
            for i, line in enumerate(content):
                if any(target in line for target in target_strings):
                    max_index = max(max_index, i)

        # Find the hash line (excluding comments and duplicate directives)
        hash_index = [i for i, line in enumerate(content) if 'hash' in line and ';' not in line and 'allow_duplicate_hash' not in line]
        if not hash_index:
            section['modified'] = False  # No changes; retain the section as-is
            processed_sections.append(section)
            continue
        hash_index = hash_index[0]

        # Add match_priority or allow_duplicate_hash if missing
        if not has_match_priority:
            if '[TextureOverride' in header:
                content.insert(hash_index + 1, "match_priority = 0")
            elif '[ShaderOverride' in header:
                content.insert(hash_index + 1, "allow_duplicate_hash = True")

        # Add if $Mod_Enabled condition if missing
        if not any("if $Mod_Enabled" in line for line in content):
            priority_index = max_index if max_index > -1 else hash_index + 1
            content.insert(priority_index + 1, "if $Mod_Enabled")
            content.append("endif")

        # Adjust indentation for the content
        depth = 0
        indent = ' ' * 4
        indented_content = []

        for line in content:
            conditional = 0
            first_word = line.strip().split(' ')[0].lower()

            if first_word == 'if':
                depth += 1
                conditional = 1
            elif first_word in ['else', 'elif']:
                conditional = 1
            elif first_word == 'endif':
                depth -= 1

            indented_content.append(indent * (depth - conditional) + line.strip())

        content = indented_content

        # Apply RabbitThing-specific logic if enabled
        if rabbit_thing and any('$currentOutfit = $nextOutfit' in line for line in content):
            content.append("else")
            content.append(indent + "$currentOutfit = -1")
            content.append("endif")

        ## Remove redundant if $Mod_Enabled...endif pairs
        #content = [
        #    line for line in content
        #    if not (line.strip() == "if $Mod_Enabled" and content[content.index(line) + 1].strip() == "endif")
        #]

        # Remove redundant if $Mod_Enabled...endif pairs
        i = 0
        while i < len(content):
            line = content[i].strip()
            if line == "if $Mod_Enabled":
                # Check for an immediate 'endif' after 'if $Mod_Enabled'
                j = i + 1
                while j < len(content) and content[j].strip() == "":  # Skip empty lines
                    j += 1
                if j < len(content) and content[j].strip() == "endif":
                    # Remove 'if $Mod_Enabled' and 'endif', including empty lines in between
                    del content[i:j + 1]
                    continue  # Restart loop from the same index
            i += 1

        # Compare content to detect changes
        if content != original_content:
            processed_sections.append({'header': header, 'content': content, 'modified': True})
        else:
            processed_sections.append({'header': header, 'content': content, 'modified': False})

    return processed_sections


def grab_resources(ib_sections, ib_array):
    resources = ''

    for section in ib_sections:
        header = section.get('header', '')
        content = section.get('content', [])

        if not header or not content:
            print("Empty or malformed section:", section)
            continue

        # Extract identifier from the header
        identifier = header.strip("[]")  # Remove square brackets
        identifier = re.sub(r"^(TextureOverride|ShaderOverride)", "", identifier).strip()  # Remove prefix

        print("Processing identifier:", identifier)

        found = False
        match_first_index = None
        match_index_count = None

        for file_path, section_data in ib_array.items():
            if identifier in section_data:
                found = True
                resource_info = section_data[identifier][0]
                match_first_index = resource_info.get('match_first_index')
                match_index_count = resource_info.get('match_index_count')
                break

        if not found:
            print(f"Identifier {identifier} not found in IB Array.")
            continue

        hash_regex = re.compile(r"hash\s*=\s*(\S+)", re.IGNORECASE)  # Captures 'hash = Hash'
        # Extract hash value from the content
        hash_match = hash_regex.search("\n".join(content))
        if hash_match:
            hash_value = hash_match.group(1).strip()

            # Generate `resource_name`
            resource_name = f"Resource_{hash_value}_{match_first_index if match_first_index is not None else ''}{'_'+match_index_count if match_index_count is not None else ''}"

            # Locate the last `endif` in the section and add the logic above it
            mod_enabled_start = next((i for i, line in enumerate(content) if "if $Mod_Enabled" in line), None)
            mod_enabled_end = next(
                (i for i, line in enumerate(content) if line.strip() == "endif" and (mod_enabled_start is None or i > mod_enabled_start)), None)

            resources += f"[{resource_name}.Diffuse]\n" \
                        f"[{resource_name}.IB]\n" \
                        f"[{resource_name}.Position]\n" \
                        f"[{resource_name}.Texcoord]\n\n"

            resource_logic = [
                f"    if {resource_name}.IB == null",
                f"\t\t{resource_name}.IB = copy ib",
                f"    endif\n",

                f"    if {resource_name}.Position == null",
                f"\t\t{resource_name}.Position = copy vb0",
                f"    endif\n",

                f"    if {resource_name}.Texcoord == null",
                f"\t\t{resource_name}.Texcoord = copy vb1",
                f"    endif\n",

                f"    if {resource_name}.Diffuse == null",
                f"\t\tif ps == 037730.0 || ps == 037730.1",
                f"\t\t    {resource_name}.Diffuse = copy ps-t1",
                f"\t\telse",
                f"\t\t    {resource_name}.Diffuse = copy ps-t0",
                f"\t\tendif",
                f"    endif",
            ]

            print(f"Adding resource logic for {identifier}: {resource_logic}")

            if mod_enabled_end is not None:
                # Insert the new logic above the last `endif`
                content[mod_enabled_end:mod_enabled_end] = resource_logic
            else:
                # If no `if $Mod_Enabled` exists, append the entire block
                content.append("if $Mod_Enabled")
                content.extend(resource_logic)
                content.append("endif")

        section['content'] = content  # Update the section with the modified content
        print(f"Updated content for {identifier}:", content)

    return ib_sections, resources


if __name__ == "__main__":
    # Starting point for the search
    root_folder = os.getcwd()

    # Step 1: Collect all .ini files
    ini_files, ini_paths = collect_ini_files(root_folder)
    print(f"Found {len(ini_files)} INI files.")

    # Step 2: Process all .ini files
    sections, ib_sections, ib_array, identifiers = process_all_ini_files(ini_paths)
    print(f"Parsed {len(sections)} sections in total.")
    print(f"Found {len(ib_sections)} IB sections.")
    print(f"IB Hashes by Identifier: {ib_array}")
    print(f"Identifiers: {sorted(identifiers)}")

    # Array to store the new strings
    resource_strings = []

    # Helper function to create a unique string entry
    def create_unique_entry(hash_value, match_first_index, match_index_count, existing_array):
        # Build the string based on the provided values
        resource_name = f"Resource{hash_value}{match_first_index if match_first_index is not None else ''}{match_index_count if match_index_count is not None else ''}"
        texture_override_name = f"TextureOverride{hash_value}{match_first_index if match_first_index is not None else ''}{match_index_count if match_index_count is not None else ''}"

        new_entry = (
            f"[{resource_name}]\n\n"
            f"[{texture_override_name}]\n"
            f"hash = {hash_value}\n"
            f"match_priority = -100\n"
            f"{f'match_first_index = {match_first_index}\n' if match_first_index is not None else ''}"
            f"{f'match_index_count = {match_index_count}\n' if match_index_count is not None else ''}"
        )

        # Check if the entry is already in the array
        if new_entry not in existing_array:
            existing_array.append(new_entry)
        else:
            print(f"Skipped duplicate entry for hash: {hash_value}")

    # Iterate through the IB array to generate strings
    for namespace, identifiers in ib_array.items():
        for identifier, hashes in identifiers.items():
            for entry in hashes:
                hash_value = entry["hash"]
                match_first_index = entry.get("match_first_index")
                match_index_count = entry.get("match_index_count")

                # Create a unique string and add it to the array
                create_unique_entry(hash_value, match_first_index, match_index_count, resource_strings)




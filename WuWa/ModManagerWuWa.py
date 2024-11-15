# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import re
import json

#Characters = {'df65bb00': 'Albedo', '3ef08385': 'Alhaitham', '46de82f3': 'Aloy', 'a2ea4b2d': 'Amber', '557b2eff': 'AmberCN', '0107925f': 'Ayaka', 'b473c856': 'Ayato',
#              '17baa562': 'Baizhu', '85282151': 'Barbara', '8b9e7c22': 'BarbaraSummertime', '51197c51': 'Beidou', '6cff51b4': 'Bennett', '9cee8711': 'Candace',
#              'c5a6d98e': 'Charlotte', '4d8d965a': 'Chevreuse', '186eac84': 'Childe', 'c8e25747': 'Chiori', '489e3621': 'Chongyun', '07f8ad68': 'Clorinde',
#              '348e58c4': 'Collei', '226f076e': 'Cyno', '9aeecbcb': 'Dehya', '71625c4d': 'Diluc', 'a2d909c8': 'DilucFlamme', 'e8083f19': 'Diona', '2a2a63ab': 'Dori',
#              '107ba6e7': 'Eula', '6162188c': 'Faruzan', 'bf6aef4d': 'Fischl', '8f473224': 'FischlHighness', 'd2bfc751': 'Freminet', '8294fe98': 'Furina',
#              'b94ef036': 'GaMing', 'a5169f1d': 'Ganyu', '9b3f356e': 'GanyuTwilight', '3ce94cac': 'Gorou', '51a75ba6': 'Heizou', 'dd16576c': 'HuTao', '3e61a41f': 'Itto',
#              '191af650': 'Jean', '93bb2522': 'JeanCN', '16fef1eb': 'JeanSea', '8a081f34': 'Kaeya', 'b9b77eff': 'KaeyaSailwind', 'b56fd424': 'Kaveh', '7c0c47b3': 'Kazuha',
#              '3aaf3e94': 'Keqing', '0d7e3cc5': 'KeqingOpulent', 'b57d7fe2': 'Kirara', 'dcd74904': 'Klee', '0f5fedb4': 'KleeBlossomingStarlight', 'dde4750a': 'Kokomi',
#              'b82eaa26': 'KujouSara', '2656ccca': 'Layla', '2a557add': 'Lisa', '37c70461': 'LisaStudent', '98eb2db4': 'Lynette', '6f7b7740': 'Lyney', '1876e82e': 'Mika',
#              '7a1dc890': 'Mona', '515f3ce6': 'MonaCN', '7106f05d': 'Nahida', 'f4e09bd7': 'Navia', 'cad3a022': 'Neuvillette', 'b2acc1df': 'Nilou', 'f9e1b52b': 'Ningguang',
#              'db37b198': 'NingguangOrchid', 'd1384d15': 'Noelle', 'cad5bebb': 'Qiqi', 'e48c61f3': 'RaidenShogun', '4662c505': 'Razor', '748f40a5': 'Rosaria',
#              '59a1f8b1': 'RosariaCN', 'c70b7fce': 'Sayu', 'e44b58b5': 'Shenhe', 'ee0980eb': 'ShenheFrostFlower', '7cfb62ea': 'Shinobu', 'b655c335': 'Sucrose',
#              '24ecd71a': 'Thoma', 'ed2e7d59': 'Tighnari', 'c77e380b': 'TravelerBoy', '8239be13': 'TravelerGirl', '09a91a5c': 'Venti', '0110e1c7': 'Wanderer',
#              'aa6f1268': 'Wriothesley', '9427917d': 'Xiangling', '39838e8f': 'Xianyun', '9464bf2d': 'Xiao', '25aed172': 'Xingqiu', 'cc158a1e': 'XingqiuBamboo',
#              '76ed85f0': 'Xinyan', '3a7f71f5': 'Yae', 'eb8b62d3': 'Yanfei', '293449d6': 'YaoYao', 'c58c76f9': 'Yelan', '65618289': 'Yoimiya', '221f052e': 'YunJin',
#              'a75ba32e': 'Zhongli', '6895f405': 'Arlecchino'}

Characters = {
    "Aalto": [
        1,
        "4f0a1fba",
        "eacac19c"
    ],
    "Baizhi": [
        2,
        "d8d2286b",
        "f2a0c0fa"
    ],
    "CalcharoBody": [
        3,
        "9c24e7eb",
        "9c0c0163"
    ],
    "Changli": [
        4,
        "1ccb8008",
        "060f5303"
    ],
    "Chixia": [
        5,
        "9b69878e",
        "6d784a01"
    ],
    "Danjin": [
        6,
        "9f182348",
        "8b542cad"
    ],
    "Encore": [
        7,
        "388cecb3",
        "d4c99da1"
    ],
    "Jianxin": [
        8,
        "82d39ecb",
        "068dd115"
    ],
    "Jinshi": [
        9,
        "8fb7baf7",
        "4ae0a358"
    ],
    "Jiyan": [
        10,
        "7759b7d3",
        "dd2c2a00"
    ],
    "Lingyang": [
        11,
        "d02c1cb1",
        "2e3de562"
    ],
    "Mortefi": [
        12,
        "7d919713",
        "d35566be"
    ],
    "RoverFemale": [
        13,
        "ac681fc1",
        "972c1750"
    ],
    "RoverMale": [
        14,
        "3ab7c4d1",
        "a4be44e5"
    ],
    "Sanhua": [
        15,
        "a80e0e2b",
        "bf231a78"
    ],
    "Shorekeeper": [
        16,
        "78fd9b75",
        "eecaa360"
    ],
    "Taoqi": [
        17,
        "9f13087a",
        "9ab88d41"
    ],
    "Verina": [
        18,
        "15791c57",
        "5a5debf6"
    ],
    "XiangliYao": [
        19,
        "e61f4606",
        "5792c16a"
    ],
    "Yangyang": [
        20,
        "d70fa623",
        "1b1ed7be"
    ],
    "Yinlin": [
        21,
        "41d656e8",
        "0c7361ae"
    ],
    "Youhu": [
        22,
        "799c40e1",
        "87aaf3fd"
    ],
    "Yuanwu": [
        23,
        "0b0fecc4",
        "51677491"
    ],
    "Zhezhi": [
        24,
        "4cdc5987",
        "7ebe61e9"
    ]
}


Mod_IDs = {
    "Aalto": 1,
    "Baizhi": 1,
    "CalcharoBody": 1,
    "Changli": 1,
    "Chixia": 1,
    "Danjin": 1,
    "Encore": 1,
    "Jianxin": 1,
    "Jinshi": 1,
    "Jiyan": 1,
    "Lingyang": 1,
    "Mortefi": 1,
    "RoverFemale": 1,
    "RoverMale": 1,
    "Sanhua": 1,
    "Shorekeeper": 1,
    "Taoqi": 1,
    "Verina": 1,
    "XiangliYao": 1,
    "Yangyang": 1,
    "Yinlin": 1,
    "Youhu": 1,
    "Yuanwu": 1,
    "Zhezhi": 1
}

Variables = """; Mod Manager
global $ModID = {Mod_ID}
global $CharacterID = {Character_ID}

global $IncludedInMaxCount = 0
global $First_Run = 1

global $Resources_Set = 0

"""

Present_Section = """; Mod Manager
if $\\NuraThings\\ModManager\\CharacterModData\\Active_{Character_Name} == 1
    if $First_Run == 1
        pre $\\NuraThings\\ModManager\\first_run = 1
        $First_Run = 0
    endif

    if $\\NuraThings\\ModManager\\config_mode == 1
        if $\\NuraThings\\ModManager\\charSwap == 1
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

if $\\NuraThings\\ModManager\\CharacterModData\\{Character_Name} == $ModID
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

#Component_Hash = 'f02baf77'

Character_Name = ''
Character_ID = 0

use_mod_name = False

target_strings = ['match_priority', 'allow_duplicate_hash', 'match_first_index', 'match_index_count']

CharacterMaxVertexCount = {}

iteration = 0

def get_sections(data):
    return re.findall(r'(\[.*\][^\[]*?\n\s*hash\s*=\s*[a-f0-9]{8}[\s\S]*?)(?=\s*(?:\s*;.*\n)*\s*\[)\s*', data+'[', re.IGNORECASE)


def parse_key_section(match):
    section_name, section_text = match  # Unpack the tuple

    # Extract conditions, key, type, and variables
    conditions = re.search(r'conditions?\s*=\s*([^\n]+)', section_text, re.IGNORECASE)
    keys = re.findall(r'key\s*=\s*([^\n]+)', section_text, re.IGNORECASE)
    backs = re.findall(r'back\s*=\s*([^\n]+)', section_text, re.IGNORECASE)
    type_ = re.search(r'type\s*=\s*([^\n]+)', section_text, re.IGNORECASE)

    # Remove the condition line from section_text to avoid capturing its variables
    section_text_no_condition = re.sub(r'conditions?\s*=\s*([^\n]+)', '', section_text, flags=re.IGNORECASE)

    # Match the first uncommented variable declaration (ignoring lines starting with ;)
    variable_match = re.search(r'^\s*\$(\w+)\s*=\s*([^\n]+)', section_text_no_condition, re.IGNORECASE | re.MULTILINE)

    conditions = conditions.group(1).strip() if conditions else None
    keys = " or ".join([key.strip() for key in keys]) if keys else None
    backs = " or ".join([back.strip() for back in backs]) if backs else None
    type_ = type_.group(1).strip() if type_ else None

    variable_name = variable_match.group(1).strip() if variable_match else None
    variable_value = variable_match.group(2).strip() if variable_match else None
    number_count = len(re.findall(r'\d+', variable_value)) if variable_value else 0

    return [section_name, keys, type_, variable_name, variable_value, number_count, conditions, backs]


def get_toggles(data):
    pattern = r"""
    \[(Key[^\]]*)\]              # Match and capture section header (e.g., [Key*])
    (                            # Start of group to capture the section's content
    (?:\n(?!\[)[^\n]*)*?         # Match lines within the section, excluding lines starting with [
    )                            # End of group
    (?=\n\[\w|\Z)                # Stop when a new section starts (next [) or at the end of the string
    """

    # Compile the regex pattern with VERBOSE flag (without DOTALL)
    compiled_pattern = re.compile(pattern, flags=re.VERBOSE | re.IGNORECASE)

    # Find all matches
    matches = compiled_pattern.findall(data + '[')

    # Parse each matched section
    results = [parse_key_section(match) for match in matches]

    return results


def collect_ini(folder_path):

    global Variables
    global Present_Section

    global use_mod_name

    global Character_Name
    global Character_ID

    global Mod_IDs

    ini_files = []
    ini_paths = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if 'BufferValues' in file_path:
            continue

        if os.path.isdir(file_path):
            collect_ini(file_path)
        elif (os.path.splitext(filename)[1] == ".ini" and "desktop" not in filename.lower() and "ntuser" not in filename.lower() and "backup" not in filename.lower()) and 'disabled' not in filename.lower():
            ini_files.append(filename)
            ini_paths.append(file_path)


    for ini_file, ini_path in zip(ini_files, ini_paths):
        Sections = []
        Key_Conditions = []

        toggles = []

        head, tail = os.path.split(folder_path)
        mod_name = tail

        Character_Name = ''
        Character_ID = 0

        try:
            data = ''
            og_data = ''

            with open(os.path.join(folder_path, ini_file), "r+", encoding="utf-8") as f:
                data = f.read()

                toggles = get_toggles(data)

                if len(toggles) > 0:
                    print(toggles)
                    toggles_info = 'Toggle (Amount): Key(s) and Back(s)\n'
                    add_other_controls = False
                    for toggle in toggles:

                        if toggle[0] and toggle[1] and toggle[2] and toggle[4]:
                            if toggle[2] == 'hold':
                                add_other_controls = True

                            elif toggle[2] == 'toggle' or toggle[2] == 'cycle':
                                amount_of_toggles = 0
                                if toggle[2] == 'toggle':
                                    amount_of_toggles = 2
                                else:
                                    amount_of_toggles = toggle[5]
                                if toggle[0].replace('Key', '').capitalize() != toggle[3].capitalize():
                                    toggles_info += f'''\n{toggle[0].replace('Key', '').capitalize()}/{toggle[3].capitalize()} ({amount_of_toggles}): {toggle[1]}{" and "+toggle[7] if toggle[7] else ""}'''
                                else:
                                    toggles_info += f'''\n{toggle[3].capitalize()} ({amount_of_toggles}): {toggle[1]}{" and "+toggle[7] if toggle[7] else ""}'''

                    if add_other_controls:
                        toggles_info += '\n\n\nHold: Key(s)\n'
                        for toggle in toggles:
                            if (toggle[0] and toggle[1] and toggle[2] and toggle[4]) and (toggle[2] == 'hold'):
                                if toggle[0].replace('Key', '').capitalize() != toggle[3].capitalize():
                                    toggles_info += f'''\n{toggle[0].replace('Key', '').capitalize()}/{toggle[3].capitalize()}: {toggle[1]}'''
                                else:
                                    toggles_info += f'''\n{toggle[3].capitalize()}: {toggle[1]}'''

                    if toggles_info != 'Toggle (Amount) - Key\n':
                        with open(os.path.join(folder_path, 'Toggles.txt'), "w", encoding="utf-8") as ft:
                            ft.write(toggles_info)
                            ft.close()
                            print('Generated Toggles.txt inside - '+folder_path+'\n')

                if 'data = "Unnamed Mod"' in data or 'data = "Empty Mod Name"' in data or '[ResourceModName]' not in data:
                    use_mod_name = True

                og_data = data
                data_lines = data.splitlines()

                for condition_line in data_lines:
                    if 'condition = ' in condition_line and '$mod_enabled' not in condition_line:
                        if condition_line not in Key_Conditions:
                            Key_Conditions.append(condition_line)

                Sections = get_sections(data)

                for Chara in Characters:
                    if Characters[Chara][1] in data and Characters[Chara][2] in data:
                        Character_Name = Chara
                        Character_ID = Characters[Chara][0]
                        if mod_name is Chara+'Mod':
                            use_mod_name = False


                match_vertex_count = re.search(r'global \$mesh_vertex_count\s*=\s*(\d+)', og_data)
                Mesh_Vertex_Count = 0

                if match_vertex_count:
                    Mesh_Vertex_Count = int(match_vertex_count.group(1))

                if iteration == 0:
                    if Character_Name != '' and Mesh_Vertex_Count > 0:
                        print(CharacterMaxVertexCount, Mesh_Vertex_Count)
                        if Character_Name in CharacterMaxVertexCount:
                            if Mesh_Vertex_Count > CharacterMaxVertexCount[Character_Name]:
                                CharacterMaxVertexCount[Character_Name] = Mesh_Vertex_Count
                        else:
                            CharacterMaxVertexCount[Character_Name] = Mesh_Vertex_Count

                    continue

                if Character_Name != '' and 'global $mod_enabled = 0' in data and '$\\NuraThings\\ModManager\\CharacterModData' not in data and 'namespace = NuraThings' not in data:

                    if Character_Name in CharacterMaxVertexCount:
                        if Mesh_Vertex_Count < CharacterMaxVertexCount[Character_Name]:
                            data = data.replace(r'global $mesh_vertex_count = ' + str(Mesh_Vertex_Count),
                                                r'global $mesh_vertex_count = ' + str(CharacterMaxVertexCount[Character_Name]))

                    if len(Key_Conditions) > 0:
                        for condition in Key_Conditions:
                            if '$active' in condition or '$object_detected' in condition:
                                data = data.replace(condition, condition + ' && $mod_enabled')
                            else:
                                data = data.replace(condition, condition + '&& $object_detected && $mod_enabled')

                    for Section in Sections:
                        OldSection = Section
                        PartsOfSection = Section.splitlines()
                        has_match_priority = False

                        max_index = -1

                        if 'match_priority' in Section or 'allow_duplicate_hash' in Section or 'match_first_index' in Section or 'match_index_count' in Section:
                            has_match_priority = True

                            for i, elem in enumerate(Section):
                                if any(target_string in str(elem) for target_string in target_strings):
                                    max_index = max(max_index, i)


                        HashID = [index for (index, item) in enumerate(PartsOfSection) if
                                'hash' in item and ';' not in item and 'allow_duplicate_hash' not in item]

                        HashID = HashID[0]
                        Hash = PartsOfSection[HashID]


                        if not has_match_priority:
                            if '[TextureOverride' in Section:
                                Section = Section.replace(Hash, Hash+'\nmatch_priority = 0')
                            elif '[ShaderOverride' in Section:
                                Section = Section.replace(Hash, Hash+'\nallow_duplicate_hash = True')
                            PartsOfSection = Section.splitlines()


                        if 'if $mod_enabled' not in Section:
                            priority_index = max_index if max_index > -1 else HashID+1

                            Section = Section.replace(PartsOfSection[priority_index], PartsOfSection[priority_index]+'\nif $mod_enabled')

                            depth = 0
                            indent = ' ' * 4
                            indented_section_lines = []

                            for line in Section.splitlines():
                                conditional = 0
                                first_word = line.strip().split(' ')[0].lower()

                                if first_word == 'if':
                                    depth += 1
                                    conditional = 1

                                elif first_word in ['else', 'elif']:
                                    conditional = 1

                                elif first_word == 'endif':
                                    depth -= 1

                                indented_section_lines.append(indent * (depth - conditional) + line.strip())

                            Section = Section.replace(Section, '\n'.join(indented_section_lines))

                            Section += '\nendif'

                            if 'if $mod_enabled\nendif' in Section:
                                Section = Section.replace('if $mod_enabled\nendif\n', '')

                        data = data.replace(OldSection, Section)

                    data += '\n[Constants]\n' + Variables.format(Character_ID=Character_ID, Mod_ID=Mod_IDs[Character_Name])
                    Mod_IDs[Character_Name] = Mod_IDs[Character_Name]+1
                    data += '\n[Present]\n' + Present_Section.format(Character_Name=Character_Name)

                    if use_mod_name:
                        if '[ResourceModName]' not in og_data:
                            data += f'\n[ResourceModName]\ntype = Buffer\ndata = "{mod_name}"\n'
                        else:
                            if ';data = "Empty Mod Name"' in og_data:
                                data = data.replace('''[ResourceModName]
;type = Buffer
;data = "Empty Mod Name"
''', f'[ResourceModName]\ntype = Buffer\ndata = "{mod_name}"\n', 1)

                            elif 'data = "Unnamed Mod"' in og_data:
                                data = data.replace('''[ResourceModName]
type = Buffer
data = "Unnamed Mod"
''', f'[ResourceModName]\ntype = Buffer\ndata = "{mod_name}"\n', 1)

                        use_mod_name = False

                    if len(toggles) > 0:
                        data = data.replace('    if $Resources_Set == 0', '    if $Resources_Set == 0\n\tpost Resource\\NuraThings\\ModManager\\ModToggles = ref ResourceModToggles unless_null')
                        data += '''
[ResourceModToggles]
type = Buffer
format = R8_UINT
filename = Toggles.txt
'''

                    data += '\n[ResourceModPath]\ntype= Buffer\nformat = R8_UINT\nfilename = ModPath.txt'

                    with open(os.path.join(folder_path, 'ModPath.txt'), "w+", encoding="utf-8") as mp:
                        mp.write(ini_path)
                        mp.close()
                        print('Generated - '+os.path.join(folder_path, 'ModPath.txt')+'\n')

                    if data != og_data:
                        f.seek(0)
                        f.truncate(0)
                    f.close()

                if not os.path.exists(os.path.join(folder_path, 'DISABLED_ModManagerBackup_'+ini_file)):
                    with open(os.path.join(folder_path, 'DISABLED_ModManagerBackup_'+ini_file), "w", encoding="utf-8") as f:
                        f.write(og_data)
                        f.close()
                        print(f'''Created Backup - {os.path.join(folder_path, 'DISABLED_ModManagerBackup_' + ini_file)}
''')
                else:
                    print(f'''Backup already Exists - {os.path.join(folder_path, 'DISABLED_ModManagerBackup_' + ini_file)}
''')

                if data != og_data:
                    with open(os.path.join(folder_path, ini_file), "w", encoding="utf-8") as f:
                        f.write(data)
                        print(f'''Affected File - {ini_path}
''')
                        f.close()
                else:
                    print(f'''Analyzed File - {ini_path}
''')

        except Exception as e:
            print("Unable to open, skipping")
            print(f"Error: {e}")


def main():
    global Mod_IDs
    global iteration

    if os.path.exists(os.path.join(os.getcwd(), 'ModsIDs.json')):
        with open(os.path.join(os.getcwd(), 'ModsIDs.json'), 'r') as file:
            Mod_IDs = json.load(file)

    for iteration in range(2):
        collect_ini(os.getcwd())

    with open(os.path.join(os.getcwd(), 'ModsIDs.json'), 'w+') as file:
        json.dump(Mod_IDs, file)
        print('\nGenerated ModsIDs.json inside - '+os.getcwd())


main()
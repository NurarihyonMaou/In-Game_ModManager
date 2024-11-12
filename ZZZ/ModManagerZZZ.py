# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import re
import json

# Characters = {'df65bb00': 'Albedo', '3ef08385': 'Alhaitham', '46de82f3': 'Aloy', 'a2ea4b2d': 'Amber', '557b2eff': 'AmberCN', '0107925f': 'Ayaka', 'b473c856': 'Ayato',
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
"Anby": ["1", "9af848eb", "5c0240db", "496a781d", "91ffb01c", "1c9533eb", "4816de84", "a33e8b5e", "45b2509c"],
"Anton": ["2", "8ab64867", "6b95c80d", "bab585ea", "d46d8476", "339b1975", "653fb27c", "66217473", "9f262894", "9f0a8d2e", "a21fcee4", "1727e9e4", "112ccbbd"],
"Belle": ["3", "a9673001", "bea4a483", "11e38ebb", "142ddbbc", "d2844c01", "1817f3ca", "801edbf4", "ac1c8f80"],
"Ben": ["4", "b4db1979", "94288cca", "c7b58675", "dfd93ee5"],
"Billy": ["5", "5783253e", "21e98aeb", "5d6b7415", "3e4c0174", "36a0392d", "3371580a", "89eeb1af", "2e9d0312"],
"Corin": ["6", "7e7eee0d", "5a839fb2", "2cf242f4", "d345e472", "5dc40184", "e74620b5", "4c6b7bda", "2eb162ef", "4e1c9e44", "5f803336", "21987873", "1a7ee1b5"],
"Ellen": ["7", "ba0fe600", "d44a8015", "a27a8e1a", "77ac5f85", "b78f3616", "e30fae03", "5ac6d5ee", "cdce1fc2"],
"Grace": ["8", "1126fd58", "89299f56", "89d903ba", "9e96a54f", "8855c5cf", "8b240678", "4bb45448", "f1cba806"],
"Harumasa": ["9", "f5727f53", "f51a89c1", "9879fba3", "fa851c10", "5991a6b6", "aa7ba2dc", "9d044bbd", "7fdd2495", "3fa41462", "78bea30d", "8c561c8c", "cafffd37"],
"Jane": ["10", "24323bf9", "7b16a708", "257a90d6", "5721e4e7", "06f9bc49", "e2c0144e", "8b85c03e", "d1aa4b85"],
"Koleda": ["11", "e5de61e4", "242a8d48", "1a9b182a", "366e92ac", "28b188d4", "3afb3865", "e3021a32", "2c856fbc"],
"Lucy": ["12", "6c733c84", "198e99d7", "751e21a5", "5661afc3", "5da9dafc", "e0ad50ed", "00f11ea6", "da79199a", "637e5139", "a0ed04de", "0d4e37c6", "66cc3370", "5fb8059e", "272dd7f6", "856c6618", "9328313b", "90e47227", "9b6370f6", "170cc13e", "7e98735e", "2f5719df", "1fe6e084", "c789d6f4", "fa7b1c96"],
"Lycaon": ["13", "31eda4d5", "060bc1ad", "395572dc", "cc59d8d6", "b68056b4", "25196b7a", "949e688a", "2a340ed5", "30ba2096", "22a1347b", "ab4b6359", "916a8726", "ffbc21b0", "5e710f36", "911a4bae", "a11680ef"],
"Nekomata": ["14", "35439aa6", "da11fd85", "9ada013d", "a00df230", "eaad1408", "26a487ff", "f589a51f", "0c01e6a5", "3c4015fd", "74688145", "2a4f8c9e", "99132d05"],
"Nicole": ["15", "199853eb", "6847bbbd", "06e4fd79", "f6344432", "89df5a07", "5a4c1ef3", "91c1b779", "8cc1262b", "176bf3d7", "40e64ae2", "077c3500", "bb7fffe9"],
"Piper": ["16", "c4619559", "940454ef", "8b6b17f8", "da8a2564", "ffe8fea7", "585da98b", "a011f94e", "d28231af"],
"Qingyi": ["17", "dd08951b", "3cacba0a", "53a2b66e", "7b43d317", "ac54012f", "195857d8", "4cbe7fbe", "7be61bce"],
"Rina": ["18", "06c78cb0", "cdb2cc7d", "0dda44b1", "8ca7dc4b", "41149c54", "2825da1e", "4c259bf3", "03e8990d"],
"Seth": ["19", "9b358a6b", "35cf83ad", "a91eeef2", "d18b1600", "c5e25439", "00172ec3", "d4837e60", "2e990d11"],
"Soldier11": ["20", "cf814b3c", "2fa74e2f", "a1305cc6", "ba0c408b", "003ff258", "e3ee72d9", "29cd94d6", "59b61855"],
"Soukaku": ["21", "beac45e4", "fe70c7a3", "43fb429d", "5432bbb8", "a426e353", "ced49ff8", "176fb4d5", "ff00994d", "3a6a6326", "1315178e", "e261ddc0", "ddd3fb88"],
"Wise": ["22", "6235fa7f", "f6cac296", "fe89498c", "ba59bf09", "9581de22", "054ea752", "a012c752", "73c48816", "19f96193", "b1df5d22", "cb22cb95", "24ca2d36"],
"ZhuYuan": ["23", "d140d2e7", "9821017e", "f3c092c5", "a3091843", "f595d24d", "6619364f", "cb885260", "291f7f5a", "d55c7763", "5e717358", "1c68a02f", "dd91b126", "5f445c20", "fcac8411", "ac21fba4", "52e3c65f", "45d265c0", "a63028ae", "75c5e659", "82889576"],
"Caesar": ["24", "6de24342", "7a8fa826", "af291513", "bb723235", "7b6d4dab", "92061e5e", "3b2a70a5", "622b5a8d"],
"Burnice": ["25", "208d5e15", "af63e974", "35826de5", "be10c4bb", "511006ba", "f779fb81", "c882e6eb", "c22b4efe"],
"Yanagi": ["26", "0e52a354", "9e12899f", "42ca0c9b", "daba2b23", "fe235fbb", "13c75775", "49188dc8", "01864eed", "7ff000de", "f478ee4c", "f4fbc5c0", "2fe26340"]
}


#'Anby': ["1","9af848eb","5c0240db","39538886","91ffb01c","1c9533eb","4816de84","a33e8b5e","45b2509c"], 'Anton': ["2","8ab64867","6b95c80d","bab585ea","d46d8476","339b1975","653fb27c","66217473","9f262894","9f0a8d2e","a21fcee4","1727e9e4","112ccbbd"],
#'Belle': ["3","a9673001","bea4a483","11e38ebb","142ddbbc","d2844c01","1817f3ca","801edbf4","ac1c8f80"], 'Ben': ["4","b4db1979","94288cca","c7b58675","dfd93ee5"],
#'Billy': ["5","5783253e","21e98aeb","5d6b7415","3e4c0174","36a0392d","3371580a","89eeb1af","2e9d0312"], 'Corin': ["6","7e7eee0d","5a839fb2","2cf242f4","d345e472","5dc40184","e74620b5","4c6b7bda","2eb162ef","4e1c9e44","5f803336","21987873","1a7ee1b5"],
#'Ellen': ["7","ba0fe600","d44a8015","5c33833e","77ac5f85","b78f3616","e30fae03","5ac6d5ee","cdce1fc2"], 'Grace': ["8","1126fd58","89299f56","d21f32ad","9e96a54f","26ffa186","0f82a13e","e536af35","e5e04f6f"],
#'Harumasa': ["9","f5727f53","f51a89c1","9879fba3","fa851c10","5991a6b6","aa7ba2dc","9d044bbd","7fdd2495","3fa41462","78bea30d","8c561c8c","cafffd37"], 'Jane': ["10","24323bf9","7b16a708","c8ad344e","5721e4e7","06f9bc49","e2c0144e","8b85c03e","d1aa4b85"],
#'Koleda': ["11","e5de61e4","242a8d48","1a9b182a","366e92ac","28b188d4","3afb3865","e3021a32","2c856fbc"], 'Lucy': ["12","6c733c84","198e99d7","751e21a5","5661afc3","5da9dafc","e0ad50ed","00f11ea6","da79199a","637e5139","a0ed04de","0d4e37c6","66cc3370","5fb8059e","272dd7f6","856c6618","9328313b","90e47227","9b6370f6","170cc13e","7e98735e","2f5719df","1fe6e084","c789d6f4","fa7b1c96"],
#'Lycaon': ["13","31eda4d5","060bc1ad","395572dc","cc59d8d6","b68056b4","25196b7a","949e688a","2a340ed5","30ba2096","22a1347b","ab4b6359","916a8726","ffbc21b0","5e710f36","911a4bae","a11680ef"], 'Nekomata': ["14","35439aa6","da11fd85","9ada013d","a00df230","eaad1408","26a487ff","f589a51f","0c01e6a5","3c4015fd","74688145","2a4f8c9e","99132d05"],
#'Nicole': ["15","199853eb","6847bbbd","06e4fd79","f6344432","89df5a07","5a4c1ef3","91c1b779","8cc1262b","176bf3d7","40e64ae2","077c3500","bb7fffe9"], 'Piper': ["16","c4619559","940454ef","fd1b9c29","da8a2564","b2f3e6aa","585da98b","a0d146b3","d28231af"],
#'Qingyi': ["17","dd08951b","3cacba0a","0643440c","7b43d317","ac54012f","195857d8","4cbe7fbe","7be61bce","24282218","8e8426df","1707933f","fca2b042"], 'Rina': ["18","06c78cb0","cdb2cc7d","0dda44b1","8ca7dc4b","41149c54","2825da1e","4c259bf3","03e8990d"],
#'Seth': ["19","9b358a6b","35cf83ad","a91eeef2","d18b1600","c5e25439","00172ec3","d4837e60","2e990d11"], 'Soldier11': ["20","cf814b3c","2fa74e2f","a1305cc6","ba0c408b","003ff258","e3ee72d9","29cd94d6","59b61855"],
#'Soukaku': ["21","beac45e4","fe70c7a3","43fb429d","5432bbb8","a426e353","ced49ff8","176fb4d5","ff00994d","3a6a6326","1315178e","e261ddc0","ddd3fb88"], 'Wise': ["22","6235fa7f","f6cac296","fe89498c","ba59bf09","9581de22","054ea752","a012c752","73c48816","19f96193","b1df5d22","cb22cb95","24ca2d36"],
#'ZhuYuan': ["23","d140d2e7","9821017e","fdc045fc","a3091843","f595d24d","6619364f","cb885260","291f7f5a","d55c7763","5e717358","1c68a02f","dd91b126","5f445c20","fcac8411","ac21fba4","52e3c65f","45d265c0","a63028ae","75c5e659","82889576"]}
#
#'Anby': ['1', '9af848eb', '5c0240db', '91ffb01c', '39538886'], 'Anton': ['2', '8ab64867', '6b95c80d', 'd46d8476', 'bab585ea'], 'Belle': ['3', 'a9673001', 'bea4a483', '142ddbbc', '11e38ebb'],
#'Ben': ['4', 'b4db1979', '94288cca', 'dfd93ee5', 'c7b58675'], 'Billy': ['5', '5783253e', '21e98aeb', '3e4c0174', '5d6b7415'], 'Corin': ['6', '7e7eee0d', '5a839fb2', 'd345e472', '2cf242f4'],
#'Ellen': ['7', 'ba0fe600', 'd44a8015', '77ac5f85', '5c33833e'], 'Grace': ['8', '1126fd58', '89299f56', '9e96a54f', 'd21f32ad'], 'Harumasa': ['9', 'f5727f53', 'f51a89c1', 'fa851c10', '9879fba3'],
#'Jane': ['10', '24323bf9', '7b16a708', '5721e4e7', 'c8ad344e'], 'Koleda': ['11', 'e5de61e4', '242a8d48', '366e92ac', '1a9b182a'], 'Lucy': ['12', '6c733c84', '198e99d7', '5661afc3', '751e21a5'],
#'Lycaon': ['13', '31eda4d5', '060bc1ad', 'cc59d8d6', '395572dc'], 'Nekomata': ['14', '35439aa6', 'da11fd85', 'a00df230', '9ada013d'], 'Nicole': ['15', '199853eb', '6847bbbd', 'f6344432', '06e4fd79'],
#'Piper': ['16', 'c4619559', '940454ef', 'da8a2564', 'fd1b9c29'], 'Qingyi': ['17', 'dd08951b', '3cacba0a', '7b43d317', '0643440c'], 'Rina': ['18', '06c78cb0', 'cdb2cc7d', '8ca7dc4b', '0dda44b1'],
#'Seth': ['19', '9b358a6b', '35cf83ad', 'd18b1600', 'a91eeef2'], 'Soldier11': ['20', 'cf814b3c', '2fa74e2f', 'ba0c408b', 'a1305cc6'], 'Soukaku': ['21', 'beac45e4', 'fe70c7a3', '5432bbb8', '43fb429d'],
#'Wise': ['22', '6235fa7f', 'f6cac296', 'ba59bf09', 'fe89498c'], 'ZhuYuan': ['23', 'd140d2e7', '9821017e', 'a3091843', 'fdc045fc']}

Mod_IDs = {
    "Anby": 1,
    "Anton": 1,
    "Belle": 1,
    "Ben": 1,
    "Billy": 1,
    "Corin": 1,
    "Ellen": 1,
    "Grace": 1,
    "Harumasa": 1,
    "Jane": 1,
    "Koleda": 1,
    "Lucy": 1,
    "Lycaon": 1,
    "Nekomata": 1,
    "Nicole": 1,
    "Piper": 1,
    "Qingyi": 1,
    "Rina": 1,
    "Seth": 1,
    "Soldier11": 1,
    "Soukaku": 1,
    "Wise": 1,
    "ZhuYuan": 1,
    "Caesar": 1,
    "Burnice": 1,
    "Yanagi": 1
}

Variables = """; Mod Manager
global $Mod_Enabled = 0
global $ModID = {Mod_ID}
global $CharacterID = {Character_ID}

global $IncludedInMaxCount = 0
global $MM_First_Run = 1

global $Resources_Set = 0

"""

Present_Section = """; Mod Manager
if $\\NuraThings\\ModManager\\CharacterModData\\Active_{Character_Name} == 1
    if $MM_First_Run == 1
        pre $\\NuraThings\\ModManager\\First_Run = 1
        $MM_First_Run = 0
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
    post $Mod_Enabled = 1

    if $Resources_Set == 0
        post run = CommandListSetResources
    endif

else
    post $Mod_Enabled = 0
    post $Resources_Set = 0
endif


"""

Character_Name = ''
Character_ID = 0

preserve_data = False

use_mod_name = True

reset_next = False

target_strings = ['match_priority', 'allow_duplicate_hash', 'match_first_index', 'match_index_count']


def get_sections(data):
    return re.findall(r'(\[.*\][^\[]*?\n\s*hash\s*=\s*[a-f0-9]{8}[\s\S]*?)(?=\s*(?:\s*;.*\n)*\s*\[)\s*', data + '[',
                      re.IGNORECASE)


def parse_key_section(match):
    section_name, section_text = match  # Unpack the tuple

    # Extract conditions, key, type, and variables
    conditions = re.search(r'conditions? = ([^\n]+)', section_text, re.IGNORECASE)
    keys = re.findall(r'key\s*=\s*([^\n]+)', section_text, re.IGNORECASE)
    backs = re.findall(r'back\s*=\s*([^\n]+)', section_text, re.IGNORECASE)
    type_ = re.search(r'type = ([^\n]+)', section_text, re.IGNORECASE)
    variable_match = re.search(r'\$(\w+) = ([^\n]+)', section_text, re.IGNORECASE)

    conditions = conditions.group(1).strip() if conditions else None
    keys = " or ".join([key.strip() for key in keys])
    backs = " or ".join([back.strip() for back in backs])
    type_ = type_.group(1).strip() if type_ else None

    variable_name = variable_match.group(1).strip() if variable_match else None
    variable_value = variable_match.group(2).strip() if variable_match else None
    number_count = len(re.findall(r'\d+', variable_value)) if variable_value else 0

    return [section_name, keys, type_, variable_name, variable_value, number_count, conditions, backs]


def get_toggles(data):
    # return re.findall(r'\[(\w+)\]\s+condition\s*=\s*.*\s+key\s*=\s*(\d+)\s+type\s*=\s*(cycle|toggle)\s*\$(\w+)\s*=\s*((?:\d+,?)+)', data, re.IGNORECASE)
    pattern = pattern = r"""
\[(Key[^\]]*)\]              # Match and capture section header (e.g., [Key*])
(                            # Start of group to capture the section's content
(?:\n(?!\[)[^\n]*)*?         # Match lines within the section, excluding lines starting with [
)                            # End of group
(?=\n\[\w|\Z)              # Stop when a new section starts (next [) or at the end of the string
"""

    # Compile the regex pattern with VERBOSE flag (without DOTALL)
    compiled_pattern = re.compile(pattern, flags=re.VERBOSE | re.IGNORECASE)

    # Find all matches
    matches = compiled_pattern.findall(data + '[')
    # print(matches)
    results = [parse_key_section(match) for match in matches]

    return results


def collect_ini(folder_path):
    global Character_Name
    global Character_ID

    global use_mod_name

    ini_files = []
    ini_paths = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if 'BufferValues' in file_path:
            continue

        if 'disabled' not in file_path.lower() and os.path.isdir(file_path):
            collect_ini(file_path)

        elif (os.path.splitext(filename)[
                  1] == ".ini" and "desktop" not in filename.lower() and "ntuser" not in filename.lower()
              and 'disabled' not in filename.lower() and "backup" not in filename.lower()):
            ini_files.append(filename)
            ini_paths.append(file_path)

    for ini_file, ini_path in zip(ini_files, ini_paths):

        Sections = []
        Key_Conditions = []

        toggles = []

        if not preserve_data:
            Character_Name = ''
            Character_ID = 0

        head, tail = os.path.split(folder_path)
        mod_name = tail

        use_mod_name = True

        try:
            out_lines = []
            data = ''
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
                                    toggles_info += f'''\n{toggle[0].replace('Key', '').capitalize()}/{toggle[3].capitalize()} ({amount_of_toggles}): {toggle[1]}{" and " + toggle[7] if toggle[7] else ""}'''
                                else:
                                    toggles_info += f'''\n{toggle[3].capitalize()} ({amount_of_toggles}): {toggle[1]}{" and " + toggle[7] if toggle[7] else ""}'''

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
                            print('Generated Toggles.txt inside - ' + folder_path + '\n')

                og_data = data
                data_lines = data.splitlines()
                credits_string = ''
                if match := re.search(r'\[ResourceCreditInfo.*\][\s\S]*?data\s*=\s*\"(.*)\"', data, re.IGNORECASE):
                    credits_string = match.group(1)

                for condition_line in data_lines:
                    if 'condition = ' in condition_line and '$Mod_Enabled' not in condition_line:
                        if condition_line not in Key_Conditions:
                            Key_Conditions.append(condition_line)

                Sections = get_sections(data)

                for Chara in Characters:

                    # Iterate over the character's component data, skipping the first element (the ID)
                    for i in range(1, len(Characters[Chara]), 4):  # Step by 4 to get position_vb, ib, texcoord_vb, draw_vb sets
                        # Check if there are enough elements left in the array to access position_vb, ib, texcoord_vb, and draw_vb
                        if i + 3 < len(Characters[Chara]):
                            # Check if the current set of component hashes exist in og_data
                            if (Characters[Chara][i] in og_data and
                                Characters[Chara][i + 1] in og_data and
                                Characters[Chara][i + 2] in og_data and
                                Characters[Chara][i + 3] in og_data):

                                    Character_Name = Chara
                                    Character_ID = Characters[Chara][0]

                                    if mod_name is Chara + 'Mod':
                                        use_mod_name = False
                                    break
                        else:
                            break

                if 'global $ModID =' not in og_data and Character_Name != '' and ('TextureOverride' in og_data or 'ShaderOverride' in og_data)\
                        and 'namespace = NuraThings' not in og_data and '$\\NuraThings\\SkillCounter' not in og_data:

                    if len(Key_Conditions) > 0:
                        for condition in Key_Conditions:
                            if '$active' in condition or '$object_detected' in condition:
                                data = data.replace(condition, condition + ' && $Mod_Enabled', 1)
                            elif '$active' in data:
                                data = data.replace(condition, condition + ' && $active && $Mod_Enabled', 1)
                            else:
                                data = data.replace(condition, condition + ' && $Mod_Enabled', 1)

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
                                Section = Section.replace(Hash, Hash + '\nmatch_priority = 0', 1)
                            elif '[ShaderOverride' in Section:
                                Section = Section.replace(Hash, Hash + '\nallow_duplicate_hash = True', 1)
                            PartsOfSection = Section.splitlines()

                        if 'if $Mod_Enabled' not in Section:
                            priority_index = max_index if max_index > -1 else HashID + 1

                            Section = Section.replace(PartsOfSection[priority_index],
                                                      PartsOfSection[priority_index] + '\nif $Mod_Enabled', 1)

                            # print(PartsOfSection, HashID)

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

                            Section = Section.replace(Section, '\n'.join(indented_section_lines), 1)

                            Section += '\nendif'

                            if 'if $Mod_Enabled\nendif' in Section:
                                Section = Section.replace('if $Mod_Enabled\nendif', '')

                        data = data.replace(OldSection, Section, 1)

                    data += '\n[Constants]\n' + Variables.format(Character_ID=Character_ID,
                                                                 Mod_ID=Mod_IDs[Character_Name])
                    Mod_IDs[Character_Name] = Mod_IDs[Character_Name] + 1

                    data += '\n[Present]\n' + Present_Section.format(Character_Name=Character_Name)

                    set_toggles = "Resource\\NuraThings\\ModManager\\ModToggles = ref ResourceModToggles unless_null"

                    if use_mod_name:
                        data += f'''

[ResourceModName]
type = Buffer
data = "{mod_name}"

'''
                    else:
                        data += f'''

[ResourceModName]
;type = Buffer
;data = ""

'''

                    if credits_string != '':
                        data += f'''[ResourceModAuthor]
type = Buffer
data = "{credits_string}"

'''
                    else:
                        data += f'''[ResourceModAuthor]
;type = Buffer
;data = ""

'''

                    data += f'''[ResourceModDesc]
;type = Buffer
;data = ""

[ResourceModLink]
;type = Buffer
;data = ""

[ResourceModLogo]
;filename = 

{"""[ResourceModToggles]
type = buffer
format = R8_UINT
filename = Toggles.txt""" if len(toggles) > 0 else ""}

[CommandListSetResources]
Resource\\NuraThings\\ModManager\\ModPath = ref ResourceModPath unless_null
Resource\\NuraThings\\ModManager\\ModName = ref ResourceModName unless_null
Resource\\NuraThings\\ModManager\\ModAuthor = ref ResourceModAuthor unless_null
Resource\\NuraThings\\ModManager\\ModDescription = ref ResourceModDesc unless_null
Resource\\NuraThings\\ModManager\\ModLink = ref ResourceModLink unless_null
Resource\\NuraThings\\ModManager\\ModLogo = ref ResourceModLogo unless_null

{set_toggles if len(toggles) > 0 else ""}

$Resources_Set = 1
'''

                    data += '\n[ResourceModPath]\ntype= Buffer\nformat = R8_UINT\nfilename = ModPath.txt'

                    with open(os.path.join(folder_path, 'ModPath.txt'), "w+", encoding="utf-8") as mp:
                        mp.write(ini_path)
                        mp.close()
                        print('Generated - ' + os.path.join(folder_path, 'ModPath.txt') + '\n')

                    if data != og_data:
                        f.seek(0)
                        f.truncate(0)
                    f.close()

                if not os.path.exists(os.path.join(folder_path, 'DISABLED_ModManagerBackup_' + ini_file)):
                    with open(os.path.join(folder_path, 'DISABLED_ModManagerBackup_' + ini_file), "w",
                              encoding="utf-8") as f:
                        f.write(og_data)
                        f.close()
                        print(f'''Created Backup - {os.path.join(folder_path, 'DISABLED_ModManagerBackup_' + ini_file)}
''')
                else:
                    print(
                        f'''Backup already Exists - {os.path.join(folder_path, 'DISABLED_ModManagerBackup_' + ini_file)}
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

    if os.path.exists(os.path.join(os.getcwd(), 'ModsIDs.json')):
        with open(os.path.join(os.getcwd(), 'ModsIDs.json'), 'r') as file:
            Mod_IDs = json.load(file)

    collect_ini(os.getcwd())

    with open(os.path.join(os.getcwd(), 'ModsIDs.json'), 'w+') as file:
        json.dump(Mod_IDs, file)
        print('\nGenerated ModsIDs.json inside - ' + os.getcwd())


main()
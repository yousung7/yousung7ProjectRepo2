import settings, file_manager, re
from util import clear

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        words = list(set(settings.CURRENT_STRING.split()))
        for word in words:
            self.insert(word)

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def _find_all_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)

        for char, next_node in node.children.items():
            words.extend(self._find_all_from_node(next_node, prefix + char))
        return words

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_all_from_node(node, prefix)

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0: return []
    lps = compute_lps(pattern)
    i = j = 0
    results = []
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            results.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return results

def search_by_range(start_char, end_char):
    words = list(set(settings.CURRENT_STRING.split()))
    results = [word for word in words if start_char <= word[0] <= end_char]
    return sorted(results)


def search_by_starts_with(prefix):
    trie = Trie()
    return trie.starts_with(prefix)


def search_by_ends_with(suffix):
    words = list(set(settings.CURRENT_STRING.split()))
    return [word for word in words if word.endswith(suffix)]


def search_by_contains(pattern):
    indices = kmp_search(settings.CURRENT_STRING, pattern)
    if not indices:
        return "결과 없음"
    else:
        result_str = []
        for i in indices:
            start = max(0, i - 10)
            end = min(len(settings.CURRENT_STRING), i + len(pattern) + 10)
            result_str.append(f"...{settings.CURRENT_STRING[start:end]}...")
        return "\n".join(result_str)


def find_longest_shortest_sentences():
    original_text = file_manager.read_file(settings.FILE_PATH)
    if not original_text:
        print("원본 파일을 읽을 수 없습니다.")
        return

    sentences = re.split(r'([.!?])', original_text.replace('\n', ' '))
    sentences = ["".join(i).strip() for i in zip(sentences[0::2], sentences[1::2])]
    sentences = [s for s in sentences if s]

    if not sentences:
        print("분석할 문장이 없습니다.")
        return

    longest_sentence = max(sentences, key=len)
    shortest_sentence = min(sentences, key=len)

    print("\n========= 문장 분석 결과 =========")
    print(f"가장 긴 문장 (길이: {len(longest_sentence)}):")
    print(f"-> \"{longest_sentence}\"")
    print(f"\n가장 짧은 문장 (길이: {len(shortest_sentence)}):")
    print(f"-> \"{shortest_sentence}\"")
    print("==================================")


def search_menu():
    if not settings.CURRENT_STRING:
        print("먼저 파일 인덱싱을 수행해야 합니다. (메뉴 1번)")
        return

    while True:
        print("\n========= 텍스트 내 검색 메뉴 =========")
        print("1. 범위로 검색 (예: e-g로 시작하는 단어)")
        print("2. 특정 문자로 시작하는 단어 검색")
        print("3. 특정 문자로 끝나는 단어 검색")
        print("4. 특정 문자열 포함 검색")
        print("5. 가장 길고 짧은 문장 찾기")
        print("9. 이전 메뉴로")

        choice = input("선택: ")
        if choice == '1':
            _range = input("검색할 시작과 끝 문자를 입력하세요 (예: a-c): ").split('-')
            if len(_range) == 2:
                results = search_by_range(_range[0].strip(), _range[1].strip())
                print("검색 결과:", results)
            else:
                print("잘못된 입력입니다.")

        elif choice == '2':
            prefix = input("시작할 단어/접두어 입력: ")
            results = search_by_starts_with(prefix)
            print("검색 결과:", results)

        elif choice == '3':
            suffix = input("끝나는 단어/접미어 입력: ")
            results = search_by_ends_with(suffix)
            print("검색 결과:", results)

        elif choice == '4':
            pattern = input("포함될 문자열 입력: ")
            results = search_by_contains(pattern)
            print("검색 결과:\n", results)
        elif choice == '5':
            find_longest_shortest_sentences()
        elif choice == '9':
            break
        else:
            print("잘못된 선택입니다.")
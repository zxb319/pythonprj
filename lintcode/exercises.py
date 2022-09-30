class Solution:
    map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    imap = {
        1: 'I',
        5: 'V',
        10: 'X',
        50: 'L',
        100: 'C',
        500: 'D',
        1000: 'M',
    }

    def romanToInt(self, s: str) -> int:
        ts = 0
        p_num = 1000
        for c in s:
            c_num = Solution.map[c]
            ts += c_num

            if p_num < c_num:
                ts -= 2 * p_num

            p_num = c_num

        return ts

    def int_to_roman(self, num: int) -> str:
        res = []
        units = [1000, 100, 10, 1]
        for u in units:
            cnt = num // u
            if cnt == 9 and u != 1000:
                res.append(Solution.imap[u])
                res.append(Solution.imap[u * 10])
            elif cnt >= 5 and u != 1000:
                res.append(Solution.imap[u * 5])
                res.append(Solution.imap[u] * (cnt - 5))
            elif cnt == 4 and u != 1000:
                res.append(Solution.imap[u])
                res.append(Solution.imap[u * 5])
            else:
                res.append(Solution.imap[u] * cnt)
            num %= u

        return ''.join(res)


if __name__ == '__main__':
    num = 19940

    res = Solution().int_to_roman(num)

    print(res)

    print(Solution().romanToInt(res))

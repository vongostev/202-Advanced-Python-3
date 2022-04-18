class Parser:

    def __init__(self, path):
        self.path = path

    def parse(self) -> list[str]:
        with open(self.path, "r") as f:
            data = []
            di = {"\[": "\]", "\(": "\)", "$$": "$$", "\\begin{equation}": "\end{equation}"}
            for line in f:
                stack = []
                for i, s in enumerate(line):
                    flag: bool = False
                    if stack != [] and i < len(line) - 13 and line[i:i + 14] == stack[-1][0]:
                        data.append(line[stack[-1][1] + 16:i].strip())
                        stack.pop()
                        flag = True
                    if stack != [] and i < len(line) - 1 and line[i:i + 2] == stack[-1][0]:
                        data.append(line[stack[-1][1] + 2:i].strip())
                        stack.pop()
                        flag = True
                    if flag is False and i < len(line) - 1:
                        if line[i:i + 2] in {"$$", "\[", '\('}:
                            stack.append((di[line[i:i + 2]], i))
                    if flag is False and i < len(line) - 14 and line[i: i + 16] in di:
                        stack.append((di[line[i:i + 16]], i))
            return data

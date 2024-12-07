class SS:
    codes = [
        "Code 1: SS Example 1",
        "Code 2: SS Example 2",
        "Code 3: SS Example 3",
        "Code 4: SS Example 4",
        "Code 5: SS Example 5",
        "Code 6: SS Example 6",
        "Code 7: SS Example 7",
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return SS.codes[index - 1]
        except IndexError:
            return "Invalid code index. Please choose a number between 1 and 7."

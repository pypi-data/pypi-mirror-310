class DSP:
    codes = [
        "Code 1: DSP Example 1",
        "Code 2: DSP Example 2",
        "Code 3: DSP Example 3",
        "Code 4: DSP Example 4",
        "Code 5: DSP Example 5",
        "Code 6: DSP Example 6",
        "Code 7: DSP Example 7",
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return DSP.codes[index - 1]
        except IndexError:
            return "Invalid code index. Please choose a number between 1 and 7."

import locale

NUMBER_CONSTANT = {0: "zero ", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                   8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
                   14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"}
IN_HUNDRED_CONSTANT = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty",
                       9: "ninety"}
BASE_CONSTANT = {0: " ", 1: "hundred", 2: "thousand", 3: "million", 4: "billion"}


# supported number range is 1-n billion
def translateNumberToEnglish(number):
    if str(number).isnumeric():
        if str(number)[0] == '0' and len(str(number)) > 1:
            return translateNumberToEnglish(int(number[1:]))
        if int(number) < 20:
            return NUMBER_CONSTANT[int(number)]
        elif int(number) < 100:
            if str(number)[1] == '0':
                return IN_HUNDRED_CONSTANT[int(str(number)[0])]
            else:
                return IN_HUNDRED_CONSTANT[int(str(number)[0])] + "-" + NUMBER_CONSTANT[int(str(number)[1])]
        else:
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
            strNumber = locale.format_string("%d", number, grouping=True)
            numberArray = str(strNumber).split(",")
            stringResult = ""
            groupCount = len(numberArray) + 1
            for groupNumber in numberArray:
                if groupCount > 1 and groupNumber[0:] != "000":
                    stringResult += str(getUnderThreeNumberString(str(groupNumber))) + " "
                else:
                    break
                groupCount -= 1
                if groupCount > 1:
                    stringResult += BASE_CONSTANT[groupCount] + ","
            endPoint = len(stringResult) - len(" hundred,")
            # return stringResult[0:endPoint]
            return stringResult

    else:
        print("please input a number!")


# between 0-999
def getUnderThreeNumberString(number):
    if str(number).isnumeric() and len(number) < 4:
        if len(number) < 3:
            return translateNumberToEnglish(int(number))
        elif len(number) == 3 and number[0:] == "000":
            return " "
        elif len(number) == 3 and number[1:] == "00":
            return NUMBER_CONSTANT[int(number[0])] + "  " + BASE_CONSTANT[1]
        else:
            return NUMBER_CONSTANT[int(number[0])] + "  " + BASE_CONSTANT[1] + " and " + translateNumberToEnglish(
                (number[1:]))
    else:
        print("number must below 1000")

    # def testTranslateNumberToEnglish():
    #     print("0: " + translateNumberToEnglish(0))
    #     print("9: " + translateNumberToEnglish(9))
    #     print("33: " + translateNumberToEnglish(33))
    #     print("40: " + translateNumberToEnglish(40))
    #     print("100: " + translateNumberToEnglish(100))
    #     print("103: " + translateNumberToEnglish(103))
    #     print("123: " + translateNumberToEnglish(123))
    #     print("1,121,912  " + translateNumberToEnglish(1121912))
    #     print("211,121,900  " + translateNumberToEnglish(211121900))
    #     print("11,000,000  " + translateNumberToEnglish(11000000))
    #     print("1,111,121,912  " + translateNumberToEnglish(111121912))
    #     print("2,211,121,900  " + translateNumberToEnglish(2211121900))
    #     print("1,111,000,000  " + translateNumberToEnglish(1111000000))


def cut_first_num():
    for i in range(2, 7):
        try:
            file_content = ""
            with open('/Users/zekunzhang/PycharmProjects/caps/eng_res/' + str(i) + '.lab', 'r') as f:
                for line in f.readlines():
                    if line is '\n':
                        continue
                    else:
                        try:
                            temp = line
                            first = int(temp.split(' ')[0])
                            line = line.replace(str(first), '')
                        except ValueError as ve:
                            continue
                        finally:
                            file_content += line

            with open('/Users/zekunzhang/PycharmProjects/caps/eng_res/' + str(i) + '.lab', 'w') as w:
                w.write(file_content)

        except FileNotFoundError as e:
            print(e)


def translate_nums():
    for i in range(2, 7):
        try:
            file_content = ""
            with open('/Users/zekunzhang/PycharmProjects/caps/eng_res/' + str(i) + '.lab', 'r') as f:
                for line in f.readlines():
                    if line is '\n':
                        continue
                    else:
                        temp = line
                        res_line = ""
                        for word in temp.split(' '):
                            try:
                                have_nums = int(word)
                                word = translateNumberToEnglish(have_nums).upper()
                            except ValueError as ve:
                                continue
                            finally:
                                res_line += word + ' '

                        file_content += res_line

            with open('/Users/zekunzhang/PycharmProjects/caps/eng_res/' + 'with_eng_nums/' + str(i) + '.lab', 'w') as w:
                w.write(file_content)

        except FileNotFoundError as e:
            print(e)


if __name__ == '__main__':
    # test for numbers to english
    # testTranslateNumberToEnglish()

    # use this function to cut the first numbers of bible (you should first run this separately)
    # cut_first_num()

    # use this function to change translate all the numbers to english (remember to create a dir under the corpus to save the files)
    translate_nums()

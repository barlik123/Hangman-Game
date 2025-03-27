
import hangman_helper

def update_word_pattern(word, pattern, letter):
    #function that updates the word pattern for the state of the game
    pattern_list = []
    for char in pattern:
        pattern_list.append(char)
    for chr_ind in range(len(word)):
        if(word[chr_ind] == letter):
            pattern_list[chr_ind] = letter
    return ''.join(pattern_list)

def run_single_game(words_list, scr):
    word = hangman_helper.get_random_word(words_list)
    wrong_guess_list = []
    pattern = '_'*len(word)
    score = scr
    message = "The game as just started, lets see how well you do!"
    num_miss = len(pattern)
    while(num_miss > 0 and score > 0):
        num_miss = num_of_missing_letters(pattern)
        if(num_miss <= 0):
            break
        hangman_helper.display_state(pattern, wrong_guess_list, score, message)
        message = ""
        answer, player_guess = hangman_helper.get_input()
        if (answer == hangman_helper.LETTER):
            if (not player_guess.isalpha()) or len(player_guess) != 1 or player_guess.isupper():
                message = "The input is invalid"
                continue
            elif(player_guess in wrong_guess_list or player_guess in pattern):
                message = "This letter has already been guessed"
                continue
            else:
                score, wrong_guess_list, pattern = letter_in_word(score, word, player_guess, pattern, wrong_guess_list)
                continue
        elif (answer == hangman_helper.WORD):
            score -= 1
            if(player_guess == word):
                score += num_miss*(num_miss+1)//2
                pattern = word
                break
        elif (answer == hangman_helper.HINT):
            score -= 1
            final_hints_list = []
            hints_list = filter_words_list(hangman_helper.load_words(), pattern, wrong_guess_list)
            if(len(hints_list) > hangman_helper.HINT_LENGTH):
                for i in range(hangman_helper.HINT_LENGTH):
                    final_hints_list.append(hints_list[i*len(hints_list)//hangman_helper.HINT_LENGTH])
                hints_list = final_hints_list
            hangman_helper.show_suggestions(hints_list)

    if(score == 0):
        message = "You lost. The word was %s" %(word)
        hangman_helper.display_state(pattern, wrong_guess_list, score, message)
        return score
    num_miss = num_of_missing_letters(pattern)
    if(num_miss == 0):
        message = "Congratulations, you won!"
    hangman_helper.display_state(pattern, wrong_guess_list, score, message)
    return score

def num_of_missing_letters(pattern):
    #checks how many underscores are left to guess
    return num_of_shows(pattern, '_')

def letter_in_word(score,word,player_guess,pattern,wrong_guess_list):
    #executes the case in which the player guesses a letter.
    scr = score
    scr -= 1
    new_pattern = pattern
    wrg_guess_lst = wrong_guess_list
    num = num_of_shows(word, player_guess)
    if (num > 0):
        new_pattern = update_word_pattern(word, pattern, player_guess)
        scr += num * (num + 1) // 2
        return scr, wrg_guess_lst, new_pattern
    else:
        wrg_guess_lst.append(player_guess)
        return scr, wrg_guess_lst, new_pattern

def num_of_shows(word, letter):
    #Checks how many times a letter is shown in a word
    num = 0
    for chr_ind in range(len(word)):
        if (word[chr_ind] == letter):
            num += 1
    return num

def filter_words_list(words, pattern, wrong_guess_lst):
    #function that filter all the non possible words from an hint list
    final_list = []
    for word in words:
        if(len(word) == len(pattern) and check_lettering(word, pattern) and compare_word_wrgguess(word,wrong_guess_lst)):
            final_list.append(word)
    return final_list

def check_lettering(word, pattern):
    #checks if letters are in the same spots as pattern and if pattern letters do not exist in other spots
    for i, letter in enumerate(word):
        if(letter in pattern or pattern[i] != "_") and pattern[i] != letter:
            return False
    return True

def compare_word_wrgguess(word,wrong_guess_list):
    #checks if words contain letters from the wrong guess
    for letter in wrong_guess_list:
        if letter in word:
            return False
    return True

def main():
    #runs the games number of times
    num_played = 1
    word_list = hangman_helper.load_words()
    initial_score = hangman_helper.POINTS_INITIAL
    while(True):
        score = run_single_game(word_list, initial_score)
        if(score > 0):
            msg = "You played: %d games so far. \nWould you like to play another game?" %(num_played)
            is_again = hangman_helper.play_again(msg)
            initial_score = score
            num_played += 1
        else:
            msg = "You played: %d games so far. \nWould you like to start a new round of games?" %(num_played)
            is_again = hangman_helper.play_again(msg)
            initial_score = hangman_helper.POINTS_INITIAL
            num_played = 0
        if(is_again == False):
            break

if __name__ == "__main__" :
    main()

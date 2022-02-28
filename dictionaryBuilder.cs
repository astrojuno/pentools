// program to create every possible combination within the rules given of a set of characters
namespace dictionaryBuilder
{
    public class dictionaryBuilder
    {
        // CHANGE THESE FOR THE RULES
        // Constants
        // the max number of times a character should be repeated in a row, like next to each other.
        // 0 is for disregard this rule. So, if your set is a, b, c and this set to 0, then aaa is acceptable. 
        // if you have it set to 2, then aab is acceptable. If you have it set to 1, then abc is acceptable
        private const int MAX_CHARACTERS_TOGETHER = 1;

        // the max number of times a character can be repeated in the entire string. 0 is for disregard. So, if
        // you enter 0 then aaa is acceptable. If you enter 2, then aca is acceptable. If you enter 1, then abc is
        // acceptable.
        private const int MAX_CHARACTERS_REPEATED_IN_STRING = 2;

        // the length of the outputted password. 0 to make it the same length as the input characters.
        private const int PASSWORD_LENGTH = 10;

        // the filename to use. 
        private const string FILENAME = "lowercaseDictionary.txt";

        // the path to save the file to. "default" will be your home directory. 
        // only change this if you want to save it somewhere else...
        private const string FILE_PATH = "default";

        // NO TOUCHY TOUCHY BELOW HERE!
        // all your options are above, leave everything else alone...
        static void Main(string[] args)
        {
            // user feedback that task has started
            Console.WriteLine("yep");

            // where we're going to save it
            string saveLoc = getFilePath();

            // if the file is already there, don't overwrite it
            checkFilePath(saveLoc);
            
            //build the array
            List<char> characters = buildArray();

            // rules for the passwords
            // max number of characters repeated together
            const int charactersTogether = MAX_CHARACTERS_TOGETHER;
            // max number of characters repeated in the password
            const int charactersRepeated = MAX_CHARACTERS_REPEATED_IN_STRING;
            // length of passwords
            const int passwordLength = PASSWORD_LENGTH;

            List<string> passwords = makeMyPasswords(characters, charactersTogether, charactersRepeated, passwordLength);

            savePasswords(passwords);

            // user feedback that task has ended            
            Console.WriteLine("nup");

            System.Environment.Exit(0);
        }

        // setup the file path
        private static string getFilePath() {
            // where we're going to save it
            string filePath = "";
            if (FILE_PATH.ToLower() == "default") {
                filePath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            } else {
                filePath = FILE_PATH;
            }
            string fileName = FILENAME;
            
            return Path.Combine(filePath, fileName);
        }

        // check the filepath and quit if the file exists
        private static void checkFilePath(string path) {
            if(File.Exists(path)) {
                Console.WriteLine("File already exists, exiting...");
                System.Environment.Exit(1);
            }
        }

        // appends the list of passwords to the end of the file
        private static void savePasswords(List<string> passwords) {
            // get the file path
            string path = getFilePath();

            try {
                File.AppendAllLines(path, passwords);
            }
            catch(Exception e) {
                Console.WriteLine("Error: " + e);
                System.Environment.Exit(1);
            }
        }

        // fills an array with either UPPER or lower case letters and numbers and returns it
        private static List<char> buildArray() {
            // for testing, just use a couple of digits
            //return new List<char> {'a', 'b', 'c', 'd'};

            // 36 is every letter plus every single digit number
            // change a for A and z for Z for the uppercase version
            List<char> characters = new List<char>();
            for(char letter = 'a'; letter <= 'z'; letter++) {
                characters.Add(letter);
            }

            // add the numbers
            for(char i = '0'; i <= '9'; i++) {
                characters.Add(i);
            }
           
            return characters;
        }
        
        // generates and returns the passwords
        private static List<string> makeMyPasswords(List<char> characters, int charactersTogether, int charactersRepeated, int passwordLength) {
            // create the shells for the recursive calls
            List<string> passwords = new List<string>();
            string currentPassword = "";

            // check and set if necessary the repetition limist
            if (charactersRepeated > passwordLength || charactersRepeated == 0) {
                charactersRepeated = passwordLength;
            }
            if (charactersTogether > passwordLength || charactersTogether == 0) {
                charactersTogether = passwordLength;
            }
            if (passwordLength > characters.Count || passwordLength == 0) {
                passwordLength = characters.Count;
            }

            // send it off to be built...
            recursBuilder(characters, ref charactersTogether, ref charactersRepeated, ref passwordLength, passwords, currentPassword);

            return passwords;
        }

        // recursivley build the passwords
        private static void recursBuilder(List<char> characters, ref int charactersTogether, ref int charactersRepeated, ref int passwordLength, List<string> passwords, string currentPassword) {            
            // check to see if the total repeated characters in the string are too many
            int count = 0;
            foreach (char c in currentPassword) {
                if (c == currentPassword.Last()) {
                    count++;
                }
            }
            if (count > charactersRepeated) {
                return;
            }
            
            // check to see if the repeated characters together are too many
            char previousChar = '\0';
            int togetherCount = 0;
            foreach (char c in currentPassword) {
                if (previousChar == '\0') {
                    previousChar = c;
                } else {
                    if (previousChar == c) {
                        togetherCount++;
                        if (togetherCount >= charactersTogether) {
                            return;
                        }
                    } else {
                        previousChar = c;
                        togetherCount = 0;
                    }
                }
            }

            // if we have a full length password, add it to the list
            if (currentPassword.Length == passwordLength) {
                passwords.Add(currentPassword);
                if (passwords.Count > 10000000) {
                    savePasswords(passwords);
                    passwords.Clear();
                    Console.WriteLine("Save successful...");
                }
                return;
            }

            // recursively build the password
            foreach (char c in characters) {
                recursBuilder(characters, ref charactersTogether, ref charactersRepeated, ref passwordLength, passwords, currentPassword + c);
            }
        }
    }
}

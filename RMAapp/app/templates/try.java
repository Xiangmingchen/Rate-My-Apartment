public static DNA getLongestCommonSubsequnce(final DNA first, final DNA second) {
    dnaHelper(first.sequence, second.sequence); 
}

public static String dnaHelper(String first, String second) {
    if (first.length() == 0 || second.length() == 0) {
        return ""; 
    }
    if (first.charAt(first.length()-1) == second.charAt(second.length)) {

    }
}
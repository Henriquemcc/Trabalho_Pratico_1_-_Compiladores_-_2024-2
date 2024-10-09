int fact ( int n) {
    int ans = 1 ;
    while (n > 1 ) {
        ans *= n ;
        n--;
    }
    return ans ;
}
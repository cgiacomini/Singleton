package maths_functions

import "errors"

var ErrInvalidSummand = errors.New("Invalid summand")


// Add is our function that sums two non negative integers 
func Add(x, y int) (int, error) {
    if x <= 0 || y <= 0 {
        return 0, ErrInvalidSummand
    }
    return x + y, nil
}

// Subtract subtracts two integers
func Subtract(x, y int) (res int) {
    return x - y
}

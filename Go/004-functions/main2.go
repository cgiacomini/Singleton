package main
import "fmt"

func main() {
   fmt.Println(double(2))

   fmt.Println(add(2,4))
}

func double(number int) int {
   return number * 2
}

func add(num1, num2 int) int {
   return num1 + num2
}
